# TLS server and client using Twisted


## Generate self signed certificate (server)

1. `openssl genrsa -aes256 -passout pass:SuperSecretPassword -out server.key 2048`

1. `openssl req -new -key server.key -passin pass:SuperSecretPassword -out server.csr`

1. `Common Name (e.g. server FQDN or YOUR name) []:localhost`

1. `openssl x509 -req -passin pass:SuperSecretPassword -days 1024 -in server.csr -signkey server.key -out server.crt`

1. `openssl rsa -in server.key -out server_no_pass.key -passin pass:SuperSecretPassword`

1. 'mv server_no_pass.key server.key`

1. `cat server.crt server.key > server.pem`


## How to cURL

1. `python server.py`

1. `curl --cacert keys/server.crt https://localhost:8000`


## Generate a Twisted self signed TLS object for servers

* `ssl.DefaultOpenSSLContextFactory('keys/server.key', 'keys/server.crt')`

* `ssl.PrivateCertificate.loadPEM(open('keys/server.pem').read())`

* let Twisted do it for you `endpoints.serverFromString(reactor, 'ssl:443:certKey=keys/server.crt:privateKey=keys/server.key')`
