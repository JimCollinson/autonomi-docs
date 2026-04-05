# Let Users Pay with External Signers

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

Use the two-phase upload flow when your application needs a wallet outside `antd` to sign the payment transaction.

This is the right approach when:

- your users pay for their own uploads
- your app should not custody a wallet key for them
- you need to integrate with an external signer or wallet stack

## Prerequisites

- `antd` running without `AUTONOMI_WALLET_KEY` (see [Using the Autonomi Daemon](../getting-started/using-the-autonomi-daemon.md))
- EVM configuration available to the daemon for the target network
- An external signer or wallet stack that can submit the required payment transactions

## Steps

### 1. Start antd without a wallet key

The daemon does not have an `--external-signer` flag. External-signer mode is the absence of `AUTONOMI_WALLET_KEY` plus the use of the prepare/finalize endpoints.

```bash
EVM_RPC_URL=https://your-rpc-endpoint \
EVM_PAYMENT_TOKEN_ADDRESS=0x... \
EVM_DATA_PAYMENTS_ADDRESS=0x... \
./target/release/antd
```

### 2. Prepare the upload

For in-memory data, call `POST /v1/data/prepare`.

```bash
DATA_B64=$(printf 'Hello, Autonomi!' | base64)

curl -X POST http://localhost:8082/v1/data/prepare \
  -H "Content-Type: application/json" \
  -d "{\"data\":\"$DATA_B64\"}"
```

Expected response shape:

```json
{
  "upload_id": "<hex_id>",
  "payments": [
    {
      "quote_hash": "0x...",
      "rewards_address": "0x...",
      "amount": "<atto_token_amount>"
    }
  ],
  "total_amount": "<atto_token_amount>",
  "data_payments_address": "0x...",
  "payment_token_address": "0x...",
  "rpc_url": "https://your-rpc-endpoint"
}
```

For file uploads, the equivalent is `POST /v1/upload/prepare` with a local `path` field instead of `data`.

### 3. Submit the payment externally

Use your signer stack to submit the EVM payment transactions described by the prepare response.

`antd` does not sign or broadcast those transactions in this flow. Your signer must return the resulting transaction hashes keyed by the quoted payment entries.

### 4. Finalize the upload

After your external signer has submitted the transactions, call `POST /v1/upload/finalize`:

```bash
curl -X POST http://localhost:8082/v1/upload/finalize \
  -H "Content-Type: application/json" \
  -d '{"upload_id":"<hex_id>","tx_hashes":{"0xquote":"0xtx"},"store_data_map":true}'
```

Expected response shape:

```json
{
  "data_map": "<hex_encoded_datamap>",
  "address": "<64_hex_address>",
  "chunks_stored": <chunk_count>
}
```

The `address` field is only present when `store_data_map` is `true`.

### 5. Know the current SDK limitation

The Python, Node.js / TypeScript, and Rust daemon SDKs include helper methods for prepare/finalize, but their finalize wrappers do not expose the full raw REST response shape. If you need `store_data_map` or the returned `data_map`, use the REST API directly.

If you are building in Rust with ant-core instead of the daemon, the library exposes native external-payment helpers such as `data_prepare_upload`, `file_prepare_upload`, `prepare_merkle_batch_external`, and `finalize_merkle_batch`.

## Verify it worked

Finalize succeeds when the daemon accepts the `upload_id` and the external transaction hashes, then returns upload metadata. If you requested `store_data_map: true`, you can retrieve the stored content again through the returned address.

## Common errors

**404 Not Found**: The `upload_id` is missing, expired, or already finalized.

**400 Bad Request**: Check the `tx_hashes` map and the hex formatting of uploaded identifiers.

**503 Service Unavailable**: You accidentally started the daemon in direct-wallet mode or without the required network configuration.

## Next steps

- [Prepare a Wallet for Uploads](manage-keys.md)
- [Estimate Costs and Handle Upload Payments](handle-payments.md)
- [REST API](../sdk-reference/rest-api.md)
- [Use antd as a Local Service](run-as-daemon.md)
