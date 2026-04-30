# Prepare a Wallet for Uploads

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: d7652ec3da82dfbe2107778e5223dc413d95815b
  verified_date: 2026-04-30
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-client
  source_ref: main
  source_commit: 8b2c9c606a1223f105fed9aa2b56310b6a6763da
  verified_date: 2026-04-30
  verification_mode: current-merged-truth
-->

Use this guide when you need a wallet that can pay for uploads.

This guide covers the shared wallet setup concerns across the SDK, CLI, and direct Rust interfaces.

It explains:

- what local development gives you automatically
- what changes on Arbitrum Sepolia and Arbitrum One
- which tools need which wallet input
- how to check the wallet, token balance, and gas balance before you upload

If you want to understand public addresses and `DataMap` handling rather than upload wallets, see [Keys, Addresses, and DataMaps](../core-concepts/keys-addresses-and-datamaps.md).

## Start with your environment

The practical difference between environments is:

| Environment | Wallet state |
|------|--------------|
| Local devnet | Wallet and balances are provisioned for you |
| Arbitrum Sepolia | Use a test wallet funded with test ANT and test gas |
| Arbitrum One | Use a production wallet funded with real ANT and gas on the selected EVM network |

If you are only building read-only features, you do not need any of this wallet setup.

## Prerequisites

- `antd` or `ant` installed (see [Start the Local Daemon](../sdk/start-the-local-daemon.md) for daemon setup)
- A hex-encoded key you already control for payments and uploads when you are not using the local devnet

## Steps

### 1. Know which tools need which wallet input

The toolchain expects:

- `antd` -> `AUTONOMI_WALLET_KEY`
- `ant` -> `SECRET_KEY`
- `ant-core` -> an attached `Wallet` in Rust

If you do not want the daemon to hold the wallet key, use the external-signer flow instead.

### 2. Configure a wallet for antd

For direct-wallet uploads on Arbitrum Sepolia or Arbitrum One, start `antd` with both the wallet key and the EVM payment settings.

From the `ant-sdk/antd` build directory, run:

```bash
export AUTONOMI_WALLET_KEY="<hex_private_key>"
export EVM_RPC_URL="https://your-rpc-endpoint"
export EVM_PAYMENT_TOKEN_ADDRESS="0x..."
export EVM_PAYMENT_VAULT_ADDRESS="0x..."
./target/release/antd
```

If `antd` is already on your `PATH`, use `antd` instead.

### 3. Configure a wallet for ant

The direct-network CLI uses `SECRET_KEY`.

```bash
export SECRET_KEY="0x<hex_private_key>"
ant --evm-network arbitrum-one wallet address
```

### 4. Verify the active wallet

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

### 5. Keep high-value keys outside the daemon when needed

If you do not want `antd` to hold a wallet key, run it without `AUTONOMI_WALLET_KEY` and use the external-signer flow instead.

From the `ant-sdk/antd` build directory, run:

```bash
EVM_RPC_URL=https://your-rpc-endpoint \
EVM_PAYMENT_TOKEN_ADDRESS=0x... \
EVM_PAYMENT_VAULT_ADDRESS=0x... \
./target/release/antd
```

If `antd` is already on your `PATH`, use `antd` instead.

Use `EVM_PAYMENT_VAULT_ADDRESS` for both wave-batch and Merkle external-signer uploads in this configuration.

That keeps signing outside the daemon and pushes transaction submission into your wallet or signer integration.

## Verify it worked

You are correctly configured when the chosen tool reports the expected wallet address and balance, and write operations stop returning wallet-not-configured errors.

## Common errors

**503 Service Unavailable**: `antd` is running, but the wallet key is missing for direct-wallet writes or the EVM payment settings are missing for external-signer uploads.

**Unsupported local wallet command**: `ant wallet` with `--evm-network local` requires a devnet manifest.

**Invalid key format**: Check for missing hex prefix, whitespace, or truncated secrets.

## Next steps

- [Start the Local Daemon](../sdk/start-the-local-daemon.md)
- [Estimate Costs and Handle Upload Payments](estimate-costs-and-handle-upload-payments.md)
- [Use External Signers for Upload Payments](../sdk/how-to-guides/use-external-signers-for-upload-payments.md)
- [Build Read-Only Features](build-read-only-features.md)
- [Keys, Addresses, and DataMaps](../core-concepts/keys-addresses-and-datamaps.md)
