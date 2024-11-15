import snowflake.connector
import os
import csv
import logging

def split_into_sublists(lst, n):
    return [lst[i:i + n] for i in range(0, len(lst), n)]

# Configure the logger
logging.basicConfig(filename='ALS-7515.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Snowflake connection parameters
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

logging.info('Starting pull')

try:
    f = open('ALS-7515.sql', 'r')
    query = f.read()
    patient_ids = open('ALS-7515-patients.txt').read()
    patient_ids = patient_ids.split('\n')
    patient_ids = split_into_sublists(patient_ids, 100)


    if query is None:
        logging.info("Query file not found.")
        exit(1)
    with open('ALS-7515.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        num_results = -1
        patient_count = 0

        for patient_group in patient_ids:
            cur = conn.cursor()
            try:
                logging.info('Running query for patient {patient_count}'.format(patient_count=patient_count))
                cur.execute(query, [patient_group])
                results = cur.fetchmany(1000)
                num_results = 0
                while len(results) > 0:
                    writer.writerows(results)
                    results = cur.fetchmany(1000)
                    num_results = num_results + len(results)
                logging.info('Found {num_results}'.format(num_results=num_results))
            except:
                logging.info("Error on patient {p}".format(p=patient_count))
            finally:
                # Close the cursor and connection
                cur.close()
                patient_count = patient_count + 100

finally:
    conn.close()


