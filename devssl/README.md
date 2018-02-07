## How to generate RSA private key and digital certificate

1. Install Openssl

Please visit https://github.com/openssl/openssl to get pkg and install.

2. Generate RSA private key and the digital certificate

```sh
$ openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```
