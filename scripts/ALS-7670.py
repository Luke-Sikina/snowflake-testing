# Take all the patient UUIDs and translate them into patient nums
import logging

logging.basicConfig(filename='ALS-7670.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info('Populating uuids...')
uuids = set()
with open('../../uuids.txt', 'r') as uuids_file:
    for uuid in uuids_file:
        uuids.add(uuid.strip())
logging.info('Populated %s uuids', len(uuids))

with open('../../UUID_mapping_07Jan2024.csv') as mapping:
    for row in mapping:
        cells = row.split('|')
        
# Run query

