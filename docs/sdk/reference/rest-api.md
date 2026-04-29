# REST API

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: 1cbfb3e92cb4309f29e92b5609837812027f0a67
  verified_date: 2026-04-29
  verification_mode: current-merged-truth
-->

This page describes the REST surface exposed by `antd`. By default, the daemon listens on `http://localhost:8082`.

All current REST payloads are JSON. When you send or receive binary data, the bytes are base64-encoded inside a `data` field.

## Health

### Health Check

**Endpoint:** `GET /health`

Returns daemon health and the selected network.

**Response:**

```json
{
  "status": "ok",
  "network": "default"
}
```

**Example:**

```bash
curl http://localhost:8082/health
```

## Data

### Store Public Data

**Endpoint:** `POST /v1/data/public`

Stores public data and returns the public address that can be shared with readers.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `data` | string | Yes | Base64-encoded payload |
| `payment_mode` | string | No | `auto`, `merkle`, or `single` |

**Response:**

```json
{
  "address": "<64_hex_address>",
  "chunks_stored": <chunk_count>,
  "payment_mode_used": "auto"
}
```

**Example:**

```bash
DATA_B64=$(printf 'Hello, Autonomi!' | base64)

curl -X POST http://localhost:8082/v1/data/public \
  -H "Content-Type: application/json" \
  -d "{\"data\":\"$DATA_B64\"}"
```

### Get Public Data

**Endpoint:** `GET /v1/data/public/{addr}`

Fetches public data by address.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `addr` | path | Yes | 64-character hex data address |

**Response:**

```json
{
  "data": "SGVsbG8sIEF1dG9ub21pIQ=="
}
```

**Example:**

```bash
curl http://localhost:8082/v1/data/public/<addr>
```

### Stream Public Data

**Endpoint:** `GET /v1/data/public/{addr}/stream`

Current merged code exposes this streaming endpoint, but the handler is still a stub at this commit and currently returns an empty SSE stream.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `addr` | path | Yes | 64-character hex data address |

**Example:**

```bash
curl -N http://localhost:8082/v1/data/public/<addr>/stream
```

### Store Private Data

**Endpoint:** `POST /v1/data/private`

Stores private data and returns a serialized DataMap instead of a public address.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `data` | string | Yes | Base64-encoded payload |
| `payment_mode` | string | No | `auto`, `merkle`, or `single` |

**Response:**

```json
{
  "data_map": "<hex_encoded_datamap>",
  "chunks_stored": <chunk_count>,
  "payment_mode_used": "auto"
}
```

**Example:**

```bash
DATA_B64=$(printf 'Secret message' | base64)

curl -X POST http://localhost:8082/v1/data/private \
  -H "Content-Type: application/json" \
  -d "{\"data\":\"$DATA_B64\"}"
```

### Get Private Data

**Endpoint:** `GET /v1/data/private`

Retrieves private data using the returned DataMap.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `data_map` | query | Yes | Hex-encoded serialized DataMap |

**Response:**

```json
{
  "data": "U2VjcmV0IG1lc3NhZ2U="
}
```

**Example:**

```bash
curl "http://localhost:8082/v1/data/private?data_map=<hex_encoded_datamap>"
```

### Estimate Data Cost

**Endpoint:** `POST /v1/data/cost`

Estimates the storage cost for a data payload without uploading it.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `data` | string | Yes | Base64-encoded payload |

**Response:**

```json
{
  "cost": "<atto_token_amount>",
  "file_size": <bytes>,
  "chunk_count": <chunk_count>,
  "estimated_gas_cost_wei": "<wei_amount>",
  "payment_mode": "auto"
}
```

**Example:**

```bash
DATA_B64=$(printf 'Hello, Autonomi!' | base64)

curl -X POST http://localhost:8082/v1/data/cost \
  -H "Content-Type: application/json" \
  -d "{\"data\":\"$DATA_B64\"}"
```

## Chunks

### Store a Chunk

**Endpoint:** `POST /v1/chunks`

Stores a raw chunk.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `data` | string | Yes | Base64-encoded chunk bytes |

**Response:**

```json
{
  "cost": "<atto_token_amount>",
  "address": "<64_hex_address>"
}
```

**Example:**

```bash
CHUNK_B64=$(printf 'chunk bytes' | base64)

curl -X POST http://localhost:8082/v1/chunks \
  -H "Content-Type: application/json" \
  -d "{\"data\":\"$CHUNK_B64\"}"
```

### Get a Chunk

