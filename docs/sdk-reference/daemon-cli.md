# Daemon CLI: antd

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: 6c4df9b745f3adcb022ac82b6bbc485727297e3e
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->

Reference for the `antd` command-line interface.

## Usage

### `antd`

Runs the local REST and gRPC gateway daemon for Autonomi.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `--rest-addr <ADDR>` | string | No | REST listen address, default `0.0.0.0:8082` |
| `--grpc-addr <ADDR>` | string | No | gRPC listen address, default `0.0.0.0:50051` |
| `--rest-port <PORT>` | integer | No | Override the REST port from `--rest-addr` |
| `--grpc-port <PORT>` | integer | No | Override the gRPC port from `--grpc-addr` |
| `--network <MODE>` | string | No | Network mode, default `default`; also supports `local` |
| `--peers <MULTIADDRS>` | string | No | Comma-separated bootstrap peer multiaddrs |
| `--cors` | boolean | No | Enable localhost CORS headers |
| `--log-level <LEVEL>` | string | No | Log level: `trace`, `debug`, `info`, `warn`, `error` |

**Environment variables:**

| Variable | Description |
|------|------|
| `ANTD_REST_ADDR` | REST listen address |
| `ANTD_GRPC_ADDR` | gRPC listen address |
| `ANTD_REST_PORT` | REST port override |
| `ANTD_GRPC_PORT` | gRPC port override |
| `ANTD_NETWORK` | Network mode |
| `ANTD_PEERS` | Comma-separated bootstrap peer multiaddrs |
| `ANTD_CORS` | Enable CORS |
| `ANTD_LOG_LEVEL` | Log level |
| `AUTONOMI_WALLET_KEY` | Direct-wallet private key for paid uploads |
| `EVM_RPC_URL` | EVM RPC endpoint |
| `EVM_PAYMENT_TOKEN_ADDRESS` | Payment token contract |
| `EVM_DATA_PAYMENTS_ADDRESS` | Data payments contract |
| `EVM_MERKLE_PAYMENTS_ADDRESS` | Optional Merkle payments contract |

**Examples:**

```bash
# Default network, default ports
antd

# Local network with explicit peers
ANTD_PEERS="/ip4/127.0.0.1/udp/12000/quic-v1/p2p/12D3Koo..." antd --network local

# Bind to localhost only
antd --rest-addr 127.0.0.1:8082 --grpc-addr 127.0.0.1:50051

# Let the OS assign free ports
antd --rest-port 0 --grpc-port 0

# Run with debug logging
antd --log-level debug
```

**Response:** None. The daemon keeps running until it is stopped.

## Notes

- The CLI does not include an `--external-signer` flag.
- External-signer mode is handled through environment configuration and the prepare/finalize upload endpoints.
- On startup, `antd` writes a `daemon.port` file so SDKs can discover the active ports.

## Error codes

| Code | Meaning | Resolution |
|------|---------|------------|
| invalid REST address | `--rest-addr` could not be parsed | Fix the host:port value |
| invalid gRPC address | `--grpc-addr` could not be parsed | Fix the host:port value |
| runtime wallet/config errors | Required env vars are missing for paid operations | Set the wallet and EVM environment variables |

## Related pages

- [Build with the SDKs](../getting-started/install.md)
- [Use antd as a Local Service](../how-to-guides/run-as-daemon.md)
- [REST API](rest-api.md)
