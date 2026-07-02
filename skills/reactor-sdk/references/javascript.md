# Reactor JavaScript / TypeScript SDK

Imperative API for vanilla JS, TS, and non-React frameworks. React wrappers live in [react.md](react.md).

## Install

```bash
npm install @reactor-team/js-sdk
# or
pnpm add @reactor-team/js-sdk
```

## Minimal end-to-end example

```ts
import { Reactor } from "@reactor-team/js-sdk";

// Fetch a JWT from your server route. See authentication.md for the mint endpoint.
const r = await fetch("/api/token", { method: "POST" });
const { jwt } = await r.json();

const reactor = new Reactor({ modelName: "helios" });

reactor.on("statusChanged", async (status) => {
  if (status === "ready") {
    // Command args are model-specific; verify against docs.reactor.inc/model-api-reference/<model>/schema
    await reactor.sendCommand("set_prompt", { prompt: "a neon city" });
  }
});

reactor.on("trackReceived", (name, track, stream) => {
  const el = document.querySelector<HTMLVideoElement>("#output")!;
  el.srcObject = stream;
  el.play();
});

reactor.on("error", (error) => {
  if (error.recoverable) {
    setTimeout(() => reactor.reconnect(), (error.retryAfter ?? 3) * 1000);
  } else {
    console.error("reactor error:", error);
  }
});

await reactor.connect(jwt);

// Teardown
await reactor.disconnect();
```

Gate command sends on the `statusChanged` event rather than polling `getStatus()` — listeners must be registered before `connect()` or early transitions are missed.

Tracks are advertised by the server via the model's declared capabilities; the client does not declare `receive` or `send` arrays. The client only needs `modelName`.

## Core API

| Method | Signature |
|---|---|
| Construct | `new Reactor({ modelName, apiUrl?, local? })` |
| Connect | `reactor.connect(jwt?: string, options?: ConnectOptions): Promise<void>` |
| Reconnect | `reactor.reconnect(options?: ConnectOptions): Promise<void>` — resumes after `disconnect(true)` or a recoverable error |
| Disconnect | `reactor.disconnect(recoverable?: boolean): Promise<void>` — `true` keeps the session alive for `reconnect()` |
| Send command | `reactor.sendCommand(name, data, scope?: MessageScope): Promise<void>` — requires `ready` |
| Publish track | `reactor.publishTrack(name: string, track: MediaStreamTrack): Promise<void>` |
| Unpublish track | `reactor.unpublishTrack(name: string): Promise<void>` |
| Upload file | `reactor.uploadFile(file: File \| Blob, options?: { name?: string }): Promise<FileRef>` |
| Register listener | `reactor.on(event, handler)` / `reactor.off(event, handler)` |

`ConnectOptions` is `{ maxAttempts?: number }` — max SDP polling attempts (default 6). `MessageScope` is `"application"` (default; model commands) or `"runtime"` (platform-level).

### State accessors

| Method | Returns |
|---|---|
| `reactor.getStatus()` | `ReactorStatus` |
| `reactor.getState()` | `{ status, lastError? }` |
| `reactor.getLastError()` | `ReactorError \| undefined` |
| `reactor.getSessionId()` | `string \| undefined` |
| `reactor.getCapabilities()` | Server capabilities (tracks, commands) once received |
| `reactor.getSessionInfo()` | Full session response |
| `reactor.getStats()` | Connection stats (RTT, jitter, bitrate, frames/sec) |

## Events

```ts
reactor.on("statusChanged", (status: ReactorStatus) => {});
reactor.on("sessionIdChanged", (id: string | undefined) => {});
reactor.on("trackReceived", (name, track, stream) => {});
reactor.on("message", (message) => {});            // model application messages
reactor.on("runtimeMessage", (message) => {});     // platform-level messages (advanced)
reactor.on("error", (error: ReactorError) => {});
reactor.on("sessionExpirationChanged", (expiresAt: number | undefined) => {});
reactor.on("capabilitiesReceived", (capabilities) => {});
reactor.on("statsUpdate", (stats) => {});
```

Register listeners **before** `connect()`. The `statusChanged` event fires during the connection sequence — late registration misses `waiting` and `ready` transitions.

## Publishing a webcam (video-to-video)

The client doesn't declare inputs ahead of time; just publish once the session is `ready`. The track name must match the model's input attribute exactly.

```ts
import { Reactor } from "@reactor-team/js-sdk";

const reactor = new Reactor({ modelName: "helios" });

const stream = await navigator.mediaDevices.getUserMedia({ video: { width: 512, height: 512 } });
const [track] = stream.getVideoTracks();

reactor.on("statusChanged", async (status) => {
  if (status === "ready") {
    await reactor.publishTrack("webcam", track); // "webcam" = model's input attribute name
  }
});

await reactor.connect(jwt);

// Teardown
window.addEventListener("beforeunload", async () => {
  await reactor.unpublishTrack("webcam");
  stream.getTracks().forEach((t) => t.stop());
  await reactor.disconnect();
});
```

A name mismatch produces silent failure — no error, no frames. If video-to-video produces no output, check this first.

## File uploads

Commands that take files upload first and pass the returned `FileRef` into `sendCommand`. `FileRef` values mix freely with scalar args in the same command payload, and multiple `FileRef` values can be passed in one command:

```ts
const ref = await reactor.uploadFile(file);                    // File | Blob
const refWithName = await reactor.uploadFile(blob, { name: "photo.jpg" });

await reactor.sendCommand("set_image", { image: ref, strength: 0.7 });
```

## Error handling

The SDK emits `ReactorError` via the `"error"` event. Fields:

```ts
interface ReactorError {
  code: string;
  message: string;
  timestamp: number;
  recoverable: boolean;
  component: "api" | "gpu";
  retryAfter?: number; // seconds
}
```

Dispatch on `recoverable` / `retryAfter` rather than matching specific code strings — the set of codes is not part of the stable public API:

```ts
reactor.on("error", (error) => {
  if (error.recoverable) {
    setTimeout(() => reactor.reconnect(), (error.retryAfter ?? 3) * 1000);
    return;
  }
  console.error(`[${error.component}] ${error.code}: ${error.message}`);
});
```

Wrap `connect()` and `sendCommand()` calls in try/catch — both can throw on transport failures. `AbortError` / `isAbortError` are exported for distinguishing user-initiated cancellations.

## Env vars

| Context | Name |
|---|---|
| Node server minting JWTs | `REACTOR_API_KEY` |
| Browser bundle | **do not expose** — use a server route (see [authentication.md](authentication.md)) |

`NEXT_PUBLIC_*` / `VITE_*` variables are inlined into the shipped JS; never use them for production API keys.