**Endpoint:** `GET /v1/chunks/{addr}`

Retrieves a raw chunk by address.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `addr` | path | Yes | 64-character hex chunk address |

**Response:**

```json
{
  "data": "Y2h1bmsgYnl0ZXM="
}
```

**Example:**

```bash
curl http://localhost:8082/v1/chunks/<addr>
```

## Files and directories

These endpoints work on paths visible to the machine running `antd`.

### Upload a Public File

**Endpoint:** `POST /v1/files/upload/public`

Uploads a local file and stores its DataMap publicly.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `path` | string | Yes | Local file path |
| `payment_mode` | string | No | `auto`, `merkle`, or `single` |

**Response:**

```json
{
  "address": "<64_hex_address>",
  "storage_cost_atto": "<atto_token_amount>",
  "gas_cost_wei": "<wei_amount>",
  "chunks_stored": 42,
  "payment_mode_used": "auto"
}
```

**Example:**

```bash
curl -X POST http://localhost:8082/v1/files/upload/public \
  -H "Content-Type: application/json" \
  -d '{"path":"/absolute/path/to/document.pdf"}'
```

### Download a Public File

**Endpoint:** `POST /v1/files/download/public`

Downloads a file to a local destination path.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | string | Yes | 64-character hex file address |
| `dest_path` | string | Yes | Local destination path |

**Response:** HTTP `200 OK` with no JSON body

**Example:**

```bash
curl -X POST http://localhost:8082/v1/files/download/public \
  -H "Content-Type: application/json" \
  -d '{"address":"<64_hex_address>","dest_path":"/absolute/path/to/downloaded.pdf"}'
```

### Upload a Public Directory

**Endpoint:** `POST /v1/dirs/upload/public`

Uploads a local directory recursively.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `path` | string | Yes | Local directory path |
| `payment_mode` | string | No | `auto`, `merkle`, or `single` |

**Response:**

```json
{
  "address": "<64_hex_address>",
  "storage_cost_atto": "<atto_token_amount>",
  "gas_cost_wei": "<wei_amount>",
  "chunks_stored": 42,
  "payment_mode_used": "auto"
}
```

**Example:**

```bash
curl -X POST http://localhost:8082/v1/dirs/upload/public \
  -H "Content-Type: application/json" \
  -d '{"path":"/absolute/path/to/my-folder"}'
```

### Download a Public Directory

**Endpoint:** `POST /v1/dirs/download/public`

Downloads a directory to a local destination path.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | string | Yes | 64-character hex directory address |
| `dest_path` | string | Yes | Local destination path |

**Response:** HTTP `200 OK` with no JSON body

**Example:**

```bash
curl -X POST http://localhost:8082/v1/dirs/download/public \
  -H "Content-Type: application/json" \
  -d '{"address":"<64_hex_address>","dest_path":"/absolute/path/to/output-folder"}'
```

### Estimate File Cost

**Endpoint:** `POST /v1/files/cost`

Estimates upload cost for a local file.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `path` | string | Yes | Local file path |
| `is_public` | boolean | No | Defaults to `true` |

**Response:**

```json
{
  "cost": "<atto_token_amount>",
  "file_size": <bytes>,
  "chunk_count": <chunk_count>,
  "estimated_gas_cost_wei": "<wei_amount>",
  "payment_mode": "auto"
}
```

**Example:**

```bash
curl -X POST http://localhost:8082/v1/files/cost \
  -H "Content-Type: application/json" \
  -d '{"path":"/absolute/path/to/document.pdf","is_public":true}'
```

## Wallet

### Get Wallet Address

**Endpoint:** `GET /v1/wallet/address`

Returns the configured wallet address.

**Response:**

```json
{
  "address": "0x1234abcd..."
}
```

**Example:**

```bash
curl http://localhost:8082/v1/wallet/address
```

### Get Wallet Balance

**Endpoint:** `GET /v1/wallet/balance`

Returns token and gas balances.

**Response:**

```json
{
  "balance": "<atto_token_balance>",
  "gas_balance": "<wei_balance>"
}
```

**Example:**

```bash
curl http://localhost:8082/v1/wallet/balance
```

### Approve Wallet Spend

**Endpoint:** `POST /v1/wallet/approve`

Approves token spend for payment contracts.

**Parameters:** None

**Response:**

```json
{
  "approved": true
}
```

**Example:**

```bash
curl -X POST http://localhost:8082/v1/wallet/approve \
  -H "Content-Type: application/json" \
  -d '{}'
```

