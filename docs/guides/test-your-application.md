# Test Your Application

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: d7652ec3da82dfbe2107778e5223dc413d95815b
  verified_date: 2026-04-30
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-client
  source_ref: main
  source_commit: 8b2c9c606a1223f105fed9aa2b56310b6a6763da
  verified_date: 2026-04-30
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-node
  source_ref: main
  source_commit: 23aee15cae33a17257ba833b2b98ed8a7a12e684
  verified_date: 2026-04-30
  verification_mode: current-merged-truth
-->

Test against the local tooling first, then move outward to more production-like environments.

This guide focuses on the shared testing progression that applies across SDK, CLI, and direct Rust work, even though the local daemon environment is the first concrete example.

## Prerequisites

- A test framework for your language
- `ant-dev` installed from an `ant-sdk` checkout, or a direct-network local devnet if you are testing `ant-core`

If you also use the direct-network `ant` CLI from `ant-client`, isolate `ant-dev` in a virtualenv, `pipx`, or a separate `PATH` so the two `ant` commands do not shadow each other.

## Steps

### 1. Keep unit tests local to your own code

Mock the daemon client or direct-network wrapper at your application boundary.

{% tabs %}
{% tab title="Python" %}
```python
from unittest.mock import MagicMock
from antd import PutResult

def test_store_data():
    mock_client = MagicMock()
    mock_client.data_put_public.return_value = PutResult(cost="1", address="abc123")

    result = mock_client.data_put_public(b"test data")
    assert result.address == "abc123"
```
{% endtab %}
{% tab title="Node.js / TypeScript" %}
```typescript
import { describe, expect, it, vi } from "vitest";

describe("store data", () => {
  it("returns an address", async () => {
    const mockClient = {
      dataPutPublic: vi.fn().mockResolvedValue({ cost: "1", address: "abc123" }),
    };

    const result = await mockClient.dataPutPublic(Buffer.from("test data"));
    expect(result.address).toBe("abc123");
  });
});
```
{% endtab %}
{% endtabs %}

### 2. Run integration tests against the local daemon environment

Start the local environment:

```bash
ant dev start --ant-node-dir ../ant-node
```

Check the daemon:

```bash
curl http://localhost:8082/health
```

Then run a round-trip integration test.

{% tabs %}
{% tab title="Python" %}
```python
from antd import AntdClient

def test_round_trip():
    client = AntdClient()
    status = client.health()
    assert status.ok

    original = b"Integration test data"
    result = client.data_put_public(original)
    retrieved = client.data_get_public(result.address)

    assert retrieved == original
```
{% endtab %}
{% tab title="Node.js / TypeScript" %}
```typescript
import { describe, expect, it } from "vitest";
import { createClient } from "antd";

describe("integration", () => {
  it("round-trips public data", async () => {
    const client = createClient();
    const status = await client.health();
    expect(status.ok).toBe(true);

    const original = Buffer.from("Integration test data");
    const result = await client.dataPutPublic(original);
    const retrieved = await client.dataGetPublic(result.address);

    expect(retrieved).toEqual(original);
  });
});
```
{% endtab %}
{% endtabs %}

### 3. Use the built-in example smoke tests

The `ant-dev` CLI can run example programs from the repo:

```bash
ant dev example connect
ant dev example data
```

These are a good smoke-test layer before you run your own suite.

### 4. Add CI setup explicitly

If your CI job starts the local environment, make the `ant-node` checkout explicit:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check out ant-sdk
        uses: actions/checkout@v4
        with:
          repository: WithAutonomi/ant-sdk
          path: ant-sdk

      - name: Check out ant-node
        uses: actions/checkout@v4
        with:
          repository: WithAutonomi/ant-node
          path: ant-node

      - name: Install ant-dev
        run: pip install -e ant-sdk/ant-dev/

      - name: Start local environment
        run: ant dev start --ant-node-dir ./ant-node

      - name: Wait for antd
        run: |
          for i in $(seq 1 30); do
            curl -sf http://localhost:8082/health && exit 0
            sleep 1
          done
          exit 1

      - name: Run tests
        run: pytest -v

      - name: Stop local environment
        if: always()
        run: ant dev stop
```

## Verify it worked

Your local integration environment is healthy when `ant dev status` reports a running daemon and your round-trip test passes against `http://localhost:8082`.

## Common errors

**Health check never turns green**: Inspect `ant dev logs`.

**Wrong daemon API shape in tests**: Update tests to the JSON/base64 `antd` surface.

**Local wallet issues**: Recreate the environment with `ant dev reset` or `ant dev stop` followed by `ant dev start`.

## Next steps

- [Set Up a Local Network](set-up-a-local-network.md)
- [Deploy to Mainnet](deploy-to-mainnet.md)
- [Store and Retrieve Data with the SDKs](../sdk/how-to-guides/store-and-retrieve-data.md)
