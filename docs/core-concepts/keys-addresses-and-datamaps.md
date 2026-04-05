# Keys, Addresses, and DataMaps

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: 6c4df9b745f3adcb022ac82b6bbc485727297e3e
  verified_date: 2026-04-05
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-client
  source_ref: main
  source_commit: 796d0df75d748419a004aec6f5e288b41d8b496e
  verified_date: 2026-04-05
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: self_encryption
  source_ref: master
  source_commit: 5f9d1646231da7ca2ce60e84d010acfb6d9c29d0
  verified_date: 2026-04-05
  verification_mode: current-merged-truth
-->

Autonomi applications handle a few different kinds of key-like or secret material, and each one has a different job.

## Why it matters

If you are building on Autonomi, you need to know which one is used for:

- paying for uploads
- retrieving public data
- retrieving private data

Those are different concerns.

## What you handle

The main things you handle are:

| Material | What it is for |
|------|-----------------|
| Wallet private key | Paying for uploads |
| Public address | Retrieving public data |
| DataMap | Retrieving private data |

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

That means `DataMap` handling is closer to access material than to a payment wallet.

## Practical example

Here is the simplest way to think about the split:

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
- [Prepare a Wallet for Uploads](../how-to-guides/manage-keys.md)
- [Build Read-Only Features](../how-to-guides/build-a-read-only-application.md)
