# Estimate Costs and Handle Upload Payments

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: 6c4df9b745f3adcb022ac82b6bbc485727297e3e
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: evmlib
  source_ref: main
  source_commit: 82f2fccff243b48de0e04ceb71ccb2aa17d810af
  verified_date: 2026-04-06
  verification_mode: current-merged-truth
-->

In this guide, you use `antd`, the local daemon used by the SDKs, to estimate costs, check balances, approve token spend, and choose a payment mode before you upload data.

If you want to work from the command line instead, see [Use the ant CLI](../getting-started/using-ant-client.md). If you want direct Rust access, see [Build in Rust with ant-core](../getting-started/build-directly-in-rust.md).

Featured examples on this page use cURL, Python, Node.js / TypeScript, and Rust. Other SDK languages are available in the [Language Bindings](../sdk-reference/language-bindings/overview.md) section.

## Prerequisites

- `antd` running on `http://localhost:8082` (see [Using the Autonomi Daemon](../getting-started/using-the-autonomi-daemon.md))
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
{% tab title="Node.js / TypeScript" %}
```typescript
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
{% tab title="Rust" %}
```rust
use antd_client::{Client, DEFAULT_BASE_URL};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::new(DEFAULT_BASE_URL);
    let address = client.wallet_address().await?;
    let balance = client.wallet_balance().await?;

    println!("{}", address.address);
    println!("{}", balance.balance);
    println!("{}", balance.gas_balance);
    Ok(())
}
```
{% endtab %}
{% endtabs %}

The wallet balance response returns token balance as atto tokens and gas balance as wei.

On public EVM networks, both values matter:

- ANT covers storage payment
- gas covers the transaction itself

### 2. Approve token spend

Fresh wallets may need an approval transaction before uploads can spend tokens through the payment contracts.

This approval currently grants the payment contracts an unlimited token allowance.

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
{% tab title="Node.js / TypeScript" %}
```typescript
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
{% tab title="Rust" %}
```rust
use antd_client::{Client, DEFAULT_BASE_URL};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::new(DEFAULT_BASE_URL);
    let approved = client.wallet_approve().await?;

    println!("{}", approved);
    Ok(())
}
```
{% endtab %}
{% endtabs %}

### 3. Estimate storage cost

The daemon exposes cost-estimation endpoints and returns the estimated upload cost as a string amount in atto tokens.

Use this step before uploads when you want to show a user the likely storage cost or validate that the wallet has enough balance.

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
{% tab title="Node.js / TypeScript" %}
```typescript
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
{% tab title="Rust" %}
```rust
use antd_client::{Client, DEFAULT_BASE_URL};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::new(DEFAULT_BASE_URL);
    let cost = client.data_cost(b"Hello, Autonomi!").await?;

    println!("{}", cost);
    Ok(())
}
```
{% endtab %}
{% endtabs %}

### 4. Choose a payment mode when uploading

The daemon accepts three payment modes: `auto`, `merkle`, and `single`.

- `auto` is the default
- `merkle` forces Merkle batch payments
- `single` forces per-chunk payments

For larger uploads, `merkle` reduces gas by using a batch payment flow.

### 5. Understand local versus public-network testing

On a local devnet, the test wallet is provisioned for you. On Arbitrum Sepolia or Arbitrum One, you must bring your own funded wallet.

That makes the local devnet the easiest place to verify upload payment logic before you move to a public EVM network.

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
{% tab title="Node.js / TypeScript" %}
```typescript
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
{% tab title="Rust" %}
```rust
use antd_client::{Client, DEFAULT_BASE_URL};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::new(DEFAULT_BASE_URL);
    let result = client
        .data_put_public(b"Hello, Autonomi!", Some("merkle"))
        .await?;

    println!("{}", result.address);
    Ok(())
}
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

- [Using the Autonomi Daemon](../getting-started/using-the-autonomi-daemon.md)
- [Prepare a Wallet for Uploads](manage-keys.md)
- [Store and Retrieve Data with the SDKs](store-and-retrieve-data.md)
- [Use External Signers for Upload Payments](use-external-signers.md)
- [Build Read-Only Features](build-a-read-only-application.md)
- [REST API](../sdk-reference/rest-api.md)
