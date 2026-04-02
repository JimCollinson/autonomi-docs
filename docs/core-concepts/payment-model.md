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
  source_commit: 727a75c46bebc6d5948ea7754debd4220ead9400
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->

Autonomi uses a pay-once storage model. You pay in ANT when you upload data, then retrieve it later without ongoing storage charges or a separate retrieval payment flow in the current developer tooling.

## Why it matters

You cannot treat uploads as fire-and-forget writes. The daemon and direct-network tooling both require wallet context for paid storage operations, and the interfaces differ in where they expose cost estimation, wallet approval, and payment-mode control.

## How it works

### Pay once on upload

Autonomi is designed around immutable storage rather than renewable storage leases. In practice, that means the payment event happens when you upload data. The current developer tooling does not expose recurring storage fees or a separate retrieval payment step.

### Wallet-backed writes

The tools use different wallet inputs:

- `antd` uses `AUTONOMI_WALLET_KEY` for direct-wallet uploads
- `ant` and `ant-core` use `SECRET_KEY` or an attached `Wallet`

Without wallet configuration, write endpoints either fail or switch into an external-signer preparation flow.

### EVM network choices

The `ant` CLI exposes these EVM network values:

- `arbitrum-one`
- `arbitrum-sepolia`
- `local`

The daemon-side external-signer flow also exposes `EVM_RPC_URL`, `EVM_PAYMENT_TOKEN_ADDRESS`, and `EVM_DATA_PAYMENTS_ADDRESS` as part of the network configuration it needs to prepare payments.

### Cost estimation

The `antd` surface exposes cost estimation explicitly:

- `POST /v1/data/cost`
- `POST /v1/cost/file`

Those endpoints return string amounts in the smallest token units used by the daemon surface.

### Payment modes

The supported payment modes are:

| Mode | Current behavior |
|------|------------------|
| `auto` | Choose Merkle for larger batches and single payments otherwise |
| `merkle` | Force Merkle batch payment |
| `single` | Force per-chunk payment |

In `ant-core`, the Merkle threshold is `64` chunks.

### What happens on retrieval

The current download flows do not expose a separate payment step for retrieval. The payment surfaces in these repos are tied to storing data, chunks, files, directories, or node-management operations that require wallet context.

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
SECRET_KEY=0x... ant file upload my_data.bin --public --merkle \
  --devnet-manifest /tmp/devnet.json \
  --allow-loopback \
  --evm-network local
```

Both paths pay as part of the upload flow, but the daemon path exposes explicit cost-estimation endpoints while the CLI path emphasizes direct upload flags and wallet setup.

## Related pages

- [Handle Payments](../how-to-guides/handle-payments.md)
- [Use External Signers](../how-to-guides/use-external-signers.md)
- [Data Types](data-types.md)
