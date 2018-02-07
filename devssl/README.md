## How to generate RSA private key and digital certificate

1. Install Openssl

Please visit https://github.com/openssl/openssl to get pkg and install.

2. Generate RSA private key

```sh
$ openssl genrsa -out ./devssl/server.key 2048
```

3. Generate digital certificate

```sh
$ openssl req -new -x509 -key ./devssl/server.key -out ./devssl/server.pem -days 365
```
