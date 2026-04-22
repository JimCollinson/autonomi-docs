# Use External Signers for Upload Payments

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: bf541ccd4ae1fd3e174fb7b5bb21deef38d999ce
  verified_date: 2026-04-21
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-client
  source_ref: main
  source_commit: eb29e99937b1aedba02db04e1ae59bd923b424a3
  verified_date: 2026-04-16
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: evmlib
  source_ref: main
  source_commit: 82f2fccff243b48de0e04ceb71ccb2aa17d810af
  verified_date: 2026-04-06
  verification_mode: current-merged-truth
-->

Use the two-phase upload flow when your application needs a wallet outside `antd` to sign and submit upload payments.

This is the right approach when:

- your users pay for their own uploads
- your app should not custody a wallet key for them
- you need to integrate with an external signer or wallet stack

## Prerequisites

- `antd` running without `AUTONOMI_WALLET_KEY` (see [Start the Local Daemon](../start-the-local-daemon.md))
- EVM configuration available to the daemon for the target network
- An external signer or wallet stack that can submit the required payment transactions

## Steps

### 1. Start antd without a wallet key

The daemon does not have an `--external-signer` flag. External-signer mode is the absence of `AUTONOMI_WALLET_KEY` plus the use of the prepare/finalize endpoints.

```bash
EVM_RPC_URL=https://your-rpc-endpoint \
EVM_PAYMENT_TOKEN_ADDRESS=0x... \
EVM_PAYMENT_VAULT_ADDRESS=0x... \
./target/release/antd
```

Use `EVM_PAYMENT_VAULT_ADDRESS` for both wave-batch and Merkle uploads in the external-signer flow.

### 2. Prepare the upload

For in-memory data, call `POST /v1/data/prepare`.

```bash
DATA_B64=$(printf 'Hello, Autonomi!' | base64)

curl -X POST http://localhost:8082/v1/data/prepare \
  -H "Content-Type: application/json" \
  -d "{\"data\":\"$DATA_B64\"}"
```

The prepare endpoints return a `payment_type` discriminator. Use that value to decide which on-chain call to make and which finalize payload to send back.

The daemon returns `wave_batch` for uploads under 64 chunks and `merkle` for uploads with 64 or more chunks.

Wave-batch prepare response:

```json
{
  "upload_id": "<hex_id>",
  "payment_type": "wave_batch",
  "payments": [
    {
      "quote_hash": "0x...",
      "rewards_address": "0x...",
      "amount": "<atto_token_amount>"
    }
  ],
  "total_amount": "<atto_token_amount>",
  "payment_vault_address": "0x...",
  "payment_token_address": "0x...",
  "rpc_url": "https://your-rpc-endpoint"
}
```

Merkle prepare response:

```json
{
  "upload_id": "<hex_id>",
  "payment_type": "merkle",
  "depth": 6,
  "pool_commitments": [
    {
      "pool_hash": "0x...",
      "candidates": [
        {
          "rewards_address": "0x...",
          "amount": "<atto_token_amount>"
        }
      ]
    }
  ],
  "merkle_payment_timestamp": 1744041600,
  "payment_vault_address": "0x...",
  "total_amount": "0",
  "payment_token_address": "0x...",
  "rpc_url": "https://your-rpc-endpoint"
}
```

Each `pool_commitments` entry contains exactly 16 candidate payments. The sample above shows one candidate for brevity.

For file uploads, the equivalent is `POST /v1/upload/prepare` with a local `path` field instead of `data`.

### 3. Submit the payment externally

Use your signer stack to submit the EVM payment transaction described by the prepare response.

`antd` does not sign or broadcast those transactions in this flow.

- For `wave_batch`, call `payForQuotes()` with the returned `payments` and keep the resulting transaction hashes keyed by `quote_hash`.
- For `merkle`, call `payForMerkleTree()` with `depth`, `pool_commitments`, and `merkle_payment_timestamp`, then keep the `winner_pool_hash` from the `MerklePaymentMade` event.

Both calls use the `payment_vault_address` returned by the prepare step.

### 4. Finalize the upload

After the external payment is on-chain, call `POST /v1/upload/finalize` with the matching fields for the prepared upload.

Wave-batch finalize request:

```bash
curl -X POST http://localhost:8082/v1/upload/finalize \
  -H "Content-Type: application/json" \
  -d '{"upload_id":"<hex_id>","tx_hashes":{"0xquote":"0xtx"},"store_data_map":true}'
```

Merkle finalize request:

```bash
curl -X POST http://localhost:8082/v1/upload/finalize \
  -H "Content-Type: application/json" \
  -d '{"upload_id":"<hex_id>","winner_pool_hash":"0x...","store_data_map":true}'
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

### 5. Use SDK helpers when available

The daemon SDKs follow the same prepare/finalize split. Merkle-capable bindings expose `payment_type` on prepare results and a `finalize_merkle_upload` helper for the Merkle path.

Use the REST API when you need the full finalize response surface, such as the raw `data_map` value or explicit `store_data_map` control on wave-batch finalize requests.

If you are building in Rust with ant-core instead of the daemon, the library exposes native external-payment helpers such as `data_prepare_upload`, `file_prepare_upload`, `prepare_merkle_batch_external`, and `finalize_merkle_batch`.

## Verify it worked

Finalize succeeds when the daemon accepts the `upload_id` plus either the `tx_hashes` map or the `winner_pool_hash`, then returns upload metadata. If you requested `store_data_map: true`, you can retrieve the stored content again through the returned address.

## Common errors

**404 Not Found**: The `upload_id` is missing, expired, or already finalized.

**400 Bad Request**: Check whether the prepared upload expects `tx_hashes` or `winner_pool_hash`, and validate the hex formatting of those values.

**503 Service Unavailable**: You accidentally started the daemon in direct-wallet mode or without the required network configuration.

## Next steps

- [Prepare a Wallet for Uploads](../../guides/prepare-a-wallet-for-uploads.md)
- [Estimate Costs and Handle Upload Payments](../../guides/estimate-costs-and-handle-upload-payments.md)
- [REST API](../reference/rest-api.md)
- [Use the Daemon as a Local Service](use-the-daemon-as-a-local-service.md)
