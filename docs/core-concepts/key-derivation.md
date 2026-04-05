# Key Derivation

<!-- verification:
  source_repo: saorsa-pqc
  source_ref: main
  source_commit: 280e5478954abeedf1a8193c599c3c9676a032ee
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

In the repos covered here, key derivation appears as a generic cryptographic primitive in `saorsa-pqc` and as domain-separated signing contexts in `ant-keygen`.

## Why it matters

This page focuses on the parts of key derivation that are actually documented in the current stack. Autonomi uses HKDF primitives and signing-context separation, but it does not define one unified key hierarchy for storage, signing, and payments.

## How it works

### HKDF in saorsa-pqc

`saorsa-pqc` provides HKDF-SHA3-256 and HKDF-SHA3-512 as key-derivation primitives.

That means the crypto library can derive new key material from shared secrets or existing key material, but the repo does not by itself define how application-level Autonomi keys should be organized.

### Domain separation in ant-keygen

`ant-keygen` uses a `--context` flag for signing and verification. That context string keeps one signing domain separate from another, so the same raw key material is not reused blindly across unrelated purposes.

The default context is `ant-node-release-v1`.

## Practical example

Generic HKDF usage from the current `saorsa-pqc` API:

```rust
use saorsa_pqc::api::kdf::HkdfSha3_256;
use saorsa_pqc::api::traits::Kdf;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let shared_secret = b"shared secret from ML-KEM";
    let info = b"application context";
    let mut derived_key = [0u8; 32];

    HkdfSha3_256::derive(shared_secret, None, info, &mut derived_key)?;
    Ok(())
}
```

Domain-separated signing with `ant-keygen`:

```bash
ant-keygen sign \
  --key ./release-signing-key.secret \
  --input ./artifact.tar.gz \
  --output ./artifact.sig \
  --context ant-node-release-v1

ant-keygen verify \
  --key ./release-signing-key.pub \
  --input ./artifact.tar.gz \
  --signature ./artifact.sig \
  --context ant-node-release-v1
```

## Current scope note

The docs can verify that HKDF primitives and signing contexts exist. They cannot verify the earlier draft claim that one application seed phrase deterministically derives every storage, signing, and payment key used across the Autonomi developer interfaces.

## Related pages

- [Post-Quantum Cryptography](post-quantum-cryptography.md)
- [Estimate Costs and Handle Upload Payments](../how-to-guides/handle-payments.md)
- [Let Users Pay with External Signers](../how-to-guides/use-external-signers.md)
