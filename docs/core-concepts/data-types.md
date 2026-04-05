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
  verified_date: 2026-04-04
  verification_mode: current-merged-truth
-->

Autonomi stores content as immutable, content-addressed data. The main developer-facing storage surfaces in this docs set are public data, private data, chunks, files, directories, and DataMaps.

## Why it matters

These are the shapes the SDK and CLI expose for developers today. Choosing the right one determines whether you work with raw bytes already in memory, files on disk, low-level chunks, or a DataMap that you keep locally versus store on-network.

## Content-addressed and immutable

When you upload data to Autonomi, the stored result is content-addressed rather than mutable. In practice, that means:

- changing the content produces a different address
- public data and public file uploads can be retrieved from their content-derived addresses
- private workflows still store content-addressed chunks, but you keep the retrieval metadata locally in a DataMap

This is why the storage surfaces on Autonomi are immutable rather than update-in-place records.

## Current surfaces at a glance

| Surface | Current role | Typical use |
|------|------|------|
| Public data | Immutable bytes with a public address | Shared payloads, app data, public content |
| Private data | Immutable bytes returned with a local DataMap | Encrypted content you keep client-side |
| Chunk | Low-level single chunk storage | Small payloads and low-level tooling |
| File | Streamed upload/download of a file | User uploads and downloads from disk |
| Directory | Streamed upload/download of a directory tree | Folder uploads and downloads |
| DataMap | Retrieval metadata for uploaded content | Private storage, public file addressing, later downloads |

## Public data

Public data is the simplest storage surface for in-memory bytes. In the daemon APIs, you send a base64 payload and receive a public address back.

Use public data when anyone who has the returned address should be able to retrieve the content.

## Private data

Private data still stores encrypted, content-addressed chunks on the network, but the retrieval metadata is returned to you as a serialized DataMap instead of being stored publicly.

Use private data when you want the network to store the encrypted chunks while you keep the retrieval capability client-side.

In the daemon and CLI surfaces, losing that DataMap means losing the practical ability to retrieve the uploaded content.

## Chunks

Chunks are the low-level storage unit. The CLI exposes them through `ant chunk put` and `ant chunk get`, and the daemon exposes them through `/v1/chunks`.

Use chunk operations when you are building low-level tooling or want explicit control over single-chunk payloads. For most application data, use public/private data or file uploads instead.

## Files and directories

File and directory uploads wrap self-encryption, chunk storage, and DataMap handling for content that already lives on disk.

Behavior differs slightly by interface:

- `antd` exposes public file and directory upload/download endpoints
- `ant` supports both public file uploads and private uploads that keep a local `.datamap` file

Use these surfaces when you want the tooling to handle file-system input and output directly instead of working with raw byte arrays.

## DataMap

A DataMap is the retrieval metadata that ties uploaded content back to its encrypted chunks.

In the SDK and CLI surfaces, a DataMap shows up in two main ways:

- private uploads return it directly to you
- public uploads store it on-network and return an address that can be fetched later

This makes DataMap handling one of the main differences between public and private workflows.

## Practical example

The tooling maps cleanly onto these surfaces:

- use `POST /v1/data/public` or `client.data_put_public(...)` for public in-memory bytes
- use `POST /v1/data/private` or `client.data_put_private(...)` for private in-memory bytes
- use `POST /v1/files/upload/public` or `ant file upload ... --public` for files that should be publicly retrievable
- use `ant file upload ...` without `--public` when you want the CLI to keep a local `.datamap` file instead

## Related pages

- [Store and Retrieve Data with the SDKs](../how-to-guides/store-and-retrieve-data.md)
- [Payment Model](payment-model.md)
- [Keys, Addresses, and DataMaps](keys-addresses-and-datamaps.md)
- [Self-Encryption](self-encryption.md)
