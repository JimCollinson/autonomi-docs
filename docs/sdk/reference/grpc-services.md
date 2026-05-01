# gRPC Services

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: d7652ec3da82dfbe2107778e5223dc413d95815b
  verified_date: 2026-04-30
  verification_mode: current-merged-truth
-->

This page describes the gRPC surface exposed by `antd` on `localhost:50051` by default.

Unlike the REST API, the gRPC API carries raw bytes in protobuf fields rather than base64 strings in JSON.

## Health Service

### Check

**Signature:** `Check(HealthCheckRequest) -> HealthCheckResponse`

Checks daemon health and network selection.

**Response fields:**

| Name | Type | Description |
|------|------|-------------|
| `status` | string | Expected `ok` on success |
| `network` | string | Current network name |

## Data Service

### Get Public

**Signature:** `GetPublic(GetPublicDataRequest) -> GetPublicDataResponse`

Fetches public data by address.

### Put Public

**Signature:** `PutPublic(PutPublicDataRequest) -> PutPublicDataResponse`

Stores public data.

### Stream Public

**Signature:** `StreamPublic(StreamPublicDataRequest) -> stream DataChunk`

This RPC is exposed, but the handler returns `UNIMPLEMENTED`.

### Get Private

**Signature:** `GetPrivate(GetPrivateDataRequest) -> GetPrivateDataResponse`

Fetches private data using a `data_map` string.

### Put Private

**Signature:** `PutPrivate(PutPrivateDataRequest) -> PutPrivateDataResponse`

Stores private data and returns a `data_map` string.

### Get Cost

**Signature:** `GetCost(DataCostRequest) -> Cost`

Estimates storage cost for a byte payload.

## Chunk Service

### Get

**Signature:** `Get(GetChunkRequest) -> GetChunkResponse`

Fetches a chunk by address.

### Put

**Signature:** `Put(PutChunkRequest) -> PutChunkResponse`

Stores a raw chunk.

## File Service

### Upload Public

**Signature:** `UploadPublic(UploadFileRequest) -> UploadPublicResponse`

Uploads a local file path.

`UploadPublicResponse` returns `address`, `storage_cost_atto`, `gas_cost_wei`, `chunks_stored`, and `payment_mode_used`.

### Download Public

**Signature:** `DownloadPublic(DownloadPublicRequest) -> DownloadResponse`

Downloads a public file to a local destination path.

### Upload Public Directory

**Signature:** `DirUploadPublic(UploadFileRequest) -> UploadPublicResponse`

Uploads a local directory path.

`DirUploadPublic` returns the same `UploadPublicResponse` shape as file uploads.

### Download Public Directory

**Signature:** `DirDownloadPublic(DownloadPublicRequest) -> DownloadResponse`

Downloads a public directory to a local destination path.

### Get File Cost

**Signature:** `GetFileCost(FileCostRequest) -> Cost`

Estimates file upload cost.

## Event Service

### Subscribe

**Signature:** `Subscribe(SubscribeRequest) -> stream ClientEventProto`

This RPC is exposed, but the stream stays open without emitting events.

`ClientEventProto` includes:

| Name | Type | Description |
|------|------|-------------|
| `kind` | string | Event kind |
| `records_paid` | uint64 | Number of paid records |
| `records_already_paid` | uint64 | Number of already-paid records |
| `tokens_spent` | string | Tokens spent |

## Common messages

The proto files define these shared shapes:

| Message | Fields |
|------|--------|
| `Cost` | `atto_tokens` |
| `HealthCheckResponse` | `status`, `network` |
| `PutPublicDataResponse` | `cost`, `address` |
| `PutPrivateDataResponse` | `cost`, `data_map` |
| `UploadPublicResponse` | `address`, `storage_cost_atto`, `gas_cost_wei`, `chunks_stored`, `payment_mode_used` |

## Related pages

- [REST API](rest-api.md)
- [SDK Overview](overview.md)
- [How Language Bindings Work](language-bindings/overview.md)
