# Copyright (c) 2026 Reactor Technologies, Inc. All rights reserved.
#
# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "transformers>=4.40",
#   "sentencepiece",
#   "ftfy",
# ]
# ///

"""CPU-only utility: count UMT5-XXL tokens in a string of text.

Mirrors the tokenization the lingbot pipeline uses in production
(``google/umt5-xxl`` with the ``whitespace`` cleaning pass from
``wan/modules/tokenizers.py``), so the count this returns is exactly
what the T5 text encoder receives at inference time — *before* the
pad / truncate to ``max_sequence_length`` (=512 by default; see
``wan/configs/shared_config.py::text_len``).

Standalone on purpose — does NOT ``import wan``. Importing ``wan``
triggers ``wan/__init__.py`` → ``wan.modules.t5``, which evaluates
``device=torch.cuda.current_device()`` as a default argument at
class-definition time and raises on a CPU-only host. The tokenizer
itself is pure-Python + sentencepiece, so it runs anywhere
``transformers`` does.

CLI::

    python token_count.py "a man walks down the street"
    python token_count.py --file prompt.txt
    echo "..." | python token_count.py -

Library::

    from token_count import count_tokens
    n = count_tokens("...")
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from functools import lru_cache

# Sourced from wan_shared_cfg.text_len, mirrored in
# LingbotPipeline.load() as `self.max_sequence_length`. Anything longer
# is truncated inside HuggingfaceTokenizer before reaching the encoder.
DEFAULT_MAX_SEQUENCE_LENGTH = 512

# HF id from wan/configs/wan_i2v_A14B.py:i2v_A14B.t5_tokenizer.
TOKENIZER_NAME = "google/umt5-xxl"


def _whitespace_clean(text: str) -> str:
    """Mirror wan.modules.tokenizers.basic_clean + whitespace_clean."""
    try:
        import ftfy
        text = ftfy.fix_text(text)
    except ImportError:
        # ftfy is a runtime dep of lingbot; if it's missing in a slim
        # CPU env we still produce a useful (slightly-less-canonical)
        # count rather than refusing to run.
        pass
    text = html.unescape(html.unescape(text)).strip()
    text = re.sub(r"\s+", " ", text).strip()
    return text


@lru_cache(maxsize=1)
def _get_tokenizer():
    from transformers import AutoTokenizer
    return AutoTokenizer.from_pretrained(TOKENIZER_NAME)


def count_tokens(text: str, *, clean: bool = True) -> int:
    """Return the number of UMT5-XXL tokens in ``text``.

    ``clean=True`` applies the same ftfy + html-unescape + whitespace
    collapse pass the pipeline runs before tokenizing.
    """
    if clean:
        text = _whitespace_clean(text)
    tok = _get_tokenizer()
    # No padding / truncation — we want the *raw* count so the caller
    # can decide whether it fits in max_sequence_length.
    return len(tok(text, add_special_tokens=True)["input_ids"])


def _main() -> int:
    ap = argparse.ArgumentParser(
        description=(
            "Count UMT5-XXL tokens for a string. Matches the lingbot "
            "pipeline's tokenization exactly."
        ),
    )
    ap.add_argument(
        "text", nargs="?", default=None,
        help="Text to tokenize. Use '-' to read from stdin. Omit if using --file.",
    )
    ap.add_argument("-f", "--file", help="Read text from a file path.")
    ap.add_argument(
        "--max", type=int, default=DEFAULT_MAX_SEQUENCE_LENGTH,
        help=f"Reference cap to flag against. Default {DEFAULT_MAX_SEQUENCE_LENGTH}.",
    )
    ap.add_argument(
        "--no-clean", action="store_true",
        help="Skip the ftfy/whitespace pre-clean. Off by default.",
    )
    args = ap.parse_args()

    if args.file and args.text:
        ap.error("pass either TEXT or --file, not both")
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    elif args.text == "-":
        text = sys.stdin.read()
    elif args.text is not None:
        text = args.text
    else:
        ap.error("no text given (provide TEXT, '-', or --file)")
        return 2  # unreachable, ap.error exits

    n = count_tokens(text, clean=not args.no_clean)
    over = n > args.max
    marker = "  (EXCEEDS — will be truncated)" if over else ""
    print(f"{n} tokens / {args.max} cap{marker}")
    return 1 if over else 0


if __name__ == "__main__":
    raise SystemExit(_main())
