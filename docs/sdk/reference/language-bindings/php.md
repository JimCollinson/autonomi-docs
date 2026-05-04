# PHP SDK

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: d7652ec3da82dfbe2107778e5223dc413d95815b
  verified_date: 2026-05-02
  verification_mode: current-merged-truth
-->

The PHP SDK is the PHP client for the `antd` daemon.

## Install

```bash
composer require autonomi/antd
```

## Connect to the daemon

```php
<?php

require_once 'vendor/autoload.php';

use Autonomi\Antd\AntdClient;

$client = new AntdClient('http://localhost:8082');
$health = $client->health();
echo $health->network . PHP_EOL;
```

## Store and retrieve data

```php
<?php

require_once 'vendor/autoload.php';

use Autonomi\Antd\AntdClient;

$client = new AntdClient();
$result = $client->dataPutPublic('Hello, Autonomi!');
echo $result->address . PHP_EOL;

$data = $client->dataGetPublic($result->address);
echo $data . PHP_EOL;
```

## Type mappings

| Autonomi type | PHP type |
|------|------|
| `HealthStatus` | response object |
| `PutResult` | response object |
| Raw data | `string` |

## Error handling

```php
<?php

use Autonomi\Antd\Errors\NotFoundError;
use Autonomi\Antd\Errors\PaymentError;

try {
    $client->dataGetPublic('bad-address');
} catch (NotFoundError $e) {
    echo "Data not found\n";
} catch (PaymentError $e) {
    echo "Insufficient funds\n";
}
```

## Full API reference

For all available daemon endpoints, see the [REST API](../rest-api.md).
