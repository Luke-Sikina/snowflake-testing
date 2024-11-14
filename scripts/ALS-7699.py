import csv
import logging


logging.basicConfig(filename='ALS-7699.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

patients = set()

logging.info('Finding unique patients...')
with open('../../inputs/ALS-7699.csv', 'r') as rows:
    csv_reader = csv.reader(rows)
    logging.info('Opened csv for reading')
    for row in csv_reader:
        if row[0] not in patients:
            logging.info('Patient added')
            patients.add(row[0])

logging.info('Mapping to MRNs')
with open('ALS-7699.csv', 'w') as out:
    writer = csv.writer(out)
    writer.writerow(['MRN', 'PATIENT_NUM'])
    with open('../../UUID_mapping_07Jan2024.csv') as mapping:
        for row in mapping:
            cells = row.split('|')
            if len(cells) == 4 and cells[1] in patients:
                logging.info('Patient added')
                writer.writerow([cells[0], cells[1]])
            elif len(cells) != 4:
                logging.info('Bad row: %s', row)
            else:
                logging.info('Line excluded: %s', row)
logging.info('Done')