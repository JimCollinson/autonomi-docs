# gRPC Services

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: 6c4df9b745f3adcb022ac82b6bbc485727297e3e
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->

This page describes the gRPC surface exposed by `antd` on `localhost:50051` by default.

Unlike the REST API, the gRPC API carries raw bytes in protobuf fields rather than base64 strings in JSON.

## HealthService

### `Check(HealthCheckRequest) -> HealthCheckResponse`

Checks daemon health and network selection.

**Response fields:**

| Name | Type | Description |
|------|------|-------------|
| `status` | string | Expected `ok` on success |
| `network` | string | Current network name |

## DataService

### `GetPublic(GetPublicDataRequest) -> GetPublicDataResponse`

Fetches public data by address.

### `PutPublic(PutPublicDataRequest) -> PutPublicDataResponse`

Stores public data.

### `StreamPublic(StreamPublicDataRequest) -> stream DataChunk`

Streams public data chunks.

### `GetPrivate(GetPrivateDataRequest) -> GetPrivateDataResponse`

Fetches private data using a `data_map` string.

### `PutPrivate(PutPrivateDataRequest) -> PutPrivateDataResponse`

Stores private data and returns a `data_map` string.

### `GetCost(DataCostRequest) -> Cost`

Estimates storage cost for a byte payload.

## ChunkService

### `Get(GetChunkRequest) -> GetChunkResponse`

Fetches a chunk by address.

### `Put(PutChunkRequest) -> PutChunkResponse`

Stores a raw chunk.

## FileService

### `UploadPublic(UploadFileRequest) -> UploadPublicResponse`

Uploads a local file path.

### `DownloadPublic(DownloadPublicRequest) -> DownloadResponse`

Downloads a public file to a local destination path.

### `DirUploadPublic(UploadFileRequest) -> UploadPublicResponse`

Uploads a local directory path.

### `DirDownloadPublic(DownloadPublicRequest) -> DownloadResponse`

Downloads a public directory to a local destination path.

### `GetFileCost(FileCostRequest) -> Cost`

Estimates file upload cost.

## EventService

### `Subscribe(SubscribeRequest) -> stream ClientEventProto`

Streams client events from the daemon.

`ClientEventProto` currently includes:

| Name | Type | Description |
|------|------|-------------|
| `kind` | string | Event kind |
| `records_paid` | uint64 | Number of paid records |
| `records_already_paid` | uint64 | Number of already-paid records |
| `tokens_spent` | string | Tokens spent |

## Common messages

The current proto files define these shared shapes:

| Message | Fields |
|------|--------|
| `Cost` | `atto_tokens` |
| `HealthCheckResponse` | `status`, `network` |
| `PutPublicDataResponse` | `cost`, `address` |
| `PutPrivateDataResponse` | `cost`, `data_map` |
| `UploadPublicResponse` | `cost`, `address` |

## Related pages

- [REST API](rest-api.md)
- [ant-sdk Overview](overview.md)
- [How Language Bindings Work](language-bindings/overview.md)
