# Use the Daemon as a Local Service

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: d7652ec3da82dfbe2107778e5223dc413d95815b
  verified_date: 2026-04-30
  verification_mode: current-merged-truth
-->

Run the Autonomi Daemon, `antd`, as a long-lived local service when you want one stable Autonomi gateway that multiple applications, scripts, or background processes can share.

Use this setup if you want:

* A persistent local REST and gRPC endpoint
* One daemon shared by more than one app or tool
* Service-manager supervision instead of manually starting `antd` in a terminal

## Prerequisites

* `antd` built or installed on the target machine
* A Linux host with `systemd` for the service example below
* Optional wallet and EVM environment variables if the daemon will handle paid uploads

## Steps

### 1. Create an environment file

Keep secrets and network settings outside the unit file.

Create `/etc/antd.env`:

```bash
AUTONOMI_WALLET_KEY=<hex_private_key>
EVM_RPC_URL=https://your-rpc-endpoint
EVM_PAYMENT_TOKEN_ADDRESS=0x...
EVM_PAYMENT_VAULT_ADDRESS=0x...
```

You only need the wallet and EVM settings if this daemon will perform paid writes. For external-signer uploads, omit `AUTONOMI_WALLET_KEY` but keep the EVM settings so the prepare/finalize endpoints can describe the payment work.

### 2. Create a systemd unit

Create `/etc/systemd/system/antd.service`:

```ini
[Unit]
Description=Autonomi antd daemon
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
EnvironmentFile=/etc/antd.env
ExecStart=/usr/local/bin/antd --rest-addr 127.0.0.1:8082 --grpc-addr 127.0.0.1:50051 --log-level info
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

This binds the daemon to localhost instead of exposing it on every interface.

### 3. Start and enable the service

```bash
sudo systemctl daemon-reload
sudo systemctl enable antd
sudo systemctl start antd
```

### 4. Check health and logs

```bash
sudo systemctl status antd
curl http://127.0.0.1:8082/health
journalctl -u antd -f
```

If you need more detail in the logs, change `--log-level info` to `debug` or `trace` and restart the service.

### 5. Use fixed or dynamic ports

For a stable local service, keep explicit addresses as shown above. If another supervisor needs OS-assigned ports, `antd` also supports:

```bash
antd --rest-port 0 --grpc-port 0
```

In that mode, SDKs can discover the chosen ports from the `daemon.port` file written under the SDK data directory on startup.

## Verify it worked

The daemon is healthy when `/health` returns `status: ok` and your application can connect to the configured REST or gRPC endpoint.

## Common errors

**Port already in use**: Change `--rest-addr`, `--grpc-addr`, `--rest-port`, or `--grpc-port`.

**503 on write endpoints**: The daemon is running, but wallet or EVM payment configuration is missing.

**Startup loop in systemd**: Inspect `journalctl -u antd -f` for invalid addresses, missing binaries, or bad environment variables.

## Next steps

- [Build with the SDKs](../install.md)
- [Start the Local Daemon](../start-the-local-daemon.md)
- [Daemon Command Reference](../reference/daemon-command-reference.md)
- [REST API](../reference/rest-api.md)
