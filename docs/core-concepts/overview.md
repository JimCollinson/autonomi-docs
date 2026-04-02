# Core Concepts Overview

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
<!-- verification:
  source_repo: self_encryption
  source_ref: master
  source_commit: 5f9d164c895f8609754c6ff2a8faf99375695276
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: saorsa-pqc
  source_ref: main
  source_commit: 280e5478954abeedf1a8193c599c3c9676a032ee
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->

This page maps the current merged concepts that matter most when you build on Autonomi.

## Storage model

The current developer-facing storage surfaces are public data, private data, chunks, files, directories, and DataMaps. Public workflows return an address that can be shared; private workflows return retrieval metadata that you keep client-side.

Read more in [Data Types](data-types.md).

## Self-encryption

Before uploaded content is stored, it is encrypted and split into chunks. The current `self_encryption` crate and the higher-level upload paths in `ant-sdk` and `ant-core` are responsible for producing the DataMap and chunk layout used later for retrieval.

Read more in [Self-Encryption](self-encryption.md).

## Post-quantum cryptography

The current merged cryptography stack in scope uses ML-DSA-65 for signatures and ML-KEM-768 for key encapsulation. Those algorithms matter most when you are reasoning about network identity, transport security, or the broader security model.

Read more in [Post-Quantum Cryptography](post-quantum-cryptography.md).

## Payment model

Current upload flows are wallet-backed writes. The daemon and direct-network clients expose payment through wallet configuration, explicit cost-estimation APIs, and payment-mode selection such as `auto`, `merkle`, and `single`.

Read more in [Payment Model](payment-model.md).

## Reading guide

Start here depending on what you need next:

- If you are building an application: [Data Types](data-types.md), then [Store and Retrieve Data](../how-to-guides/store-and-retrieve-data.md)
- If you need to understand the encryption path: [Self-Encryption](self-encryption.md)
- If you need to understand upload costs and wallets: [Payment Model](payment-model.md), then [Handle Payments](../how-to-guides/handle-payments.md)
- If you need the security context: [Post-Quantum Cryptography](post-quantum-cryptography.md)
