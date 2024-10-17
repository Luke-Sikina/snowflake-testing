import snowflake.connector as sc
import os

private_key_file = os.getcwd() + '/keys/rsa_key.p8'

conn_params = {
    'account': 'SVC_IRBP00000159_RA',
    'user': 'lucas.sikina@childrens.harvard.edu',
    'private_key_file': private_key_file,
    'warehouse': 'EDW',
    'database': 'I2B2_PROD',
    'schema': 'EDW',
    'role': 'ra_i2b2_protocol_role',
}

ctx = sc.connect(**conn_params)
cs = ctx.cursor()
