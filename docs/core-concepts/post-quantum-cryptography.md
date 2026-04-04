# Post-Quantum Cryptography

<!-- verification:
  source_repo: saorsa-pqc
  source_ref: main
  source_commit: 280e5478954abeedf1a8193c599c3c9676a032ee
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: saorsa-transport
  source_ref: main
  source_commit: b2c2280b88adb94203554bd2c80cb0c0fcb8ce6a
  verified_date: 2026-04-03
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-keygen
  source_ref: main
  source_commit: 3a2953f384a3b16391968de451b703843b98ed86
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->

The post-quantum cryptography described here centers on `saorsa-pqc`, transport documentation built around ML-KEM-768 and ML-DSA-65, and `ant-keygen` release-signing with ML-DSA-65.

## Why it matters

If you are reasoning about security, transport identity, or release authenticity, you need to know which cryptographic primitives the stack uses.

## How it works

### saorsa-pqc

`saorsa-pqc` is a broader PQC library that includes:

- ML-KEM key encapsulation variants
- ML-DSA signature variants
- SLH-DSA signature variants
- BLAKE3, SHA3, HMAC, HKDF, AES-256-GCM, and ChaCha20-Poly1305

So the library itself is broader than any single Autonomi-facing transport choice.

### saorsa-transport

`saorsa-transport` describes its transport layer as pure post-quantum and highlights this pair for transport use:

- ML-KEM-768 for key exchange
- ML-DSA-65 for signatures

The transport layer has no classical fallback.

### ant-keygen

`ant-keygen` is the release-signing CLI that uses ML-DSA-65. It generates release-signing keypairs, signs files, verifies signatures, and supports a signing context for domain separation.

## Practical example

```bash
ant-keygen generate ./keys

ant-keygen sign \
  --key ./keys/release-signing-key.secret \
  --input ./artifact.tar.gz \
  --output ./artifact.sig

ant-keygen verify \
  --key ./keys/release-signing-key.pub \
  --input ./artifact.tar.gz \
  --signature ./artifact.sig
```

## Upstream sources

- [saorsa-pqc](https://github.com/saorsa-labs/saorsa-pqc)
- [saorsa-transport](https://github.com/saorsa-labs/saorsa-transport)
- [ant-keygen](https://github.com/WithAutonomi/ant-keygen)

## Related pages

- [Key Derivation](key-derivation.md)
- [Self-Encryption](self-encryption.md)
- [Core Concepts Overview](overview.md)
