# Handle Payments

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: 6c4df9b745f3adcb022ac82b6bbc485727297e3e
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->

Use the current merged wallet and cost endpoints in `antd` to check balances, approve token spend, estimate uploads, and choose a payment mode.

## Prerequisites

- `antd` running on `http://localhost:8082`
- A configured wallet for write operations, or a local devnet started with `ant dev start`

## Steps

### 1. Check the configured wallet

{% tabs %}
{% tab title="cURL" %}
```bash
curl http://localhost:8082/v1/wallet/address
curl http://localhost:8082/v1/wallet/balance
```
{% endtab %}
{% tab title="Python" %}
```python
from antd import AntdClient

client = AntdClient()
address = client.wallet_address()
balance = client.wallet_balance()

print(address.address)
print(balance.balance)
print(balance.gas_balance)
```
{% endtab %}
{% tab title="JavaScript" %}
```javascript
import { createClient } from "antd";

async function main() {
  const client = createClient();
  const address = await client.walletAddress();
  const balance = await client.walletBalance();

  console.log(address.address);
  console.log(balance.balance);
  console.log(balance.gasBalance);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
```
{% endtab %}
{% endtabs %}

The current wallet balance response returns token balance as atto tokens and gas balance as wei.

### 2. Approve token spend

Fresh wallets may need an approval transaction before uploads can spend tokens through the payment contracts.

{% tabs %}
{% tab title="cURL" %}
```bash
curl -X POST http://localhost:8082/v1/wallet/approve \
  -H "Content-Type: application/json" \
  -d '{}'
```
{% endtab %}
{% tab title="Python" %}
```python
from antd import AntdClient

client = AntdClient()
approved = client.wallet_approve()

print(approved)
```
{% endtab %}
{% tab title="JavaScript" %}
```javascript
import { createClient } from "antd";

async function main() {
  const client = createClient();
  const approved = await client.walletApprove();
  console.log(approved);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
```
{% endtab %}
{% endtabs %}

### 3. Estimate storage cost

Cost estimation uses the current merged daemon logic and returns a string amount in atto tokens.

{% tabs %}
{% tab title="cURL" %}
```bash
DATA_B64=$(printf 'Hello, Autonomi!' | base64)

curl -X POST http://localhost:8082/v1/data/cost \
  -H "Content-Type: application/json" \
  -d "{\"data\":\"$DATA_B64\"}"
```
{% endtab %}
{% tab title="Python" %}
```python
from antd import AntdClient

client = AntdClient()
cost = client.data_cost(b"Hello, Autonomi!")

print(cost)
```
{% endtab %}
{% tab title="JavaScript" %}
```javascript
import { createClient } from "antd";

async function main() {
  const client = createClient();
  const cost = await client.dataCost(Buffer.from("Hello, Autonomi!"));
  console.log(cost);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
```
{% endtab %}
{% endtabs %}

### 4. Choose a payment mode when uploading

The current merged daemon accepts three payment modes: `auto`, `merkle`, and `single`.

- `auto` is the default
- `merkle` forces Merkle batch payments
- `single` forces per-chunk payments

{% tabs %}
{% tab title="cURL" %}
```bash
DATA_B64=$(printf 'Hello, Autonomi!' | base64)

curl -X POST http://localhost:8082/v1/data/public \
  -H "Content-Type: application/json" \
  -d "{\"data\":\"$DATA_B64\",\"payment_mode\":\"merkle\"}"
```
{% endtab %}
{% tab title="Python" %}
```python
from antd import AntdClient

client = AntdClient()
result = client.data_put_public(b"Hello, Autonomi!", payment_mode="merkle")

print(result.address)
```
{% endtab %}
{% tab title="JavaScript" %}
```javascript
import { createClient } from "antd";

async function main() {
  const client = createClient();
  const result = await client.dataPutPublic(Buffer.from("Hello, Autonomi!"), {
    paymentMode: "merkle",
  });
  console.log(result.address);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
```
{% endtab %}
{% endtabs %}

## Verify it worked

Check the wallet balance before and after a paid upload, then fetch the stored data by address. The upload response also tells you which payment mode the daemon actually used.

## Common errors

**402 Payment Required**: Fund the wallet or use a local devnet.

**503 Service Unavailable**: The daemon does not have wallet configuration.

**400 Bad Request**: Check the base64 payload and `payment_mode` value.

## Next steps

- [Store and Retrieve Data](store-and-retrieve-data.md)
- [Use External Signers](use-external-signers.md)
- [REST API](../sdk-reference/rest-api.md)
