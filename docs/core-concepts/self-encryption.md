# Self-Encryption

<!-- verification:
  source_repo: self_encryption
  source_ref: master
  source_commit: 5f9d164c895f8609754c6ff2a8faf99375695276
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->

Self-encryption is the content-processing step that turns input bytes into a `DataMap` plus encrypted chunks before those chunks are stored elsewhere.

## Why it matters

This is the layer that makes uploads content-addressed and client-side encrypted. Higher-level tools such as `antd` and `ant-core` rely on it to produce the `DataMap` and chunk layout used for later retrieval.

## How it works

The current crate surface revolves around a few core operations:

- `encrypt(bytes)` returns `(DataMap, Vec<EncryptedChunk>)`
- `decrypt(data_map, chunks)` reconstructs the original content
- `stream_encrypt(...)` and `streaming_decrypt(...)` support streaming flows for files and large payloads

The current implementation uses:

- BLAKE3 for chunk hashing
- ChaCha20-Poly1305 for authenticated encryption
- Brotli compression during chunk processing

Chunk addresses are derived from the encrypted content. That is why the higher-level storage model is content-addressed: if the content changes, the resulting encrypted chunks and their addresses change too.

Important current limits from the crate itself:

- `MIN_ENCRYPTABLE_BYTES` is currently `3`
- `MAX_CHUNK_SIZE` is currently `4_190_208` bytes

The crate stores chunk metadata in a `DataMap`, and the `DataMap` can be shrunk recursively when it grows beyond the immediate chunk set. In the higher-level SDK and CLI workflows, that `DataMap` is what turns a set of encrypted chunks back into retrievable content.

## Practical example

```rust
use bytes::Bytes;
use self_encryption::{decrypt, encrypt};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let data = Bytes::from("Hello, World!".repeat(1000));

    let (data_map, encrypted_chunks) = encrypt(data.clone())?;
    let decrypted = decrypt(&data_map, &encrypted_chunks)?;

    assert_eq!(data, decrypted);
    Ok(())
}
```

The crate does not store anything on the network for you. Persisting the encrypted chunks and keeping the `DataMap` somewhere safe is the caller's responsibility. That is why higher-level tools build on top of it: they handle payment, network storage, and the public/private retrieval choices around the `DataMap`.

## Related pages

- [Data Types](data-types.md)
- [Store and Retrieve Data with the SDKs](../how-to-guides/store-and-retrieve-data.md)
- [Core Concepts Overview](overview.md)
