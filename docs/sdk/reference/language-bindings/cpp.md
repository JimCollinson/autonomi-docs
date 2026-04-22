# C++ SDK

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: bf541ccd4ae1fd3e174fb7b5bb21deef38d999ce
  verified_date: 2026-04-21
  verification_mode: current-merged-truth
-->

The C++ SDK is the C++ client for the `antd` daemon.

## Install

```cmake
include(FetchContent)
FetchContent_Declare(
    antd-cpp
    GIT_REPOSITORY https://github.com/WithAutonomi/ant-sdk.git
    SOURCE_SUBDIR  antd-cpp
)
FetchContent_MakeAvailable(antd-cpp)

target_link_libraries(your_target PRIVATE antd)
```

## Connect to the daemon

```cpp
#include "antd/antd.hpp"

int main() {
    antd::Client client("http://localhost:8082");
    auto health = client.health();
    return health.ok ? 0 : 1;
}
```

## Store and retrieve data

```cpp
#include "antd/antd.hpp"
#include <iostream>

int main() {
    antd::Client client;
    std::string msg = "Hello, Autonomi!";
    std::vector<uint8_t> data(msg.begin(), msg.end());

    auto result = client.data_put_public(data);
    std::cout << result.address << std::endl;

    auto retrieved = client.data_get_public(result.address);
    std::string text(retrieved.begin(), retrieved.end());
    std::cout << text << std::endl;
}
```

## Type mappings

| Autonomi type | C++ type |
|------|------|
| `HealthStatus` | struct with `ok` and `network` |
| `PutResult` | struct with `cost` and `address` |
| Raw data | `std::vector<uint8_t>` |

## Error handling

```cpp
try {
    auto data = client.data_get_public("bad-address");
} catch (const antd::NotFoundError& e) {
    std::cerr << e.what() << std::endl;
} catch (const antd::PaymentError& e) {
    std::cerr << e.what() << std::endl;
} catch (const antd::AntdError& e) {
    std::cerr << e.what() << std::endl;
}
```

## Full API reference

For all available daemon endpoints, see the [REST API](../rest-api.md).
