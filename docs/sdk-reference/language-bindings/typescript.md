# TypeScript SDK

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: 6c4df9b745f3adcb022ac82b6bbc485727297e3e
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->

The TypeScript SDK uses the same `antd` package as JavaScript and ships its own type definitions.

## Install

```bash
npm install antd
```

## Connect to the daemon

```typescript
import { RestClient, createClient, type RestClientOptions } from "antd";

const client = createClient();

const options: RestClientOptions = {
  baseUrl: "http://localhost:8082",
  timeout: 60_000,
};

const directClient = new RestClient(options);
```

## Store and retrieve data

```typescript
import { createClient, type PutResult } from "antd";

async function main(): Promise<void> {
  const client = createClient();
  const result: PutResult = await client.dataPutPublic(Buffer.from("Hello from TypeScript!"));
  console.log(result.address);

  const data: Buffer = await client.dataGetPublic(result.address);
  console.log(data.toString());
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
```

## Type mappings

| Autonomi type | TypeScript type |
|------|------|
| `HealthStatus` | `{ ok: boolean; network: string }` |
| `PutResult` | `{ cost: string; address: string }` |
| `WalletAddress` | `{ address: string }` |
| `WalletBalance` | `{ balance: string; gasBalance: string }` |
| `PrepareUploadResult` | typed object exported from `antd` |
| `FinalizeUploadResult` | `{ address: string; chunksStored: number }` |
| Raw data | `Buffer` |

## Error handling

```typescript
import { NotFoundError, PaymentError, createClient } from "antd";

async function main(): Promise<void> {
  const client = createClient();

  try {
    await client.dataGetPublic("nonexistent");
  } catch (error) {
    if (error instanceof NotFoundError) {
      console.log("Not found");
    } else if (error instanceof PaymentError) {
      console.log("Insufficient funds");
    } else {
      throw error;
    }
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
```

## Full API reference

For all available daemon endpoints, see the [REST API](../rest-api.md).
