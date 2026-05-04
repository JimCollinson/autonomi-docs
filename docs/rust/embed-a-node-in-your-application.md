# How to Embed a Node in Your Application

<!-- verification:
  source_repo: ant-node
  source_ref: main
  source_commit: 23aee15cae33a17257ba833b2b98ed8a7a12e684
  verified_date: 2026-05-02
  verification_mode: current-merged-truth
-->

Use the `ant-node` API when your Rust application needs to own a node runtime directly.

## Prerequisites

- Rust toolchain
- A Rust application that can own an async node task for the life of the process
- A rewards address for production node operation

## Steps

### 1. Add ant-node

Use the published `ant-node` crate from crates.io:

```toml
[dependencies]
ant-node = "0.11.0"
tokio = { version = "1", features = ["full"] }
```

The crate enables its `logging` feature by default. If you opt into `default-features = false`, add `features = ["logging"]` explicitly when you still want tracing output from the node runtime.

### 2. Build a node with the API

For local or development embedding, start from the development preset:

```rust
use ant_node::{NodeBuilder, NodeConfig};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut config = NodeConfig::development();
    config.root_dir = "./embedded-node".into();

    let mut node = NodeBuilder::new(config).build().await?;
    node.run().await?;
    Ok(())
}
```

### 3. Subscribe to node events

`RunningNode` exposes event subscriptions.

```rust
let mut node = NodeBuilder::new(NodeConfig::development()).build().await?;
let mut events = node.subscribe_events();

tokio::spawn(async move {
    while let Ok(event) = events.recv().await {
        println!("{event:?}");
    }
});
```

### 4. Configure production settings explicitly

`NodeConfig::default()` is production-oriented and expects real rewards configuration. The config includes fields such as:

- `root_dir`
- `port`
- `ipv4_only`
- `bootstrap`
- `network_mode`
- `testnet`
- `upgrade`
- `payment.rewards_address`
- `payment.evm_network`
- `bootstrap_cache`
- `storage`
- `close_group_cache_dir`
- `max_message_size`
- `log_level`

`payment.evm_network` can target `ArbitrumOne`, `ArbitrumSepolia`, or a private EVM with `Custom { rpc_url, payment_token_address, payment_vault_address }`.

Treat that list as a practical overview rather than a complete contract. For the full config surface, see the [ant-node API](https://github.com/WithAutonomi/ant-node).

## Verify it worked

The node is running when `node.run().await?` starts successfully, the runtime binds to a port, and your event subscriber begins receiving node events.

## Common errors

**Missing rewards configuration in production mode**: The builder rejects production nodes without `payment.rewards_address`.

**Multiple identities under the default root**: Use an explicit `root_dir` if you do not want identity auto-discovery under the default node directory.

**Node task blocks the rest of the app**: Put your application orchestration around the async node task instead of expecting `run()` to return immediately.

## Next steps

- [System Overview](../architecture/system-overview.md)
- [Deploy to Mainnet](../guides/deploy-to-mainnet.md)
- [Core Concepts Overview](../core-concepts/overview.md)
