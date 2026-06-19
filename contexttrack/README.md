## Use-Cases

### Context blog example:

[Repo](https://github.com/thearossman/contextblog)

```
dlv debug --headless --listen=:2345 --api-version=2 .
```

### Caddy:

**Major Gotcha with Caddy**: A stale Caddy server from a previous test can still be running, which won't be caught in the current Delve run. Find the process and kill it, e.g.:

```
$ ss -tlnp | grep 2999; lsof -i :2999 2>/dev/null | head -10
LISTEN 0      4096       127.0.0.1:2999       0.0.0.0:*    users:(("caddy-test",pid=1623641,fd=12))
COMMAND       PID USER   FD   TYPE   DEVICE SIZE/OFF NODE NAME
caddy-tes 1623641 tcr6   12u  IPv4 12601032      0t0  TCP localhost:2999 (LISTEN)
$ kill 1623641
$ curl -s http://localhost:2999/config/ # validate that this returns nothing
```

[Repo](https://github.com/caddyserver/caddy)

Short tests:

```
dlv test --headless --listen=:2345 --api-version=2 ./modules/caddyhttp/reverseproxy/ -- -test.short -test.v
```

Integration tests:

```
dlv test --headless --listen=:2345 --api-version=2     --build-flags="-gcflags=net/http=-l"     ./caddytest/integration/     -- -test.v -test.timeout 0
```
