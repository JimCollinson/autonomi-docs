# Dart SDK

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: d7652ec3da82dfbe2107778e5223dc413d95815b
  verified_date: 2026-04-30
  verification_mode: current-merged-truth
-->

The Dart SDK is the Dart client for the `antd` daemon.

## Install

```bash
dart pub add antd
```

## Connect to the daemon

```dart
import 'package:antd/antd.dart';

void main() async {
  final client = AntdClient(baseUrl: 'http://localhost:8082');
  final health = await client.health();
  print(health.network);
  client.close();
}
```

## Store and retrieve data

```dart
import 'dart:convert';
import 'dart:typed_data';

import 'package:antd/antd.dart';

void main() async {
  final client = AntdClient();
  final result = await client.dataPutPublic(Uint8List.fromList(utf8.encode('Hello, Autonomi!')));
  print(result.address);

  final data = await client.dataGetPublic(result.address);
  print(utf8.decode(data));
  client.close();
}
```

## Type mappings

| Autonomi type | Dart type |
|------|------|
| `HealthStatus` | Dart model type |
| `PutResult` | Dart model type |
| Raw data | `Uint8List` |

## Error handling

```dart
try {
  final data = await client.dataGetPublic('bad-address');
  print(data);
} on NotFoundError {
  print('Data not found');
} on PaymentError {
  print('Insufficient funds');
} on AntdError catch (error) {
  print(error);
}
```

## Full API reference

For all available daemon endpoints, see the [REST API](../rest-api.md).
