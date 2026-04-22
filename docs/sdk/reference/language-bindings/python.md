# Python SDK

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: bf541ccd4ae1fd3e174fb7b5bb21deef38d999ce
  verified_date: 2026-04-21
  verification_mode: current-merged-truth
-->

The Python SDK is the Python client for the `antd` daemon.

## Install

```bash
pip install antd[rest]
pip install antd[grpc]
pip install antd[all]
```

## Connect to the daemon

```python
from antd import AntdClient, AsyncAntdClient, discover_daemon_url

# REST transport by default
client = AntdClient()

# Async REST client
async_client = AsyncAntdClient()

# Explicit gRPC transport
grpc_client = AntdClient(transport="grpc", target="localhost:50051")

# Use discovery helpers if antd chose a non-default port
base_url = discover_daemon_url() or "http://localhost:8082"
discovered_client = AntdClient(base_url=base_url)
```

## Store and retrieve data

```python
from antd import AntdClient

client = AntdClient()
status = client.health()
assert status.ok

result = client.data_put_public(b"Hello from Python!")
print(result.address)

data = client.data_get_public(result.address)
assert data == b"Hello from Python!"
print(data.decode())
```

## Type mappings

| Autonomi type | Python type |
|------|------|
| `HealthStatus` | `antd.HealthStatus` |
| `PutResult` | `antd.PutResult` |
| `WalletAddress` | `antd.WalletAddress` |
| `WalletBalance` | `antd.WalletBalance` |
| `PrepareUploadResult` | `antd.PrepareUploadResult` |
| `FinalizeUploadResult` | `antd.FinalizeUploadResult` |
| Raw data | `bytes` |

## Error handling

```python
from antd import AntdClient, AntdError, NotFoundError, PaymentError

client = AntdClient()

try:
    client.data_get_public("nonexistent_address")
except NotFoundError:
    print("Data not found")
except PaymentError:
    print("Insufficient funds")
except AntdError as error:
    print(error)
```

REST and gRPC share the same high-level API, but wallet operations and `payment_mode` are REST-only.

## Full API reference

For all available daemon endpoints, see the [REST API](../rest-api.md).
