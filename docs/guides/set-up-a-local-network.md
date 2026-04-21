# Set Up a Local Network

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: 6c4df9b745f3adcb022ac82b6bbc485727297e3e
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-node
  source_ref: main
  source_commit: 2a6e9f2a2066d80c072a7cc2cb644e35def9add3
  verified_date: 2026-04-03
  verification_mode: current-merged-truth
-->

Use the `ant-dev` workflow to start a local devnet plus `antd` on your machine.

This is the best place to test uploads before you move to Arbitrum Sepolia or Arbitrum One, because the local environment also provisions a funded wallet for you.

## Prerequisites

- Rust toolchain
- Python 3.10+
- `protoc` (Protocol Buffers compiler) available on your machine
- A local checkout of `ant-sdk`
- A local checkout of `ant-node`

## Steps

### 1. Clone the required repos

If you do not already have them locally:

```bash
git clone https://github.com/WithAutonomi/ant-sdk.git
git clone https://github.com/WithAutonomi/ant-node.git
```

### 2. Install the local dev CLI

From the `ant-sdk` repo root:

```bash
cd ant-sdk
pip install -e ant-dev/
```

This installs the `ant` command provided by the current `ant-dev` package.

If `antd` has not been built on this machine before, make sure `protoc` is installed first. On macOS, one working setup is `brew install protobuf`.

### 3. Start the local environment

Point `ant dev start` at your `ant-node` checkout:

```bash
ant dev start --ant-node-dir ../ant-node
```

If the two repos are already laid out as siblings and discovery works in your environment, `--ant-node-dir` can be omitted.

On the first run, this step can take longer than usual because local components may still be compiling in release mode. If the command times out on a cold build, run it again after the initial compilation completes.

The local start flow launches:

- a local `ant-devnet`
- `antd --network local`
- a wallet-enabled local environment with REST health on `http://localhost:8082/health`

That means local testing gives you:

- a network to upload to
- a daemon to talk to
- a wallet you can inspect
- token and gas balances for upload testing

### 4. Check status and wallet

```bash
ant dev status
ant dev wallet show
```

`ant dev status` checks the local processes and the daemon health endpoint. `ant dev wallet show` prints the configured local wallet address, token balance, and gas balance.

This is the easiest way to confirm that your local environment is actually ready for paid upload tests.

### 5. Verify the daemon responds

```bash
curl http://localhost:8082/health
```

Expected response shape:

```json
{
  "status": "ok",
  "network": "local"
}
```

### 6. Store and retrieve a quick test payload

```bash
DATA_B64=$(printf 'Local network test' | base64)

curl -X POST http://localhost:8082/v1/data/public \
  -H "Content-Type: application/json" \
  -d "{\"data\":\"$DATA_B64\"}"

curl http://localhost:8082/v1/data/public/<address>
```

### 7. Stop the local environment

```bash
ant dev stop
```

## Verify it worked

The local network is working when `ant dev status` reports a healthy daemon, `ant dev wallet show` reports a funded wallet, and a test public upload can be fetched back through the same `antd` instance.

## Common errors

**No local environment running**: Re-run `ant dev start` and check that the `ant-node` path is correct.

**Cannot reach `http://localhost:8082/health`**: Use `ant dev status` and `ant dev logs` to inspect the daemon.

**Wallet not configured**: Restart the environment; the local start flow provisions wallet access from the generated devnet manifest.

## Next steps

- [Start the Local Daemon](../sdk/start-the-local-daemon.md)
- [Prepare a Wallet for Uploads](prepare-a-wallet-for-uploads.md)
- [Store Data on the Network](../sdk/store-data-on-the-network.md)
- [Store and Retrieve Data with the SDKs](../sdk/how-to-guides/store-and-retrieve-data.md)
- [Estimate Costs and Handle Upload Payments](estimate-costs-and-handle-upload-payments.md)
