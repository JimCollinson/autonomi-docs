# Go SDK

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: d7652ec3da82dfbe2107778e5223dc413d95815b
  verified_date: 2026-05-02
  verification_mode: current-merged-truth
-->

The Go SDK is the Go client for the `antd` daemon.

## Install

```bash
go get github.com/WithAutonomi/ant-sdk/antd-go
```

## Connect to the daemon

```go
package main

import (
    "context"
    "fmt"

    antd "github.com/WithAutonomi/ant-sdk/antd-go"
)

func main() {
    client := antd.NewClient(antd.DefaultBaseURL)
    ctx := context.Background()

    health, err := client.Health(ctx)
    if err != nil {
        panic(err)
    }
    fmt.Println(health.OK)

    discoveredClient, url := antd.NewClientAutoDiscover()
    _ = discoveredClient
    fmt.Println(url)
}
```

The SDK also includes a `GrpcClient` for the daemon's gRPC endpoint.

## Store and retrieve data

For upload examples in this section, start `antd` in a write-enabled mode first. On the default network, that means wallet plus EVM payment configuration. On a local devnet, `ant dev start` provisions that for you.

```go
package main

import (
    "context"
    "fmt"
    "log"

    antd "github.com/WithAutonomi/ant-sdk/antd-go"
)

func main() {
    client := antd.NewClient(antd.DefaultBaseURL)
    ctx := context.Background()

    result, err := client.DataPutPublic(ctx, []byte("Hello from Go!"))
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println(result.Address)

    data, err := client.DataGetPublic(ctx, result.Address)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println(string(data))
}
```

## Type mappings

| Autonomi type | Go type |
|------|------|
| `HealthStatus` | `antd.HealthStatus` |
| `PutResult` | `antd.PutResult` |
| `WalletAddress` | `antd.WalletAddress` |
| `WalletBalance` | `antd.WalletBalance` |
| `PrepareUploadResult` | `antd.PrepareUploadResult` |
| `FinalizeUploadResult` | `antd.FinalizeUploadResult` |
| Raw data | `[]byte` |

## Error handling

```go
package main

import (
    "context"
    "errors"
    "fmt"

    antd "github.com/WithAutonomi/ant-sdk/antd-go"
)

func main() {
    client := antd.NewClient(antd.DefaultBaseURL)
    _, err := client.DataGetPublic(context.Background(), "nonexistent_address")
    if err != nil {
        var notFound *antd.NotFoundError
        if errors.As(err, &notFound) {
            fmt.Println("Data not found")
            return
        }
        fmt.Println(err)
    }
}
```

## Full API reference

For all available daemon endpoints, see the [REST API](../rest-api.md).
