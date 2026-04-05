# Prepare a Wallet for Uploads

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: 6c4df9b745f3adcb022ac82b6bbc485727297e3e
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-client
  source_ref: main
  source_commit: 796d0df75d748419a004aec6f5e288b41d8b496e
  verified_date: 2026-04-04
  verification_mode: current-merged-truth
-->
Use this guide when you need a wallet that can pay for uploads.

It explains:

- which tools need which wallet input
- what local development gives you automatically
- what changes on Arbitrum Sepolia and Arbitrum One
- how to check the wallet, token balance, and gas balance before you upload

If you want to understand public addresses and `DataMap` handling rather than upload wallets, see [Keys, Addresses, and DataMaps](../core-concepts/keys-addresses-and-datamaps.md).

## Prerequisites

- `antd` or `ant` installed (see [Using the Autonomi Daemon](../getting-started/using-the-autonomi-daemon.md) for daemon setup)
- A hex-encoded key you already control for payments and uploads

## Steps

### 1. Know which tools need which wallet input

The toolchain expects:

- `antd` -> `AUTONOMI_WALLET_KEY`
- `ant` -> `SECRET_KEY`
- `ant-core` -> an attached `Wallet` in Rust

If you do not want the daemon to hold the wallet key, use the external-signer flow instead.

### 2. Configure a wallet for antd

The daemon consumes a hex private key through `AUTONOMI_WALLET_KEY`.

```bash
export AUTONOMI_WALLET_KEY="<hex_private_key>"
./target/release/antd
```

### 3. Configure a wallet for ant

The direct-network CLI uses `SECRET_KEY`.

```bash
export SECRET_KEY="0x<hex_private_key>"
ant --evm-network arbitrum-one wallet address
```

### 4. Understand local, Sepolia, and mainnet

The practical difference between environments is:

| Environment | Wallet state |
|------|--------------|
| Local devnet | Wallet and balances are provisioned for you |
| Arbitrum Sepolia | Use a test wallet funded with test ANT and test gas |
| Arbitrum One | Use a production wallet funded with real ANT and gas |

If you are only building a read-only application, you do not need any of this wallet setup.

### 5. Verify the active wallet

{% tabs %}
{% tab title="antd" %}
```bash
curl http://localhost:8082/v1/wallet/address
curl http://localhost:8082/v1/wallet/balance
```
{% endtab %}
{% tab title="ant" %}
```bash
SECRET_KEY=0x... ant --evm-network arbitrum-one wallet address
SECRET_KEY=0x... ant --evm-network arbitrum-one wallet balance
```
{% endtab %}
{% endtabs %}

### 6. Keep high-value keys outside the daemon when needed

If you do not want `antd` to hold a wallet key, run it without `AUTONOMI_WALLET_KEY` and use the external-signer flow instead.

```bash
EVM_RPC_URL=https://your-rpc-endpoint \
EVM_PAYMENT_TOKEN_ADDRESS=0x... \
EVM_DATA_PAYMENTS_ADDRESS=0x... \
./target/release/antd
```

That keeps the signing step outside the daemon and pushes transaction submission into your wallet or signing service.

### 7. Use ant-keygen only for release-signing keys

`ant-keygen` is for ML-DSA-65 release signing, not for storage-payment wallets.

```bash
ant-keygen generate ./keys
ant-keygen verify-key --hex "<hex_secret_key>"
```

## Verify it worked

You are correctly configured when the chosen tool reports the expected wallet address and balance, and write operations stop returning wallet-not-configured errors.

## Common errors

**503 Service Unavailable**: `antd` is running but `AUTONOMI_WALLET_KEY` is not set.

**Unsupported local wallet command**: `ant wallet` with `--evm-network local` requires a devnet manifest.

**Invalid key format**: Check for missing hex prefix, whitespace, or truncated secrets.

## Next steps

- [Using the Autonomi Daemon](../getting-started/using-the-autonomi-daemon.md)
- [Estimate Costs and Handle Upload Payments](handle-payments.md)
- [Let Users Pay with External Signers](use-external-signers.md)
- [Build Read-Only Features](build-a-read-only-application.md)
- [Keys, Addresses, and DataMaps](../core-concepts/keys-addresses-and-datamaps.md)
