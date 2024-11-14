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


Copy from S3

```bash
aws s3 cp bch_data_oct2024.csv s3://pic-sure-data-sharing-bucket-bch/NS_Phenotype/bch_data_oct2024.csv --sse aws:kms --sse-kms-key-id arn:aws:kms:us-east-1:762503070141:key/2fd678e3-4b33-4d69-987d-32be7812d09c

```