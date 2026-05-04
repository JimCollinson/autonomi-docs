# Swift SDK

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: d7652ec3da82dfbe2107778e5223dc413d95815b
  verified_date: 2026-05-02
  verification_mode: current-merged-truth
-->

The Swift SDK is a macOS-oriented REST/gRPC client for the `antd` daemon.

## Install

```swift
dependencies: [
    .package(path: "../ant-sdk/antd-swift"),
]
```

Use a local package dependency until the package is published.

## Connect to the daemon

```swift
import AntdSdk

let client = AntdClient.createRest(baseURL: "http://localhost:8082")
let status = try await client.health()
print(status.network)
```

## Store and retrieve data

```swift
import AntdSdk

let client = AntdClient.createRest()
let result = try await client.dataPutPublic("Hello, Autonomi!".data(using: .utf8)!)
print(result.address)

let data = try await client.dataGetPublic(address: result.address)
print(String(data: data, encoding: .utf8)!)
```

## Type mappings

| Autonomi type | Swift type |
|------|------|
| `HealthStatus` | Swift model type |
| `PutResult` | Swift model type |
| Raw data | `Data` |

## Error handling

```swift
do {
    let data = try await client.dataGetPublic(address: "nonexistent")
    _ = data
} catch let error as NotFoundError {
    print(error.message)
} catch let error as PaymentError {
    print(error.message)
} catch let error as AntdError {
    print(error.message)
}
```

## Full API reference

For all available daemon endpoints, see the [REST API](../rest-api.md).
