#!/usr/bin/env python3
"""Generate a LingBot-World V2 seed image via Replicate's google/imagen-4.

Reactor-internal only: fetches the Replicate API token from the shared
"Replicate API Token" item in the team's 1Password "Shared" vault. Requires
the `op` CLI installed and signed in (`op account list` to check).

Usage:
  python3 generate_seed_image.py "<still-frame image prompt>" out/seed.png
  python3 generate_seed_image.py "<prompt>" out/seed.png --aspect-ratio 16:9
"""
import argparse
import json
import subprocess
import sys
import time
import urllib.request

REPLICATE_MODEL = "google/imagen-4"
OP_ITEM_ID = "ca7j2xiqudacdtiejflfaydznm"  # "Replicate API Token", Shared vault
ASPECT_RATIOS = ["1:1", "9:16", "16:9", "3:4", "4:3"]
OUTPUT_FORMATS = ["png", "jpg"]


def get_api_token():
    result = subprocess.run(
        ["op", "item", "get", OP_ITEM_ID, "--fields", "credential", "--reveal"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        sys.exit(
            "Failed to read the Replicate token from 1Password "
            f"(item {OP_ITEM_ID}). Run `op account list` to confirm you're "
            f"signed in, or `op item get {OP_ITEM_ID}` to check the item "
            f"still exists.\n{result.stderr}"
        )
    return result.stdout.strip()


def poll(get_url, token, timeout=120, interval=2):
    deadline = time.time() + timeout
    while time.time() < deadline:
        req = urllib.request.Request(get_url, headers={"Authorization": f"Bearer {token}"})
        with urllib.request.urlopen(req) as resp:
            body = json.load(resp)
        if body["status"] in ("succeeded", "failed", "canceled"):
            return body
        time.sleep(interval)
    raise TimeoutError("prediction did not complete within timeout")


def generate(prompt, aspect_ratio, output_format, token):
    req = urllib.request.Request(
        f"https://api.replicate.com/v1/models/{REPLICATE_MODEL}/predictions",
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Prefer": "wait",
        },
        data=json.dumps({
            "input": {
                "prompt": prompt,
                "aspect_ratio": aspect_ratio,
                "output_format": output_format,
            }
        }).encode(),
    )
    with urllib.request.urlopen(req, timeout=65) as resp:
        body = json.load(resp)
    if body.get("status") != "succeeded":
        body = poll(body["urls"]["get"], token)
    if body["status"] != "succeeded":
        raise RuntimeError(f"prediction {body['status']}: {body.get('error')}")
    output = body["output"]
    return output[0] if isinstance(output, list) else output


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("prompt", help="still-frame image prompt derived from the base prompt")
    ap.add_argument("output_path", help="where to save the downloaded image")
    ap.add_argument("--aspect-ratio", default="16:9", choices=ASPECT_RATIOS)
    ap.add_argument("--format", default="png", choices=OUTPUT_FORMATS, dest="output_format")
    args = ap.parse_args()

    token = get_api_token()
    url = generate(args.prompt, args.aspect_ratio, args.output_format, token)
    urllib.request.urlretrieve(url, args.output_path)
    print(f"saved seed image to {args.output_path}")


if __name__ == "__main__":
    main()
