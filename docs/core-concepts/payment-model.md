# Payment Model

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: 1cbfb3e92cb4309f29e92b5609837812027f0a67
  verified_date: 2026-04-29
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-client
  source_ref: main
  source_commit: 97587c248ce6410edc1c6ee28846216ef82145eb
  verified_date: 2026-04-29
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-node
  source_ref: main
  source_commit: 23aee15cae33a17257ba833b2b98ed8a7a12e684
  verified_date: 2026-04-29
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: evmlib
  source_ref: main
  source_commit: 225acbb1af613193bcc8264b6ede4d7e4a7ac607
  verified_date: 2026-04-29
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-protocol
  source_ref: main
  source_commit: 87071931a982e8a90494353007a3f4e6ebb3de3c
  verified_date: 2026-04-29
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
- `POST /v1/files/cost`

Those endpoints return the estimated upload cost as a string amount in atto tokens.

### Payment modes

The supported payment modes are:

| Mode | Current behavior |
|------|------------------|
| `auto` | Choose Merkle for larger batches and single payments otherwise |
| `merkle` | Force Merkle batch payment |
| `single` | Force per-chunk payment |

In `ant-core`, the current Merkle threshold is `64` chunks.

Nodes verify the payment proof that arrives with each write. That includes signature checks, on-chain payment verification, and record-level validation before content is accepted into the chunk store.

Node-side storage pricing currently follows `BASELINE + K × (n / D)^2`, where `n` is the number of close records the node is already storing and `D` is a fixed divisor. That gives lightly loaded nodes a non-zero spam-barrier price and pushes larger uploads toward less-loaded close groups as the network fills.

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
- [Prepare a Wallet for Uploads](../guides/prepare-a-wallet-for-uploads.md)
- [Estimate Costs and Handle Upload Payments](../guides/estimate-costs-and-handle-upload-payments.md)
- [Use External Signers for Upload Payments](../sdk/how-to-guides/use-external-signers-for-upload-payments.md)
- [Build Read-Only Features](../guides/build-read-only-features.md)
- [Data Types](data-types.md)
