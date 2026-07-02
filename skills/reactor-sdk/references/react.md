# Reactor React SDK

Declarative React bindings built on top of `@reactor-team/js-sdk`. For imperative JS usage see [javascript.md](javascript.md).

## Install

```bash
npm install @reactor-team/js-sdk
```

React hooks and components ship from the same top-level package — there is no `/react` subpath.

## Provider setup

Wrap the subtree that needs Reactor access. Tracks are advertised by the server from the model's capabilities — do **not** pass `receive` or `send` props.

```tsx
import { ReactorProvider, ReactorView } from "@reactor-team/js-sdk";

export function App({ jwtToken }: { jwtToken: string }) {
  return (
    <ReactorProvider
      modelName="helios"
      jwtToken={jwtToken}
      connectOptions={{ autoConnect: true }}
    >
      <ReactorView className="w-full aspect-video" />
    </ReactorProvider>
  );
}
```

Fetch the JWT in a parent component (or via data-fetching library) and pass it in. Hooks below must be used inside a `ReactorProvider`.

`connectOptions` accepts `autoConnect?: boolean` (default `false`) plus `maxAttempts?: number` (SDP polling attempts, default 6).

## Hooks

```tsx
import {
  useReactor,
  useReactorMessage,
  useReactorInternalMessage,
  useStats,
} from "@reactor-team/js-sdk";
```

### `useReactor(selector)`

Generic selector over the store state. Destructure the fields you need — the store is flat:

```tsx
function StatusBanner() {
  const { status, lastError } = useReactor((s) => s);
  return <div>{status}{lastError ? ` — ${lastError.message}` : ""}</div>;
}
```

Store fields (state):

| Field | Type |
|---|---|
| `status` | `"disconnected" \| "connecting" \| "waiting" \| "ready"` |
| `tracks` | `Record<string, MediaStreamTrack>` — model-emitted tracks keyed by name |
| `lastError` | `ReactorError \| undefined` |
| `sessionId` | `string \| undefined` |
| `sessionExpiration` | `number \| undefined` |

Store fields (actions):

| Field | Signature |
|---|---|
| `connect` | `(jwt?, options?: ConnectOptions) => Promise<void>` |
| `disconnect` | `(recoverable?: boolean) => Promise<void>` |
| `reconnect` | `(options?: ConnectOptions) => Promise<void>` |
| `sendCommand` | `(name, data, scope?: MessageScope) => Promise<void>` |
| `publish` | `(name, track: MediaStreamTrack) => Promise<void>` |
| `unpublish` | `(name) => Promise<void>` |
| `uploadFile` | `(file: File \| Blob, options?: { name?: string }) => Promise<FileRef>` |

**Note the rename:** the store exposes `publish` / `unpublish` (not `publishTrack` / `unpublishTrack` — those names exist on the underlying `Reactor` class but hook consumers use the shorter names).

### `useReactorMessage(handler)`

Subscribes to model application messages. Handler is registered on mount, removed on unmount.

```tsx
function FrameCounter() {
  const [frame, setFrame] = useState(0);
  useReactorMessage((msg) => {
    if (msg.type === "state") setFrame(msg.data.current_frame);
  });
  return <div>Frame: {frame}</div>;
}
```

### `useReactorInternalMessage(handler)`

Subscribes to platform-level (runtime) messages — capabilities exchange and other control-plane data. Advanced; most apps use `useReactorMessage` instead.

### `useStats()`

Returns the latest `ConnectionStats` (RTT, jitter, bitrate, frames/sec, connection timings). Updates every ~2s while connected; `undefined` when disconnected.

## Rendering video

```tsx
import { ReactorView } from "@reactor-team/js-sdk";

function Scene() {
  return (
    <ReactorView
      className="w-full aspect-video rounded-lg"
      videoObjectFit="cover"
    />
  );
}
```

`ReactorViewProps`:

| Prop | Default | Purpose |
|---|---|---|
| `track` | `"main_video"` | Name of the recvonly video track to render |
| `audioTrack` | — | Optional recvonly audio track name (mixed into the same element) |
| `width`, `height` | — | Dimensions |
| `className`, `style` | — | Standard |
| `videoObjectFit` | `"contain"` | CSS `object-fit` |
| `muted` | `true` | Browser autoplay policies require muted-by-default |

