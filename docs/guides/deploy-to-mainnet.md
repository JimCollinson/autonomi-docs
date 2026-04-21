# Deploy to Mainnet

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: bf541ccd4ae1fd3e174fb7b5bb21deef38d999ce
  verified_date: 2026-04-17
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-client
  source_ref: main
  source_commit: d46a73d38731a31fbd9815394fe8a2943eb38246
  verified_date: 2026-04-17
  verification_mode: current-merged-truth
-->

Move from local testing to a mainnet-facing configuration for either `antd` or `ant`.

This guide covers both the daemon-backed SDK deployment workflow and the direct CLI deployment workflow because mainnet decisions usually touch both.

## Prerequisites

- Your application already tested locally
- Production wallet access
- Bootstrap peer information or daemon network defaults appropriate for your deployment

## Steps

### 1. Lock down wallet handling

For daemon-based deployments, provide wallet and EVM settings through the environment:

```bash
export AUTONOMI_WALLET_KEY="<hex_private_key>"
export EVM_RPC_URL="https://your-rpc-endpoint"
export EVM_PAYMENT_TOKEN_ADDRESS="0x..."
export EVM_PAYMENT_VAULT_ADDRESS="0x..."
```

For direct-network CLI deployments, provide:

```bash
export SECRET_KEY="0x<hex_private_key>"
```

### 2. Start the production daemon shape

Run `antd` without `--network local`:

```bash
antd --rest-addr 127.0.0.1:8082 --grpc-addr 127.0.0.1:50051 --log-level info
```

### 3. Verify daemon health and wallet state

```bash
curl http://127.0.0.1:8082/health
curl http://127.0.0.1:8082/v1/wallet/address
curl http://127.0.0.1:8082/v1/wallet/balance
```

### 4. Estimate and perform a small write through antd

```bash
DATA_B64=$(printf 'mainnet deployment test' | base64)

curl -X POST http://127.0.0.1:8082/v1/data/cost \
  -H "Content-Type: application/json" \
  -d "{\"data\":\"$DATA_B64\"}"

curl -X POST http://127.0.0.1:8082/v1/data/public \
  -H "Content-Type: application/json" \
  -d "{\"data\":\"$DATA_B64\"}"
```

### 5. Verify the CLI separately if you use it

The `ant` CLI expects bootstrap peers and an EVM network setting for mainnet-style writes:

```bash
SECRET_KEY=0x... ant --bootstrap 1.2.3.4:12000 --evm-network arbitrum-one file upload photo.jpg
```

If you use the private mode, the CLI saves a local `.datamap` file and uses that for later download.

### 6. Keep monitoring simple and current

Use the daemon health endpoint and wallet endpoints directly:

```bash
curl -sf http://127.0.0.1:8082/health
curl -sf http://127.0.0.1:8082/v1/wallet/balance
```

## Verify it worked

Mainnet deployment is working when the daemon reports healthy status, wallet endpoints return valid data, and a small write/read cycle succeeds with production configuration.

## Common errors

**503 on write endpoints**: The daemon is running but wallet configuration is missing.

**Direct CLI upload fails immediately**: Check `SECRET_KEY`, `--bootstrap`, and `--evm-network`.

**Unexpected local-network behavior in production**: Remove `--network local`, `--allow-loopback`, and devnet manifest flags from production commands.

## Next steps

- [Use the Daemon as a Local Service](../sdk/how-to-guides/use-the-daemon-as-a-local-service.md)
- [Estimate Costs and Handle Upload Payments](estimate-costs-and-handle-upload-payments.md)
- [Use External Signers for Upload Payments](../sdk/how-to-guides/use-external-signers-for-upload-payments.md)
