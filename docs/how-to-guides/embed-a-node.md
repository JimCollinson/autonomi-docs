# Embed a Node in Your Application

<!-- verification:
  source_repo: ant-node
  source_ref: main
  source_commit: 8e9541b5bd5ae9791a1b9d037c62c76ff8a7d0c8
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->

Use the current `ant-node` API when your Rust application needs to own a node runtime directly.

## Prerequisites

- Rust toolchain
- A Rust application that can own an async node task for the life of the process
- A rewards address for production node operation

## Steps

### 1. Add `ant-node`

```toml
[dependencies]
ant-node = "0.9.0"
tokio = { version = "1", features = ["full"] }
```

### 2. Build a node with the current API

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

The current `RunningNode` surface exposes event subscriptions.

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

`NodeConfig::default()` is production-oriented and expects real rewards configuration. The current config also exposes fields such as:

- `root_dir`
- `port`
- `bootstrap`
- `network_mode`
- `payment.rewards_address`
- `payment.evm_network`

Use those directly instead of assuming the looser development defaults.

## Verify it worked

The node is running when `node.run().await?` starts successfully, the runtime binds to a port, and your event subscriber begins receiving node events.

## Common errors

**Missing rewards configuration in production mode**: The builder rejects production nodes without `payment.rewards_address`.

**Multiple identities under the default root**: Use an explicit `root_dir` if you do not want identity auto-discovery under the default node directory.

**Node task blocks the rest of the app**: Put your application orchestration around the async node task instead of expecting `run()` to return immediately.

## Next steps

- [System Overview](../architecture/system-overview.md)
- [Deploy to Mainnet](deploy-to-mainnet.md)
- [Core Concepts Overview](../core-concepts/overview.md)