For custom rendering or multiple named tracks, read `tracks[name]` from the store directly.

## Publishing a webcam

```tsx
import { ReactorProvider, WebcamStream, ReactorView } from "@reactor-team/js-sdk";

<ReactorProvider modelName="helios" jwtToken={jwt} connectOptions={{ autoConnect: true }}>
  <WebcamStream track="webcam" className="w-48 aspect-video" />
  <ReactorView className="w-full aspect-video" />
</ReactorProvider>;
```

`WebcamStream` handles `getUserMedia`, waits for `ready`, publishes the track, and unpublishes + stops the capture on unmount.

`WebcamStreamProps`:

| Prop | Default | Purpose |
|---|---|---|
| `track` | **required** | Sendonly track name; must match the model's input attribute |
| `videoConstraints` | `{ width: { ideal: 1280 }, height: { ideal: 720 } }` | `MediaTrackConstraints` for `getUserMedia` |
| `showWebcam` | `true` | Show the local preview |
| `className`, `style` | — | Standard |
| `videoObjectFit` | `"contain"` | CSS `object-fit` on the preview |

## Sending commands from components

```tsx
function PromptBox() {
  const { sendCommand, status } = useReactor((s) => s);

  const onSubmit = async (text: string) => {
    if (status !== "ready") return;
    // Command arg shapes are model-specific — verify against docs.reactor.inc/model-api-reference/<model>/schema
    await sendCommand("set_prompt", { prompt: text });
  };

  return <input disabled={status !== "ready"} onChange={(e) => onSubmit(e.target.value)} />;
}
```

Always gate sends on `status === "ready"`, or disable the control until ready — otherwise the call is rejected.

## File uploads

```tsx
function ImagePicker() {
  const { uploadFile, sendCommand, status } = useReactor((s) => s);

  const onFile = async (file: File) => {
    if (status !== "ready") return;
    const ref = await uploadFile(file);
    await sendCommand("set_image", { image: ref });
  };

  return <input type="file" onChange={(e) => e.target.files?.[0] && onFile(e.target.files[0])} />;
}
```

`FileRef` values can be mixed with scalar args in the same command payload, and multiple files can be passed in one command.

## Error handling and automatic reconnect

```tsx
function ErrorBanner() {
  const lastError = useReactor((s) => s.lastError);
  if (!lastError) return null;
  return (
    <div>
      <strong>{lastError.code}</strong>: {lastError.message}
    </div>
  );
}

function ReconnectOnRecoverable() {
  const { reconnect } = useReactor((s) => s);

  useEffect(() => {
    const handler = (error: ReactorError) => {
      if (error.recoverable) {
        setTimeout(() => reconnect(), (error.retryAfter ?? 3) * 1000);
      }
    };
    // Access the underlying Reactor via the store for direct event subscription.
    // Most apps can just watch `lastError` from useReactor instead.
    // ...
  }, [reconnect]);

  return null;
}
```

Dispatch on `lastError.recoverable` and `lastError.retryAfter` rather than matching specific error code strings.

## Manual connection control

Defer connection until a user action:

```tsx
<ReactorProvider modelName="helios" jwtToken={jwt} connectOptions={{ autoConnect: false }}>
  <ConnectButton />
</ReactorProvider>;

function ConnectButton() {
  const { connect, disconnect, reconnect, status } = useReactor((s) => s);
  return (
    <div>
      <button onClick={() => connect()} disabled={status !== "disconnected"}>Start</button>
      <button onClick={() => disconnect()} disabled={status === "disconnected"}>Stop</button>
      <button onClick={() => reconnect()}>Reconnect</button>
    </div>
  );
}
```

For brief network blips, pass `true` to `disconnect` so `reconnect()` can resume the server-side session:

```tsx
await disconnect(true);
// ... network recovers ...
await reconnect();
```

## Other exports

- `ReactorController` — a prebuilt connect/disconnect UI component; useful for demos and internal tools.
- `AbortError`, `isAbortError` — for distinguishing user-initiated cancellations from errors.
- `DEFAULT_BASE_URL` — the coordinator URL default (`https://api.reactor.inc`).

## Cleanup

`ReactorProvider` disconnects on unmount and on `beforeunload`. `WebcamStream` stops local tracks on unmount. For SPAs with long-lived trees, call `disconnect()` on route change if you want to release the GPU session early.
