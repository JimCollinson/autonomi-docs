# Your First Upload

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: 6c4df9b745f3adcb022ac82b6bbc485727297e3e
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->

This page stores a small public payload with the current merged `antd` daemon and reads it back. By the end, you will have a working upload/download round-trip through the live daemon surface.

## Prerequisites

- `antd` installed and running on `http://localhost:8082` (see [Install antd](install.md))
- For write operations: start `antd` with `AUTONOMI_WALLET_KEY` set, or use `ant dev start` for a local devnet
- Optional: Python or JavaScript runtime if you want to use those SDK tabs

## Steps

### 1. Check the daemon is healthy

{% tabs %}
{% tab title="cURL" %}
```bash
curl http://localhost:8082/health
```
{% endtab %}
{% tab title="Python" %}
```python
from antd import AntdClient

client = AntdClient()
status = client.health()

print(status.network)
print(status.ok)
```
{% endtab %}
{% tab title="JavaScript" %}
```javascript
import { createClient } from "antd";

async function main() {
  const client = createClient();
  const status = await client.health();
  console.log(status.network);
  console.log(status.ok);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
```
{% endtab %}
{% endtabs %}

Expected REST response:

```json
{
  "status": "ok",
  "network": "default"
}
```

### 2. Store a public payload

The REST API expects binary data as base64 inside JSON.

{% tabs %}
{% tab title="cURL" %}
```bash
DATA_B64=$(printf 'Hello, Autonomi!' | base64)

curl -X POST http://localhost:8082/v1/data/public \
  -H "Content-Type: application/json" \
  -d "{\"data\":\"$DATA_B64\"}"
```
{% endtab %}
{% tab title="Python" %}
```python
from antd import AntdClient

client = AntdClient()
result = client.data_put_public(b"Hello, Autonomi!")

print(result.address)
```
{% endtab %}
{% tab title="JavaScript" %}
```javascript
import { createClient } from "antd";

async function main() {
  const client = createClient();
  const result = await client.dataPutPublic(Buffer.from("Hello, Autonomi!"));
  console.log(result.address);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
```
{% endtab %}
{% endtabs %}

Expected REST response shape:

```json
{
  "address": "<64_hex_address>",
  "chunks_stored": <chunk_count>,
  "payment_mode_used": "auto"
}
```

Save the returned address.

### 3. Retrieve the payload

{% tabs %}
{% tab title="cURL" %}
```bash
curl http://localhost:8082/v1/data/public/<address>
```
{% endtab %}
{% tab title="Python" %}
```python
from antd import AntdClient

client = AntdClient()
data = client.data_get_public("<address>")

print(data.decode())
```
{% endtab %}
{% tab title="JavaScript" %}
```javascript
import { createClient } from "antd";

async function main() {
  const client = createClient();
  const data = await client.dataGetPublic("<address>");
  console.log(data.toString());
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
```
{% endtab %}
{% endtabs %}

Expected REST response shape:

```json
{
  "data": "SGVsbG8sIEF1dG9ub21pIQ=="
}
```

The REST `data` field is base64-encoded. The Python and JavaScript SDKs decode it for you.

### 4. Verify the round-trip

{% tabs %}
{% tab title="Python" %}
```python
from antd import AntdClient

client = AntdClient()
original = b"Hello, Autonomi!"
result = client.data_put_public(original)
retrieved = client.data_get_public(result.address)

assert retrieved == original
print(result.address)
```
{% endtab %}
{% tab title="JavaScript" %}
```javascript
import assert from "node:assert/strict";
import { createClient } from "antd";

async function main() {
  const client = createClient();
  const original = Buffer.from("Hello, Autonomi!");
  const result = await client.dataPutPublic(original);
  const retrieved = await client.dataGetPublic(result.address);

  assert.deepEqual(retrieved, original);
  console.log(result.address);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
```
{% endtab %}
{% endtabs %}

## What happened

`antd` accepted your payload, encrypted and chunked it internally, stored the resulting data on the network, then returned the network address used to fetch it again. The REST API represents binary payloads as base64 inside JSON, while the current Python and JavaScript SDKs decode those values back into bytes for you.

## Next steps

- [Store and Retrieve Data](../how-to-guides/store-and-retrieve-data.md)
- [REST API](../sdk-reference/rest-api.md)
- [ant-sdk Overview](../sdk-reference/overview.md)
