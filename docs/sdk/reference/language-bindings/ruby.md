# Ruby SDK

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: bf541ccd4ae1fd3e174fb7b5bb21deef38d999ce
  verified_date: 2026-04-21
  verification_mode: current-merged-truth
-->

The Ruby SDK talks to `antd` over REST by default and also includes a gRPC client.

## Install

```bash
gem install antd
```

## Connect to the daemon

```ruby
require "antd"

client = Antd::Client.new(base_url: "http://localhost:8082")
health = client.health
puts health.network
```

## Store and retrieve data

```ruby
require "antd"

client = Antd::Client.new
result = client.data_put_public("Hello, Autonomi!")
puts result.address

data = client.data_get_public(result.address)
puts data
```

## Type mappings

| Autonomi type | Ruby type |
|------|------|
| `HealthStatus` | model object with `ok` and `network` |
| `PutResult` | model object with `cost` and `address` |
| Raw data | `String` |

## Error handling

```ruby
begin
  client.data_get_public("bad-address")
rescue Antd::NotFoundError
  puts "Data not found"
rescue Antd::PaymentError
  puts "Insufficient funds"
rescue Antd::AntdError => e
  puts e.message
end
```

## Full API reference

For all available daemon endpoints, see the [REST API](../rest-api.md).
