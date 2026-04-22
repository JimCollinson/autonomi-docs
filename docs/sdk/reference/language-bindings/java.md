# Java SDK

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: bf541ccd4ae1fd3e174fb7b5bb21deef38d999ce
  verified_date: 2026-04-21
  verification_mode: current-merged-truth
-->

The Java SDK talks to `antd` over REST by default and also exposes async and gRPC clients.

## Install

```kotlin
dependencies {
    implementation("com.autonomi:antd-java:0.1.0")
}
```

## Connect to the daemon

```java
import com.autonomi.antd.AntdClient;

try (var client = new AntdClient()) {
    var health = client.health();
    System.out.println(health.network());
}
```

The SDK also provides `AsyncAntdClient` and `GrpcAntdClient`.

## Store and retrieve data

```java
import com.autonomi.antd.AntdClient;

public class QuickStart {
    public static void main(String[] args) throws Exception {
        try (var client = new AntdClient()) {
            var result = client.dataPutPublic("Hello, Autonomi!".getBytes());
            System.out.println(result.address());

            byte[] data = client.dataGetPublic(result.address());
            System.out.println(new String(data));
        }
    }
}
```

## Type mappings

| Autonomi type | Java type |
|------|------|
| `HealthStatus` | `com.autonomi.antd.models.HealthStatus` |
| `PutResult` | `com.autonomi.antd.models.PutResult` |
| Raw data | `byte[]` |

## Error handling

```java
try {
    byte[] data = client.dataGetPublic("bad-address");
} catch (com.autonomi.antd.NotFoundException e) {
    System.out.println("Data not found");
} catch (com.autonomi.antd.PaymentException e) {
    System.out.println("Insufficient funds");
} catch (com.autonomi.antd.AntdException e) {
    System.out.println(e.getMessage());
}
```

## Full API reference

For all available daemon endpoints, see the [REST API](../rest-api.md).
