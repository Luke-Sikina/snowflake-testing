import csv
import logging

logging.basicConfig(filename='ALS-7825.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Read in patients
patient_data_mapping = dict()


# For line in mapping
logging.info('Mapping to UUIDs')
with open('ALS-7825.csv', 'w') as out:
    writer = csv.writer(out)
    writer.writerow(['PATIENT_NUM', 'UUID', 'DATA_TYPE'])
    with open('../../UUID_mapping_07Jan2024.csv') as mapping:
        for row in mapping:
            cells = row.split('|')
            if len(cells) == 4 and cells[1] in patients:
                logging.info('Patient added')
                writer.writerow([cells[1], cells[2]])
            elif len(cells) != 4:
                logging.info('Bad row: %s', row)
            else:
                logging.info('Line excluded: %s', row)
