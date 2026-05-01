# MCP Server Reference

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: d7652ec3da82dfbe2107778e5223dc413d95815b
  verified_date: 2026-04-30
  verification_mode: current-merged-truth
-->

Reference for the `antd-mcp` server that exposes the `antd` daemon as MCP tools for AI agents and MCP-compatible clients.

## Server command

### Main command

**Command:** `antd-mcp`

Runs the MCP server in stdio mode by default.

### SSE mode

**Command:** `antd-mcp --sse`

Runs the MCP server in SSE mode for web-based clients.

## Installation

Use this setup:

```bash
pip install "antd[rest]"
pip install -e antd-mcp/
```

Run the editable install from an `ant-sdk` checkout root.

The package metadata declares:

- Python `>=3.10`
- dependency on `mcp>=1.2.0`
- dependency on `antd>=0.1.0`

## Configuration

### Environment variables

| Variable | Required | Description |
|------|----------|-------------|
| `ANTD_BASE_URL` | No | Overrides daemon auto-discovery and points the MCP server at a specific `antd` REST URL |

### Daemon discovery order

At startup, the server resolves the daemon base URL in this order:

1. `ANTD_BASE_URL`
2. `daemon.port` discovery
3. `http://127.0.0.1:8082`

The discovery helper still checks a `daemon.port` file before falling back to the default URL.

`antd` writes `ant/sdk/daemon.port`, while `antd-mcp` reads `ant/daemon.port`. Treat `ANTD_BASE_URL` as the reliable configuration path unless you have already confirmed port-file discovery works in your environment.

## Claude Desktop configuration

```json
{
  "mcpServers": {
    "antd-autonomi": {
      "command": "antd-mcp",
      "env": {
        "ANTD_BASE_URL": "http://127.0.0.1:8082"
      }
    }
  }
}
```

Adjust `ANTD_BASE_URL` if your daemon runs on a different host or port.

## Data tools

### Store Data

**Tool:** `store_data(text, private=false, payment_mode="auto")`

Stores text on the network as public or private data.

### Retrieve Data

**Tool:** `retrieve_data(address, private=false)`

Retrieves text from the network by address or DataMap.

### Upload a File

**Tool:** `upload_file(path, is_directory=false, payment_mode="auto")`

Uploads a local file or directory as public content.

### Download a File

**Tool:** `download_file(address, dest_path, is_directory=false)`

Downloads a public file or directory to a local path.

### Estimate Cost

**Tool:** `get_cost(text=None, file_path=None)`

Estimates storage cost for text or a local file path.

Provide exactly one of `text` or `file_path`.

### Check Health

**Tool:** `check_health()`

Checks daemon health and returns the current network name.

## Wallet tools

### Get Wallet Address

**Tool:** `wallet_address()`

Returns the wallet public address configured in the daemon.

### Get Wallet Balance

**Tool:** `wallet_balance()`

Returns token and gas balances from the daemon.

### Approve Wallet Spend

**Tool:** `wallet_approve()`

Approves token spend on payment contracts.

## Chunk tools

### Store a Chunk

**Tool:** `chunk_put(data)`

Stores a raw chunk. The input is base64-encoded.

### Get a Chunk

**Tool:** `chunk_get(address)`

Fetches a raw chunk and returns base64-encoded data.

## External-signer tools

### Prepare a File Upload

**Tool:** `prepare_upload(path)`

Prepares a file upload for external signing and returns payment details plus a `payment_type` discriminator.

### Prepare a Data Upload

**Tool:** `prepare_data_upload(data)`

Prepares a data upload for external signing. The input is base64-encoded.

Both prepare tools return either:

- `payment_type: "wave_batch"` with quote-level `payments`
- `payment_type: "merkle"` with `depth`, `pool_commitments`, `merkle_payment_timestamp`, and `payment_vault_address`

### Finalize a Wave-Batch Upload

**Tool:** `finalize_upload(upload_id, tx_hashes)`

Finalizes an externally-signed upload when the prepare step returned `payment_type: "wave_batch"`.

### Finalize a Merkle Upload

**Tool:** `finalize_merkle_upload(upload_id, winner_pool_hash)`

Finalizes an externally-signed upload when the prepare step returned `payment_type: "merkle"`.

## Payment modes

The server accepts the same daemon payment mode strings for the tools that upload content:

| Mode | Description |
|------|-------------|
| `auto` | Default mode |
| `merkle` | Force Merkle batch payment |
| `single` | Force per-chunk payments |

## Success and error responses

Successful tool responses are JSON and always include a `network` field.

Examples:

```json
{
  "healthy": true,
  "network": "local"
}
```

Example `upload_file(..., is_directory=true)` response:

```json
{
  "address": "abc123...",
  "storage_cost_atto": "1000000",
  "gas_cost_wei": "42000000000000",
  "chunks_stored": 7,
  "payment_mode_used": "auto",
  "network": "local"
}
```

Example `store_data` response:

```json
{
  "address": "abc123...",
  "cost": "1000000",
  "network": "local"
}
```

Structured `AntdError` responses include:

| Field | Description |
|------|-------------|
| `error` | Normalized error code such as `NOT_FOUND`, `BAD_REQUEST`, or `PAYMENT_FAILED` |
| `message` | Human-readable message |
| `status_code` | Daemon HTTP status code |
| `network` | Connected network |

Unexpected errors include `error`, `message`, and `network`, but may not include `status_code`.

## Upstream sources

- [ant-sdk](https://github.com/WithAutonomi/ant-sdk)

## Related pages

- [How to Use the MCP Server](use-the-autonomi-mcp-server.md)
- [SDK Overview](../sdk/reference/overview.md)
- [REST API](../sdk/reference/rest-api.md)
