# Data Types

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
  verified_date: 2026-04-06
  verification_mode: current-merged-truth
-->

Autonomi stores content as immutable, content-addressed chunks. As a developer, you usually work with higher-level interfaces such as public data, private data, files, directories, and DataMaps.

## Why it matters

Because Autonomi stores content as immutable, content-addressed chunks, developers need to understand the higher-level interfaces they use to package, publish, and retrieve that data. This page explains how public data, private data, files, directories, and DataMap handling fit together.

## One storage primitive underneath

Autonomi has one underlying storage primitive: the chunk.

When you upload data:

- self-encryption turns the content into encrypted chunks
- a `DataMap` records how those chunks fit back together
- public and private workflows mainly differ in where that `DataMap` lives

A `DataMap` is not a separate storage primitive. It is retrieval metadata.

## Content-addressed and immutable

When you upload data to Autonomi, the stored result is content-addressed rather than mutable. In practice, that means:

- changing the content produces a different address
- public data and public file uploads can be retrieved from their content-derived addresses
- private workflows still store content-addressed chunks, but you keep the retrieval metadata locally in a `DataMap`

This is why Autonomi is immutable rather than update-in-place.

## Developer-facing interfaces at a glance

| Interface | Under the hood | Typical use |
|------|------|------|
| Public data | Chunks plus a published `DataMap` address | Shared payloads, app data, public content |
| Private data | Chunks plus a client-held `DataMap` | Encrypted content you keep client-side |
| Chunk | A single chunk stored directly | Small payloads and low-level tooling |
| File | Self-encrypted chunks plus a file-oriented `DataMap` flow | Uploading and downloading files from disk |
| Directory | Self-encrypted file trees plus directory-oriented `DataMap` flow | Folder uploads and downloads |
| `DataMap` | Retrieval metadata for chunked content | Private retrieval, public file addressing, later downloads |

## Public and private data

Public and private data are not two different low-level storage systems.

- In public workflows, the `DataMap` is stored or published so the content can be retrieved by address.
- In private workflows, the `DataMap` stays with you and is not stored publicly.

In the daemon APIs, you can see this difference clearly:

- `POST /v1/data/public` returns a public address
- `POST /v1/data/private` returns a serialized `DataMap`

In both cases, the underlying content is still stored as chunks.

## Chunks

Chunks are the low-level storage unit. The CLI exposes them through `ant chunk put` and `ant chunk get`, and the daemon exposes them through `/v1/chunks`.

Use chunk operations when you are building low-level tooling or want explicit control over single-chunk payloads. For most application data, use public/private data or file uploads instead.

## Files and directories

File and directory uploads wrap the same chunk-and-DataMap model for content that already lives on disk.

Behavior differs slightly by interface:

- `antd` exposes public file and directory upload/download endpoints
- `ant` supports both public file uploads and private uploads that keep a local `.datamap` file

Use these surfaces when you want the tooling to handle file-system input and output directly instead of working with raw byte arrays.

## DataMap

A DataMap is the retrieval metadata that ties uploaded content back to its encrypted chunks.

In the SDK and CLI surfaces, a DataMap shows up in two main ways:

- private uploads return it directly to you
- public uploads store it on-network and return an address that can be fetched later

This is one of the main differences between public and private workflows.

## Practical example

The tooling maps cleanly onto these interfaces:

- use `POST /v1/data/public` or `client.data_put_public(...)` when you want the `DataMap` stored publicly and returned as an address
- use `POST /v1/data/private` or `client.data_put_private(...)` when you want the `DataMap` returned to you directly
- use `POST /v1/files/upload/public` or `ant file upload ... --public` when you want file content to be publicly retrievable
- use `ant file upload ...` without `--public` when you want the CLI to keep the `.datamap` file locally instead

## Related pages

- [Store and Retrieve Data with the SDKs](../how-to-guides/store-and-retrieve-data.md)
- [Payment Model](payment-model.md)
- [Keys, Addresses, and DataMaps](keys-addresses-and-datamaps.md)
- [Self-Encryption](self-encryption.md)
