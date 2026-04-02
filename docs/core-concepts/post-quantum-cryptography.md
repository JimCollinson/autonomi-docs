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
  source_commit: a81dbb5bc3c7929537873c90e7a10678993d415e
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-keygen
  source_ref: main
  source_commit: 3a2953f384a3b16391968de451b703843b98ed86
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->

The current post-quantum cryptography stack in scope centers on `saorsa-pqc`, transport documentation built around ML-KEM-768 and ML-DSA-65, and `ant-keygen` release-signing with ML-DSA-65.

## Why it matters

If you are reasoning about security, transport identity, or release authenticity, you need to know which cryptographic primitives the current repos actually document and expose today.

## How it works

### saorsa-pqc

The current `saorsa-pqc` README describes a broader PQC library that includes:

- ML-KEM key encapsulation variants
- ML-DSA signature variants
- SLH-DSA signature variants
- BLAKE3, SHA3, HMAC, HKDF, AES-256-GCM, and ChaCha20-Poly1305

So the library itself is broader than any single Autonomi-facing transport choice.

### saorsa-transport

The current `saorsa-transport` README describes its transport layer as pure post-quantum and highlights this pair for transport use:

- ML-KEM-768 for key exchange
- ML-DSA-65 for signatures

That repo frames the transport surface as no classical fallback in its documented model.

### ant-keygen

`ant-keygen` is the concrete current CLI in scope that uses ML-DSA-65 today. It generates release-signing keypairs, signs files, verifies signatures, and supports a signing context for domain separation.

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
