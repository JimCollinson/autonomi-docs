# Keys, Addresses, and DataMaps

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: d7652ec3da82dfbe2107778e5223dc413d95815b
  verified_date: 2026-05-02
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-client
  source_ref: main
  source_commit: 71ad53b047f7fc6b55e73ce6008d0a834feebbd6
  verified_date: 2026-05-02
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: self_encryption
  source_ref: master
  source_commit: 5f9d1646231da7ca2ce60e84d010acfb6d9c29d0
  verified_date: 2026-05-02
  verification_mode: current-merged-truth
-->

Autonomi keeps upload payment, public retrieval, and private retrieval separate.

## Why it matters

If you are building on Autonomi, you need to understand three different things:

- wallet keys pay for uploads
- public addresses retrieve public data
- `DataMap` retrieves private data

Treating those as one all-purpose developer key makes the rest of the system harder to understand.

## What you handle

| Material | When you get it | What you do with it |
|------|------------------|---------------------|
| Wallet private key | You provide it | Pay for uploads |
| Public address | Returned after a public upload or public DataMap store | Share or store it, then use it to retrieve public data |
| `DataMap` | Returned after a private upload or saved locally by some tools | Store it safely, then use it to retrieve private data |

## Wallet private key

The wallet private key is used for paid writes.

Depending on the tool you use, that appears as:

- `AUTONOMI_WALLET_KEY` for `antd`
- `SECRET_KEY` for `ant`
- an attached `Wallet` in `ant-core`

This key is about payment, not about private-data decryption.

## Public address

A public address is what you use to retrieve data that has been published on the network.

When you upload public data or store a public DataMap, the tooling returns an address that other readers can use later. If the content changes, the address changes too, because the storage model is content-addressed and immutable.

## DataMap

A `DataMap` is the private retrieval material that ties uploaded content back to its encrypted chunks.

For private data:

- the chunks are still stored on the network
- the `DataMap` is returned to you instead of being stored publicly
- if you lose that `DataMap`, you lose the practical ability to retrieve the private content

That means `DataMap` handling is a data-access concern, not a payment concern.

## Practical example

The simplest way to think about the split is:

- use a wallet key when you need to upload data
- use a public address when you want to retrieve public data
- use a `DataMap` when you want to retrieve private data

## Upstream sources

- [ant-sdk](https://github.com/WithAutonomi/ant-sdk)
- [ant-client](https://github.com/WithAutonomi/ant-client)
- [self_encryption](https://github.com/WithAutonomi/self_encryption)

## Related pages

- [Data Types](data-types.md)
- [Self-Encryption](self-encryption.md)
- [Prepare a Wallet for Uploads](../guides/prepare-a-wallet-for-uploads.md)
- [Build Read-Only Features](../guides/build-read-only-features.md)
