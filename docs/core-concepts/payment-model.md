# Payment Model

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
  source_repo: ant-node
  source_ref: main
  source_commit: 2a6e9f2a2066d80c072a7cc2cb644e35def9add3
  verified_date: 2026-04-03
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: evmlib
  source_ref: main
  source_commit: 82f2fccff243b48de0e04ceb71ccb2aa17d810af
  verified_date: 2026-04-06
  verification_mode: current-merged-truth
-->

Autonomi uses a pay-once storage model. You pay in Autonomi Network Token (ANT) when you upload data, then retrieve it later without ongoing storage charges or download fees.

## Why it matters

You cannot treat uploads as fire-and-forget writes. The daemon, CLI, and native Rust library all require wallet context for paid storage operations, and they differ in where they expose cost estimation, wallet approval, and payment-mode control.

## How it works

### Pay once on upload

Autonomi is designed around immutable storage rather than renewable storage leases. In practice, that means the payment event happens when you upload data. There are no recurring storage fees or separate retrieval payments.

### Wallet-backed writes

The tools use different wallet inputs:

- `antd` uses `AUTONOMI_WALLET_KEY` for direct-wallet uploads
- `ant` and `ant-core` use `SECRET_KEY` or an attached `Wallet`

Without wallet configuration, write endpoints either fail or switch into an external-signer preparation flow.

When you use the CLI or build in Rust with ant-core, quote collection and payment construction use on-chain market prices from the payment vault when preparing uploads. That keeps the client-side payment proofs aligned with the prices nodes verify on receipt.

### EVM network choices

The `ant` CLI exposes these EVM network values:

- `arbitrum-one`
- `arbitrum-sepolia`
- `local`

The daemon-side external-signer flow also exposes the RPC URL and payment contract addresses the signer needs to submit the transaction for the selected network.

### Cost estimation

The `antd` surface exposes cost estimation explicitly:

- `POST /v1/data/cost`
- `POST /v1/cost/file`

Those endpoints return the estimated upload cost as a string amount in atto tokens.

### Payment modes

The supported payment modes are:

| Mode | Current behavior |
|------|------------------|
| `auto` | Choose Merkle for larger batches and single payments otherwise |
| `merkle` | Force Merkle batch payment |
| `single` | Force per-chunk payment |

In `ant-core`, the Merkle threshold is `64` chunks.

Nodes verify the payment proof that arrives with each write. That includes signature checks, on-chain payment verification, and record-level validation before content is accepted into the chunk store.

### What happens on retrieval

Downloads do not require a separate payment step. Payments are tied to storing data, chunks, files, directories, or node-management operations that require wallet context.

## Practical example

Two payment patterns show up across the daemon and direct-network interfaces:

1. Estimate and upload through `antd`

```bash
DATA_B64=$(printf 'Hello, Autonomi!' | base64)

curl -X POST http://localhost:8082/v1/data/cost \
  -H "Content-Type: application/json" \
  -d "{\"data\":\"$DATA_B64\"}"

curl -X POST http://localhost:8082/v1/data/public \
  -H "Content-Type: application/json" \
  -d "{\"data\":\"$DATA_B64\",\"payment_mode\":\"merkle\"}"
```

2. Upload directly with `ant`

```bash
SECRET_KEY=0x... ant \
  --devnet-manifest /tmp/devnet.json \
  --allow-loopback \
  --evm-network local \
  file upload my_data.bin --public --merkle
```

In both examples, payment happens as part of the upload flow, but the daemon example exposes explicit cost-estimation endpoints while the CLI example emphasizes direct upload flags and wallet setup.

## Related pages

- [Keys, Addresses, and DataMaps](keys-addresses-and-datamaps.md)
- [Prepare a Wallet for Uploads](../how-to-guides/manage-keys.md)
- [Estimate Costs and Handle Upload Payments](../how-to-guides/handle-payments.md)
- [Use External Signers for Upload Payments](../how-to-guides/use-external-signers.md)
- [Build Read-Only Features](../how-to-guides/build-a-read-only-application.md)
- [Data Types](data-types.md)
