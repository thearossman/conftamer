## Use-Cases

### Context blog example:

[Repo](https://github.com/thearossman/contextblog)

```
dlv debug --headless --listen=:2345 --api-version=2 .
```

### Caddy:

[Repo](https://github.com/caddyserver/caddy)

Short tests:

```
dlv test --headless --listen=:2345 --api-version=2 ./modules/caddyhttp/reverseproxy/ -- -test.short -test.v
```

Integration tests:

```
dlv test --headless --listen=:2345 --api-version=2 ./caddytest/integration/ -- -test.run TestRespondWithJSON -test.v
```
