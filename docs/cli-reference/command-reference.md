# Command Reference

<!-- verification:
  source_repo: ant-client
  source_ref: main
  source_commit: 1fb95f03f8010db60e4b1e9a26957b3bb2acd8bc
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->

Reference for the `ant` CLI.

## Global flags

### `ant [FLAGS] <COMMAND>`

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `--json` | boolean | No | Emit structured JSON |
| `-b, --bootstrap <IP:PORT>` | socket list | No | Bootstrap peers for data operations |
| `--devnet-manifest <PATH>` | path | No | Local devnet manifest JSON |
| `--allow-loopback` | boolean | No | Allow loopback connections for local testing |
| `--timeout-secs <N>` | integer | No | Network timeout in seconds, default `60` |
| `--chunk-concurrency <N>` | integer | No | Upload chunk concurrency override |
| `--log-level <LEVEL>` | string | No | `trace`, `debug`, `info`, `warn`, `error` |
| `--evm-network <NET>` | string | No | `arbitrum-one`, `arbitrum-sepolia`, or `local` |

**Environment:**

| Variable | Description |
|------|------|
| `SECRET_KEY` | Required for uploads and wallet commands |

## File commands

### `ant file upload <PATH>`

Uploads a file with self-encryption and EVM payment.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `PATH` | path | Yes | File to upload |
| `--public` | boolean | No | Store the DataMap on-network |
| `--merkle` | boolean | No | Force Merkle batch payment |
| `--no-merkle` | boolean | No | Force single per-chunk payments |

**Example:**

```bash
SECRET_KEY=0x... ant file upload my_data.bin --public --devnet-manifest /tmp/devnet.json --allow-loopback --evm-network local
```

### `ant file download [ADDRESS]`

Downloads a public file by address or a private file using a local DataMap file.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ADDRESS` | string | No | Public DataMap address |
| `--datamap <PATH>` | path | No | Local `.datamap` file for private download |
| `-o, --output <PATH>` | path | No | Output file path |

**Example:**

```bash
ant file download a1b2c3... -o restored.bin --devnet-manifest /tmp/devnet.json --allow-loopback --evm-network local
```

## Chunk commands

### `ant chunk put [FILE]`

Stores a single chunk from a file or stdin.

**Example:**

```bash
echo "hello autonomi" | SECRET_KEY=0x... ant chunk put --devnet-manifest /tmp/devnet.json --allow-loopback --evm-network local
```

### `ant chunk get <ADDRESS>`

Retrieves a single chunk by address.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ADDRESS` | string | Yes | 64-character hex chunk address |
| `-o, --output <PATH>` | path | No | Write to file instead of stdout |

**Example:**

```bash
ant chunk get a1b2c3... -o output.bin --bootstrap 1.2.3.4:12000 --evm-network arbitrum-one
```

## Wallet commands

### `ant wallet address`

Prints the current wallet address derived from `SECRET_KEY`.

**Example:**

```bash
SECRET_KEY=0x... ant wallet address --evm-network arbitrum-one
```

### `ant wallet balance`

Prints the token balance for the configured EVM network.

**Example:**

```bash
SECRET_KEY=0x... ant wallet balance --evm-network arbitrum-one
```

## Node commands

### `ant node daemon start`

Starts the node-management daemon in the background.

### `ant node daemon stop`

Stops the node-management daemon.

### `ant node daemon status`

Shows daemon status and node counts.

### `ant node daemon info`

Outputs programmatic connection details for the daemon.

### `ant node add`

Adds one or more nodes to the registry.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `--rewards-address <ADDR>` | string | Yes | Wallet address for node earnings |
| `--count <N>` | integer | No | Number of nodes, default `1` |
| `--node-port <PORT|RANGE>` | string | No | Node port or range |
| `--metrics-port <PORT|RANGE>` | string | No | Metrics port or range |
| `--data-dir-path <PATH>` | path | No | Custom data directory prefix |
| `--log-dir-path <PATH>` | path | No | Custom log directory prefix |
| `--network-id <ID>` | integer | No | Network ID, default `1` |
| `--path <PATH>` | path | No | Local node binary path |
| `--version <X.Y.Z>` | string | No | Download a specific node version |
| `--url <URL>` | string | No | Download a node archive from URL |
| `--bootstrap <ADDRS>` | string list | No | Bootstrap peers |
| `--env <K=V>` | string list | No | Node environment variables |

**Example:**

```bash
ant node add --rewards-address 0xYourWallet --count 3 --node-port 12000-12002 --path /path/to/antnode
```

### `ant node start`

Starts all nodes, or one named node with `--service-name`.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `--service-name <NAME>` | string | No | Start one named node instead of all nodes |

### `ant node stop`

Stops all nodes, or one named node with `--service-name`.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `--service-name <NAME>` | string | No | Stop one named node instead of all nodes |

### `ant node status`

Shows the status of registered nodes.

### `ant node reset`

Clears node data, logs, and registry state.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `--force` | boolean | No | Skip confirmation prompt |

## Related pages

- [ant-client Overview](overview.md)
- [Use the ant CLI](../getting-started/using-ant-client.md)
- [ant-core Rust Library](ant-core-library.md)
