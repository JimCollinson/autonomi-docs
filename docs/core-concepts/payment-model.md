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
  source_commit: 1fb95f03f8010db60e4b1e9a26957b3bb2acd8bc
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->

The current merged Autonomi developer interfaces charge on write operations and expose payment through wallet configuration, cost-estimation APIs, and selectable payment modes.

## Why it matters

You cannot treat uploads as fire-and-forget writes. The current daemon and direct-network tooling both require wallet context for paid storage operations, and the interfaces differ in where they expose cost estimation, wallet approval, and payment-mode control.

## How it works

### Wallet-backed writes

The current merged tools use different wallet inputs:

- `antd` uses `AUTONOMI_WALLET_KEY` for direct-wallet uploads
- `ant` and `ant-core` use `SECRET_KEY` or an attached `Wallet`

Without wallet configuration, write endpoints either fail or switch into an external-signer preparation flow.

### Current EVM network choices

The current `ant` CLI exposes these EVM network values:

- `arbitrum-one`
- `arbitrum-sepolia`
- `local`

The daemon-side external-signer flow also exposes `EVM_RPC_URL`, `EVM_PAYMENT_TOKEN_ADDRESS`, and `EVM_DATA_PAYMENTS_ADDRESS` as part of the network configuration it needs to prepare payments.

### Cost estimation

The current merged `antd` surface exposes cost estimation explicitly:

- `POST /v1/data/cost`
- `POST /v1/cost/file`

Those endpoints return string amounts in the smallest token units used by the current daemon surface.

### Payment modes

The current merged payment modes are:

| Mode | Current behavior |
|------|------------------|
| `auto` | Choose Merkle for larger batches and single payments otherwise |
| `merkle` | Force Merkle batch payment |
| `single` | Force per-chunk payment |

In `ant-core`, the Merkle threshold is currently `64` chunks.

### What happens on retrieval

The current merged download flows do not expose a separate payment step for retrieval. The payment surfaces in these repos are tied to storing data, chunks, files, directories, or node-management operations that require wallet context.

## Practical example

Two current payment patterns show up across the merged interfaces:

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
