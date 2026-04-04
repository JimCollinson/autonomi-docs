# Manage Keys and Wallets

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
<!-- verification:
  source_repo: ant-keygen
  source_ref: main
  source_commit: 3a2953f384a3b16391968de451b703843b98ed86
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->

This guide shows how the Autonomi toolchain consumes existing wallet and signing keys.

## Prerequisites

- `antd` or `ant` installed
- A hex-encoded key you already control for payments and uploads

## Steps

### 1. Configure a wallet for antd

The daemon consumes a hex private key through `AUTONOMI_WALLET_KEY`.

```bash
export AUTONOMI_WALLET_KEY="<hex_private_key>"
./target/release/antd
```

### 2. Configure a wallet for ant

The direct-network CLI uses `SECRET_KEY`.

```bash
export SECRET_KEY="0x<hex_private_key>"
ant --evm-network arbitrum-one wallet address
```

### 3. Verify the active wallet

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

### 4. Keep high-value keys outside the daemon when needed

If you do not want `antd` to hold a wallet key, run it without `AUTONOMI_WALLET_KEY` and use the external-signer flow instead.

```bash
EVM_RPC_URL=https://your-rpc-endpoint \
EVM_PAYMENT_TOKEN_ADDRESS=0x... \
EVM_DATA_PAYMENTS_ADDRESS=0x... \
./target/release/antd
```

That keeps the signing step outside the daemon and pushes transaction submission into your wallet or signing service.

### 5. Use ant-keygen only for release-signing keys

`ant-keygen` is currently for ML-DSA-65 release signing, not for storage-payment wallets.

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

- [Handle Payments](handle-payments.md)
- [Use External Signers](use-external-signers.md)
- [Key Derivation](../core-concepts/key-derivation.md)
