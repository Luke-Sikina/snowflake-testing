# Take all the patient UUIDs and translate them into patient nums
import snowflake.connector
import logging
import os
import csv

logging.basicConfig(filename='ALS-7670.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info('Populating uuids...')
uuids = set()
with open('../../uuids.txt', 'r') as uuids_file:
    for uuid in uuids_file:
        uuids.add(uuid.strip())
logging.info('Populated %s uuids', len(uuids))

logging.info('Mapping uuids to patient_nums')
patients = dict()
with open('../../UUID_mapping_07Jan2024.csv') as mapping:
    for row in mapping:
        cells = row.split('|')
        if cells[2] in uuids:
            patients[cells[1]] = cells[2]
            logging.info('Added patient mapping %s: %s', cells[1], cells[2])
logging.info('Mapped %s uuids', len(patients))

logging.info('Connecting to snowflake')
account = 'ita05443.us-east-1'
host='ita05443.us-east-1.snowflakecomputing.com'
user = 'SVC_IRBP00000159_RA'
password = os.environ.get("SNOWFLAKE_PASSWORD")
warehouse = 'RESEARCH_COMPUTING_WH'
database = 'I2B2_PROD'
schema = 'EDW'
role = 'ra_i2b2_protocol_role'

# Establish connection to Snowflake
conn = snowflake.connector.connect(
    host=host,
    user=user,
    password=password,
    account=account,
    warehouse=warehouse,
    database=database,
    schema=schema,
    role=role,
    port=443
)
f = open('ALS-7670.sql', 'r')
query = f.read()

logging.info('Running query')
with open('ALS-7670.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    try:
        cur = conn.cursor()
        cur.execute(query, [patients.values()])
        results = cur.fetchmany(1000)
        logging.info('Writing results')
        while len(results) > 0:
            for row in results:
                row = row.append(patients[row[0]])
                writer.write(row)
    finally:
        conn.close()

logging.info('Done')

