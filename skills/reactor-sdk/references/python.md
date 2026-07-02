# Reactor Python SDK

Async, decorator-based API for scripts, servers, and data pipelines. Frames arrive as NumPy arrays for direct processing.

## Install

```bash
pip install reactor-sdk
```

Import as `reactor_sdk`.

## Minimal end-to-end example

```python
import asyncio
import os
from reactor_sdk import Reactor, ReactorStatus

async def main():
    reactor = Reactor(
        model_name="helios",
        api_key=os.environ["REACTOR_API_KEY"],
    )

    @reactor.on_status(ReactorStatus.READY)
    async def ready(status):
        await reactor.send_command("set_prompt", {"prompt": "a neon city"})

    @reactor.on_frame
    def on_frame(frame):
        # frame: np.ndarray, shape (H, W, 3), dtype uint8, RGB
        pass

    @reactor.on_error
    def on_error(err):
        print(f"[{err.component}:{err.code}] {err.message}")

    async with reactor:
        await asyncio.Event().wait()  # run until cancelled

asyncio.run(main())
```

The SDK fetches the JWT automatically from the API key — no separate token exchange needed. See [authentication.md](authentication.md) for key handling.

## Core API

| Method | Signature |
|---|---|
| Construct | `Reactor(model_name, api_key=None, api_url="https://api.reactor.inc", local=False)` |
| Connect | `await reactor.connect()` |
| Reconnect | `await reactor.reconnect()` — resume after `disconnect(recoverable=True)` |
| Disconnect | `await reactor.disconnect(recoverable=False)` — `True` keeps the session alive for `reconnect()` |
| Send command | `await reactor.send_command(command, data, scope=MessageScope.APPLICATION)` — requires `ReactorStatus.READY` |
| Publish track | `await reactor.publish_track(name: str, track: MediaStreamTrack)` |
| Unpublish track | `await reactor.unpublish_track(name: str)` |
| Upload file | `await reactor.upload_file(file, *, name=None, mime_type=None)` → `FileRef` |
| Context manager | `async with reactor:` — connects on enter, disconnects on exit |

`file` in `upload_file` can be a `str` path, `os.PathLike`, `bytes`, or a binary file-like object. `MessageScope` is `APPLICATION` (default; model commands) or `RUNTIME` (platform-level).

### State accessors

| Method | Returns |
|---|---|
| `reactor.get_status()` | `ReactorStatus` |
| `reactor.get_state()` | `ReactorState(status, last_error)` |
| `reactor.get_last_error()` | `Optional[ReactorError]` |
| `reactor.get_session_id()` | `Optional[str]` |
| `reactor.get_capabilities()` | Server capabilities (tracks, commands) once received |
| `reactor.get_remote_tracks()` | `dict[str, MediaStreamTrack]` — model-emitted tracks keyed by name |
| `reactor.get_session_info()` | Full session response |

## Decorators for events

```python
@reactor.on_status(ReactorStatus.READY)
async def handle_ready(status): ...

@reactor.on_status(ReactorStatus.DISCONNECTED)
def handle_disconnect(status): ...

# Multiple statuses
@reactor.on_status([ReactorStatus.CONNECTING, ReactorStatus.WAITING])
def handle_setup(status): ...

# No filter — fires on every status change
@reactor.on_status
def handle_any(status): ...

@reactor.on_frame
def handle_frame(frame):
    # np.ndarray (H, W, 3) uint8 RGB — do NOT block here
    pass

@reactor.on_track("main_video")
def handle_video_track(track):
    # Called when a specific named track is received. Gives you the raw
    # MediaStreamTrack for custom processing (e.g. routing to aiortc recording).
    pass

@reactor.on_message
def handle_message(message):
    # Model application messages
    ...

@reactor.on_internal_message
def handle_runtime_message(message):
    # Platform-level (runtime) messages. Advanced use.
    ...

@reactor.on_error
def handle_error(error):
    # ReactorError — see Error handling below
    ...
```

Register decorators **before** calling `connect()` (or entering `async with`) so you don't miss early events.

## Frame handling — critical pattern

`@on_frame` is called synchronously on the media thread. Slow handlers block frame delivery and cause the pipeline to drop frames. Offload real work:

```python
import asyncio
import queue

frame_queue: queue.Queue = queue.Queue(maxsize=32)

@reactor.on_frame
def enqueue(frame):
    try:
        frame_queue.put_nowait(frame)
    except queue.Full:
        pass  # drop if consumer is falling behind

async def consumer():
    loop = asyncio.get_running_loop()
    while True:
        frame = await loop.run_in_executor(None, frame_queue.get)
        await process(frame)  # heavy work here is fine
```

Typical offload targets:
- CPU-bound frame analysis → `run_in_executor` / `ProcessPoolExecutor`
- Disk writes → a dedicated writer task consuming the queue
- Network sends → `asyncio.create_task`

## Publishing video input

For video-to-video models, publish a `MediaStreamTrack`-compatible object captured from a file, camera, or other source (aiortc, av, etc.). The first argument to `publish_track` is the track **name** — it must match the server-side model's input attribute exactly.

```python
from reactor_sdk import Reactor, ReactorStatus

reactor = Reactor(model_name="helios", api_key=api_key)

@reactor.on_status(ReactorStatus.READY)
async def start_publishing(status):
    await reactor.publish_track("webcam", my_webcam_track)  # "webcam" matches model input
```

Call `await reactor.unpublish_track("webcam")` to stop, and stop the underlying capture yourself.

## File uploads

For commands that take files, upload first and pass the returned `FileRef` into `send_command`. Multiple `FileRef` values can be mixed with scalar args in one command:

```python
# From a path (name and MIME type inferred from filename)
ref = await reactor.upload_file("photo.jpg")

# From bytes (supply name so the runtime can infer MIME)
ref = await reactor.upload_file(image_bytes, name="photo.jpg")

# From a file-like object
with open("photo.jpg", "rb") as f:
    ref = await reactor.upload_file(f)

# Override MIME type explicitly
ref = await reactor.upload_file(blob, name="photo.jpg", mime_type="image/jpeg")

await reactor.send_command("set_image", {"image": ref, "strength": 0.7})
```

## Reconnection

For brief network blips, keep the session alive across a reconnect:

```python
await reactor.disconnect(recoverable=True)
# ... later, within the recovery window ...
await reactor.reconnect()
```

Without `recoverable=True`, reconnecting produces a fresh session with no prior state.

## Error handling

Errors surface through the `@on_error` decorator as `ReactorError` instances. Fields:

```python
@dataclass
class ReactorError:
    code: str
    message: str
    timestamp: float
    recoverable: bool
    component: Literal["api", "gpu"]
    retry_after: Optional[float] = None
```

Dispatch on `recoverable` + `retry_after` rather than matching specific code strings — the set of codes is not part of the stable public API:

```python
import asyncio
from reactor_sdk import ReactorError

@reactor.on_error
async def handle_error(err: ReactorError):
    print(f"[{err.component}:{err.code}] {err.message}")
    if err.recoverable:
        await asyncio.sleep(err.retry_after or 3)
        await reactor.reconnect()
```

`ConflictError` is raised for state conflicts (e.g., publishing a track name already in use). `VersionMismatchError` is raised when the SDK and server disagree on wire format (HTTP 426 / 501).

Don't raise from inside `@on_error` — the handler runs on the event loop.

## Env vars

Convention: `REACTOR_API_KEY`. Pass it explicitly to the constructor (`api_key=os.environ["REACTOR_API_KEY"]`) — the docs do not document an implicit env-var fallback. For minting JWTs on behalf of browser clients, see [authentication.md](authentication.md).