## External signer flow

### Prepare a Data Upload

**Endpoint:** `POST /v1/data/prepare`

Prepares an in-memory data upload for external signing.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `data` | string | Yes | Base64-encoded payload |

**Response:**

The response varies by `payment_type`.

The daemon returns `wave_batch` for uploads under 64 chunks and `merkle` for uploads with 64 or more chunks.

```json
{
  "upload_id": "<hex_id>",
  "payment_type": "wave_batch",
  "payments": [
    {
      "quote_hash": "0x...",
      "rewards_address": "0x...",
      "amount": "<atto_token_amount>"
    }
  ],
  "total_amount": "<atto_token_amount>",
  "payment_vault_address": "0x...",
  "payment_token_address": "0x...",
  "rpc_url": "http://127.0.0.1:8545"
}
```

Merkle variant:

```json
{
  "upload_id": "<hex_id>",
  "payment_type": "merkle",
  "depth": 6,
  "pool_commitments": [
    {
      "pool_hash": "0x...",
      "candidates": [
        {
          "rewards_address": "0x...",
          "amount": "<atto_token_amount>"
        }
      ]
    }
  ],
  "merkle_payment_timestamp": 1744041600,
  "payment_vault_address": "0x...",
  "total_amount": "0",
  "payment_token_address": "0x...",
  "rpc_url": "http://127.0.0.1:8545"
}
```

Each `pool_commitments` entry contains exactly 16 candidate payments. The example above shows one candidate for brevity.

**Example:**

```bash
DATA_B64=$(printf 'Hello, Autonomi!' | base64)

curl -X POST http://localhost:8082/v1/data/prepare \
  -H "Content-Type: application/json" \
  -d "{\"data\":\"$DATA_B64\"}"
```

### Prepare a File Upload

**Endpoint:** `POST /v1/upload/prepare`

Prepares a file upload for external signing.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `path` | string | Yes | Local file path |

**Response:** Same `payment_type`-based shape as `POST /v1/data/prepare`

**Example:**

```bash
curl -X POST http://localhost:8082/v1/upload/prepare \
  -H "Content-Type: application/json" \
  -d '{"path":"/absolute/path/to/document.pdf"}'
```

### Finalize an Upload

**Endpoint:** `POST /v1/upload/finalize`

Finalizes a prepared upload after the external signer has submitted the matching payment transaction.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `upload_id` | string | Yes | Value returned by a prepare endpoint |
| `tx_hashes` | object | No | Wave-batch only: map of `quote_hash` to `tx_hash` |
| `winner_pool_hash` | string | No | Merkle only: winner pool hash emitted by `MerklePaymentMade` |
| `store_data_map` | boolean | No | If `true`, also stores the DataMap on-network |

Provide `tx_hashes` when the prepare response returned `payment_type: "wave_batch"`. Provide `winner_pool_hash` when it returned `payment_type: "merkle"`.

**Response:**

```json
{
  "data_map": "<hex_encoded_datamap>",
  "address": "<64_hex_address>",
  "chunks_stored": <chunk_count>
}
```

The `address` field is only present when `store_data_map` is `true`.

**Examples:**

```bash
curl -X POST http://localhost:8082/v1/upload/finalize \
  -H "Content-Type: application/json" \
  -d '{"upload_id":"<hex_id>","tx_hashes":{"0xquote":"0xtx"},"store_data_map":true}'
```

```bash
curl -X POST http://localhost:8082/v1/upload/finalize \
  -H "Content-Type: application/json" \
  -d '{"upload_id":"<hex_id>","winner_pool_hash":"0x...","store_data_map":true}'
```

## Error codes

| Code | Meaning | Resolution |
|------|---------|------------|
| `400` | Bad request | Check base64 encoding, address length, data map format, and local paths |
| `402` | Payment required | Fund the configured wallet or reduce the upload size |
| `404` | Not found | Check the address or `upload_id` |
| `413` | Payload too large | Split the upload or switch to file/directory endpoints |
| `500` | Internal server error | Check daemon logs and retry |
| `502` | Network unreachable | Confirm the daemon can reach the Autonomi network |
| `503` | Service unavailable | Configure a wallet before calling wallet or write endpoints |

## Related pages

- [Build with the SDKs](../install.md)
- [Start the Local Daemon](../start-the-local-daemon.md)
- [Store Data on the Network](../store-data-on-the-network.md)
- [Store and Retrieve Data with the SDKs](../how-to-guides/store-and-retrieve-data.md)
