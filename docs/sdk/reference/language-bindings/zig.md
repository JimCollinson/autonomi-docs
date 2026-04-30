# Zig SDK

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: d7652ec3da82dfbe2107778e5223dc413d95815b
  verified_date: 2026-04-30
  verification_mode: current-merged-truth
-->

The Zig SDK is the Zig client for the `antd` daemon.

## Install

```zig
.dependencies = .{
    .antd = .{
        .url = "https://github.com/WithAutonomi/ant-sdk/archive/<commit>.tar.gz",
        .hash = "...",
    },
},
```

## Connect to the daemon

```zig
const std = @import("std");
const antd = @import("antd");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    var client = antd.Client.init(allocator, antd.default_base_url);
    defer client.deinit();

    const status = try client.health();
    defer status.deinit(allocator);
    std.debug.print("{s}\n", .{status.network});
}
```

## Store and retrieve data

```zig
const std = @import("std");
const antd = @import("antd");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    var client = antd.Client.init(allocator, antd.default_base_url);
    defer client.deinit();

    const result = try client.dataPutPublic("Hello, Autonomi!");
    defer result.deinit(allocator);
    std.debug.print("{s}\n", .{result.address});

    const data = try client.dataGetPublic(result.address);
    defer allocator.free(data);
    std.debug.print("{s}\n", .{data});
}
```

## Type mappings

| Autonomi type | Zig type |
|------|------|
| `HealthStatus` | Zig struct |
| `PutResult` | Zig struct |
| Raw data | `[]const u8` |

## Error handling

```zig
const result = client.dataPutPublic("data") catch |err| switch (err) {
    error.NotFound => return err,
    error.Payment => return err,
    else => return err,
};
_ = result;
```

## Full API reference

For all available daemon endpoints, see the [REST API](../rest-api.md).
