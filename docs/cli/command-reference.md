# CLI Command Reference

<!-- verification:
  source_repo: ant-client
  source_ref: main
  source_commit: 71ad53b047f7fc6b55e73ce6008d0a834feebbd6
  verified_date: 2026-05-02
  verification_mode: current-merged-truth
-->

Reference for the `ant` CLI command tree and its flags. The command tree below follows the direct-network CLI surface, and the option tables stay grouped by command family for easier scanning. Hidden or advanced flags are called out where they matter for troubleshooting.

## Command tree

```text
ant
├── node
│   ├── add
│   ├── daemon
│   │   ├── start
│   │   ├── stop
│   │   ├── status
│   │   └── info
│   ├── reset
│   ├── start
│   ├── status
│   └── stop
├── wallet
│   ├── address
│   └── balance
├── file
│   ├── upload
│   ├── download
│   └── cost
├── chunk
│   ├── put
│   └── get
└── update
```

## Root command and global flags

### `ant [OPTIONS] <COMMAND>`

The root command accepts the global flags used across data and node operations. Root flags must appear before the subcommand.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `--json` | boolean | No | Emit structured JSON |
| `-b, --bootstrap <IP:PORT>` | socket list | No | Bootstrap peers for data operations. Can be comma-separated or repeated. |
| `--devnet-manifest <PATH>` | path | No | Path to a local devnet manifest JSON file |
| `--allow-loopback` | boolean | No | Allow loopback connections for local devnet or local testing |
| `--ipv4-only` | boolean | No | Disable dual-stack and force IPv4-only mode |
| `--quote-timeout-secs <N>` | integer | No | Hidden. Controls lightweight network-operation timeouts such as DHT lookups. |
| `--store-timeout-secs <N>` | integer | No | Hidden. Controls chunk store and retrieve timeouts. |
| `--quote-concurrency <N>` | integer | No | Hidden. Caps the quote channel only. It does not affect store or download concurrency. |
| `--store-concurrency <N>` | integer | No | Hidden. Controls upload chunk concurrency. `--chunk-concurrency` is accepted as an alias. |
| `-v, --verbose...` | count | No | Increase log verbosity: `-v`, `-vv`, or `-vvv` |
| `--evm-network <NET>` | string | No | EVM network for payments: `arbitrum-one`, `arbitrum-sepolia`, or `local` |
| `-h, --help` | boolean | No | Print help |
| `-V, --version` | boolean | No | Print version |

**Environment:**

| Variable | Description |
|------|------|
| `SECRET_KEY` | Required for uploads and wallet commands |

**Example:**

```bash
ant --help
```

## File commands

### `ant file upload <PATH>`

Uploads a file with self-encryption and EVM payment.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `PATH` | path | Yes | File to upload |
| `--public` | boolean | No | Store the DataMap on-network so anyone with the address can download the file |
| `--merkle` | boolean | No | Force Merkle batch payment |
| `--no-merkle` | boolean | No | Force single per-chunk payments |
| `--store-timeout <N>` | integer | No | Hidden. Overrides the chunk store timeout for this upload. |
| `--store-concurrency <N>` | integer | No | Hidden. Overrides upload chunk concurrency for this upload. |
| `--overwrite` | boolean | No | Replace any existing `<filename>.datamap` instead of writing a suffixed `<filename>-2.datamap`. |

**Example:**

```bash
SECRET_KEY=0x<hex_private_key> ant file upload photo.jpg --public
```

### `ant file download [ADDRESS]`

