# snowflake-testing

## Setup

1. Generate Key

```bash
openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out /keys/rsa_key.p8 -nocrypt
openssl genrsa 2048 | openssl pkcs8 -topk8 -v2 des3 -inform PEM -out /keys/rsa_key.p8
```

2. Install requirements

```bash
pip3 install -r requirements.txt
```

3. Run

```bash
python3 test_db.txt
```