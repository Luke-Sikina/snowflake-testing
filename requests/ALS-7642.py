import snowflake.connector
import os
import csv

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

print('Starting pull')

try:
    f = open('query.sql', 'r')
    query = f.read()
    if query is None:
        print("Query file not found.")
        exit(1)
    with open('out.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        num_results = -1
        patient_count = 0
        while num_results != 0:
            # Execute a simple query
            cur = conn.cursor()
            try:
                print('Running query for patient {patient_count}'.format(patient_count=patient_count))
                cur.execute(query, [patient_count])
                results = cur.fetchall()
                num_results = len(results)
                print('Patient {patient_count}, found {num_results}'.format(patient_count=patient_count, num_results=num_results))
                writer.writerows(results)
                
            finally:
                # Close the cursor and connection
                cur.close()
                patient_count = patient_count + 1

finally:
    conn.close()