Downloads a public file by address or a private file using a local DataMap file.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ADDRESS` | string | Conditionally | Public DataMap address. Required unless `--datamap` is provided. |
| `--datamap <PATH>` | path | No | Local `.datamap` file for private download |
| `-o, --output <PATH>` | path | Conditionally | Required for address-based downloads. Optional for `--datamap` downloads that can infer the original filename. |

**Example:**

```bash
ant file download 711c7e20006ff3e0ac6c1f3063286a0c1a3e4c409642e8c526173fa60bb7078a -o lucky.jpg
```

The output path is your local filename. In this example, the command downloads a public JPEG of Lucky the dog and saves it as `lucky.jpg`.

Private datamap example:

```bash
ant file download --datamap photo.jpg.datamap
```

### `ant file cost <PATH>`

Estimates the upload cost for a file without uploading it.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `PATH` | path | Yes | File to estimate |
| `--merkle` | boolean | No | Force Merkle batch payment mode for the estimate |
| `--no-merkle` | boolean | No | Force single payment mode for the estimate |

**Example:**

```bash
ant file cost photo.jpg --merkle
```

## Chunk commands

### `ant chunk put [FILE]`

Stores a single chunk from a file or from standard input.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `FILE` | path | No | Input file. If omitted, `ant` reads from standard input. |

**Example:**

```bash
echo "hello autonomi" | SECRET_KEY=0x<hex_private_key> ant chunk put
```

### `ant chunk get <ADDRESS>`

Retrieves a single chunk by address.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ADDRESS` | string | Yes | Hex-encoded chunk address (64 hex characters) |
| `-o, --output <PATH>` | path | No | Write the chunk to a file instead of stdout |

**Example:**

```bash
ant chunk get <chunk_address> -o chunk.bin
```

## Wallet commands

### `ant wallet address`

Prints the wallet address derived from `SECRET_KEY`.

**Parameters:**

This command has no command-specific parameters.

**Example:**

```bash
SECRET_KEY=0x<hex_private_key> ant wallet address
```

### `ant wallet balance`

Prints the token balance for the configured EVM network.

**Parameters:**

This command has no command-specific parameters.

**Example:**

```bash
SECRET_KEY=0x<hex_private_key> ant wallet balance
```

## Node commands

### `ant node daemon start`

Launches the node daemon as a detached background process.

**Parameters:**

This command has no command-specific parameters.

**Example:**

```bash
ant node daemon start
```

### `ant node daemon stop`

Shuts down the running node daemon.

**Parameters:**

This command has no command-specific parameters.

**Example:**

```bash
ant node daemon stop
```

### `ant node daemon status`

Shows whether the node daemon is running and reports summary stats.

**Parameters:**

This command has no command-specific parameters.

**Example:**

```bash
ant node daemon status
```

### `ant node daemon info`

Outputs daemon connection details for programmatic use. This command always emits JSON.

**Parameters:**

This command has no command-specific parameters.

**Example:**

```bash
ant node daemon info
```

### `ant node add`

Adds one or more nodes to the registry.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `--rewards-address <ADDR>` | string | Yes | Wallet address for node earnings |
| `--count <N>` | integer | No | Number of nodes to add |
| `--node-port <PORT|RANGE>` | string | No | Node port or port range |
| `--metrics-port <PORT|RANGE>` | string | No | Metrics port or port range |
| `--data-dir-path <PATH>` | path | No | Custom data directory prefix |
| `--log-dir-path <PATH>` | path | No | Custom log directory prefix |
| `--network-id <ID>` | integer | No | Network ID. Default `1` is mainnet. |
| `--path <PATH>` | path | No | Local node binary path |
| `--version <X.Y.Z>` | string | No | Download a specific node version |
| `--url <URL>` | string | No | Download a node archive from a URL |
| `--bootstrap <ADDRS>` | string list | No | Bootstrap peers for the node binary itself |
| `--env <K=V>` | string list | No | Node environment variables |

**Example:**

```bash
ant node add --rewards-address 0xYourWallet --count 1
```

### `ant node start`

Starts all registered nodes, or one named node with `--service-name`.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `--service-name <NAME>` | string | No | Start one named node instead of all nodes |

**Example:**

```bash
ant node start --service-name node1
```

### `ant node status`

Shows the status of all registered nodes.

**Parameters:**

This command has no command-specific parameters.

**Example:**

```bash
ant node status
```

### `ant node stop`

Stops all registered nodes, or one named node with `--service-name`.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `--service-name <NAME>` | string | No | Stop one named node instead of all nodes |

**Example:**

```bash
ant node stop --service-name node1
```

### `ant node reset`

Resets node state, including data, logs, and registry information.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `--force` | boolean | No | Skip the confirmation prompt |

**Example:**

```bash
ant node reset --force
```

## Update command

### `ant update`

Checks GitHub Releases for a newer version of the CLI, downloads it if one is available, and replaces the current executable in place.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `--force` | boolean | No | Re-download even if the current version is already latest |

**Example:**

```bash
ant update
ant update --force
```

## Related pages

- [Use the CLI](use-the-cli.md)
- [Rust Library Reference](../rust/library-reference.md)
