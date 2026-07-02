# Reactor models, commands, and messages

## Commands vs. messages

Reactor sessions carry two kinds of non-video data alongside the video stream:

- **Commands** — named actions your app sends to the model. Change what the model is doing in real time.
- **Messages** — structured JSON the model sends back to your app. Report state, signal events, push any data the model wants to share.

```ts
// JS
await reactor.sendCommand("set_prompt", { prompt: "a forest at dawn" });

reactor.on("message", (msg) => {
  if (msg.type === "state") console.log("frame:", msg.data.current_frame);
});
```

```python
# Python
await reactor.send_command("set_prompt", {"prompt": "a forest at dawn"})

@reactor.on_message
def on_message(msg):
    if msg.get("type") == "state":
        print("frame:", msg["data"]["current_frame"])
```

Commands can only be sent when the connection is `ready`. Messages can arrive at any time during the session.

## Authoritative source

Every model defines its own command and message surface. The authoritative spec for any model is its docs page:

- **Models index:** https://docs.reactor.inc/model-api-reference/overview
- **Per-model pages:** `https://docs.reactor.inc/model-api-reference/<name>/overview` (plus `/schema`, `/prompt-guide`, and `/tutorial` under the same path)

Each model page lists:
- Accepted commands (name, parameters, types)
- Messages the model emits
- Declared input tracks (client `publishTrack` / `publish_track` target)
- Declared output tracks (client `receive` side — read via `tracks[name]` in JS, `get_remote_tracks()` in Python)

Fetch the model page before writing a new integration. Command surfaces drift — do not assume commands from prior integrations still apply.

## Currently shipping

- **Helios** — interactive long-form real-time video generation with autoregressive chunked diffusion and image-to-video support. Model name: `"helios"`. See the `helios-prompts` skill for prompt-authoring rules.
- **LingBot** — interactive, navigable video worlds driven by a seed image, WASD/arrow-key controls, and live text prompts. Model name: `"lingbot"`. See the `lingbot-world` skill for world-authoring rules.
- **SANA-Streaming** — real-time video-to-video editing (restyle, swap, remove, overlay) on a live input stream. Model name: `"sana-streaming"`. See the `sana-streaming-prompts` skill for instruction-authoring rules.
- **LongLive** — long-form streaming video generation. Model name: `"longlive-v2"`.

Additional models ship regularly. Check `https://docs.reactor.inc/model-api-reference/overview` for the current roster before writing code against anything else.

## Track naming contract

For any video-to-video model, three names must agree exactly:

1. The publish call: JS `reactor.publishTrack("webcam", track)` / Python `reactor.publish_track("webcam", track)`
2. The model's input attribute as declared in its capabilities (advertised by the server)
3. The identifier used in any related command parameters

Mismatch at any layer causes silent failure — no error, no frames. If a video-to-video integration produces no output, check this first.

## Writing code for a new model

1. Fetch the model's docs page from `https://docs.reactor.inc/model-api-reference/<name>/overview`.
2. Identify its input/output tracks. Match names exactly when publishing.
3. Identify its command surface. Verify every command name and argument shape against the docs before sending.
4. Check for model-specific auth, rate limits, or session constraints.
5. Smoke-test: connect → wait for `ready` → send one command → verify a frame arrives. Layer real logic only after that round trip works.

## When the docs disagree with the SDK

If a command shape differs between the docs page and what the SDK accepts, trust the SDK error message (it comes from the live model) and flag the docs discrepancy to the Reactor team.
