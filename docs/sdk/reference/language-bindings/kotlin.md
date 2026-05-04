# Kotlin SDK

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: d7652ec3da82dfbe2107778e5223dc413d95815b
  verified_date: 2026-05-02
  verification_mode: current-merged-truth
-->

The Kotlin SDK targets the `antd` daemon over REST or gRPC.

## Install

```kotlin
dependencies {
    implementation("com.autonomi:antd-kotlin:0.1.0")
}
```

Until the package is published, use the project as a local dependency or composite build.

## Connect to the daemon

```kotlin
import com.autonomi.sdk.*
import kotlinx.coroutines.runBlocking

fun main() = runBlocking {
    val client = AntdClient.createRest("http://localhost:8082")
    val status = client.health()
    println(status.network)
    client.close()
}
```

## Store and retrieve data

```kotlin
import com.autonomi.sdk.*
import kotlinx.coroutines.runBlocking

fun main() = runBlocking {
    val client = AntdClient.createRest()
    val result = client.dataPutPublic("Hello, Autonomi!".toByteArray())
    println(result.address)

    val data = client.dataGetPublic(result.address)
    println(String(data))
    client.close()
}
```

## Type mappings

| Autonomi type | Kotlin type |
|------|------|
| `HealthStatus` | Kotlin data class |
| `PutResult` | Kotlin data class |
| Raw data | `ByteArray` |

## Error handling

```kotlin
try {
    val data = client.dataGetPublic("nonexistent")
} catch (e: NotFoundException) {
    println("Not found")
} catch (e: PaymentException) {
    println("Payment required")
} catch (e: AntdException) {
    println(e.message)
}
```

## Full API reference

For all available daemon endpoints, see the [REST API](../rest-api.md).
