import csv
import logging

logging.basicConfig(filename='ALS-7825.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Read in patients
patient_data_mapping = dict()
logging.info('Finding unique patients...')
with open('../../inputs/ALS-7825.csv', 'r') as rows:
    csv_reader = csv.reader(rows)
    logging.info('Opened csv for reading')
    for row in csv_reader:
        patient_data_mapping[row[0]] = row[1]

# For line in mapping
logging.info('Mapping to UUIDs')
with open('ALS-7825.csv', 'w') as out:
    writer = csv.writer(out)
    logging.info('Writing output')
    writer.writerow(['PATIENT_NUM', 'UUID', 'DATA_TYPE'])
    with open('../../UUID_mapping_07Jan2024.csv') as mapping:
        for row in mapping:
            cells = row.split('|')
            if len(cells) == 4 and cells[1] in patient_data_mapping:
                writer.writerow([cells[1], cells[2], patient_data_mapping[cells[1]]])
            elif len(cells) != 4:
                logging.info('Bad row: %s', row)
logging.info('Done')
