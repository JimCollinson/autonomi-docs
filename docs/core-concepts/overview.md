# Core Concepts Overview

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
  source_commit: 0b104d1e8e5a8dab08a24eeb8c81b25702548c96
  verified_date: 2026-04-21
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: self_encryption
  source_ref: master
  source_commit: 5f9d1646231da7ca2ce60e84d010acfb6d9c29d0
  verified_date: 2026-04-21
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: saorsa-pqc
  source_ref: main
  source_commit: 1619cb2231db942cd65ab954ca0e0304dd6bc220
  verified_date: 2026-04-21
  verification_mode: current-merged-truth
-->

This page introduces the concepts that matter most when you build on Autonomi.

## Storage model

Autonomi stores data as immutable, content-addressed chunks. The developer-facing storage surfaces in this docs set are public data, private data, chunks, files, directories, and DataMaps. Public workflows return an address that can be shared; private workflows return retrieval metadata that you keep client-side.

Read more in [Data Types](data-types.md).

## Keys, addresses, and DataMaps

Wallet keys pay for writes, public addresses retrieve public data, and `DataMap` values are the critical retrieval material for private data.

Read more in [Keys, Addresses, and DataMaps](keys-addresses-and-datamaps.md).

## Self-encryption

Before uploaded content is stored, it is encrypted and split into chunks. The `self_encryption` crate and the higher-level upload paths in `ant-sdk` and `ant-core` are responsible for producing the DataMap and chunk layout used later for retrieval.

Read more in [Self-Encryption](self-encryption.md).

## Post-quantum cryptography

The cryptography stack uses ML-DSA-65 for signatures and ML-KEM-768 for key encapsulation. Those algorithms matter most when you are reasoning about network identity, transport security, or the broader security model.

Read more in [Post-Quantum Cryptography](post-quantum-cryptography.md).

## Payment model

Autonomi is designed around pay-once, immutable storage. Uploads are wallet-backed writes: you pay when you store data, then retrieve it later without recurring storage fees or retrieval payments.

Read more in [Payment Model](payment-model.md).

## Reading guide

Start here depending on what you need next:

- If you are building an application: [Data Types](data-types.md), then [Store and Retrieve Data with the SDKs](../sdk/how-to-guides/store-and-retrieve-data.md)
- If you need to understand wallets, public addresses, and private retrieval material: [Keys, Addresses, and DataMaps](keys-addresses-and-datamaps.md)
- If you need to understand the encryption path: [Self-Encryption](self-encryption.md)
- If you need to understand upload costs and wallets: [Payment Model](payment-model.md), then [Estimate Costs and Handle Upload Payments](../guides/estimate-costs-and-handle-upload-payments.md)
- If you need the security context: [Post-Quantum Cryptography](post-quantum-cryptography.md)
