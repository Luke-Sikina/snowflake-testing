import csv
import logging


logging.basicConfig(filename='ALS-7721.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

patients = set()

logging.info('Finding unique patients...')
with open('../../bch_phenotypic_data.csv', 'r') as rows:
    csv_reader = csv.reader(rows)
    for row in csv_reader:
        logging.info('Patient added')
        patients.add(row[0])

logging.info('Mapping to UUIDs')
with open('ALS-7721.csv', 'w') as out:
    writer = csv.writer(file)
    with open('../../UUID_mapping_07Jan2024.csv') as mapping:
        for row in mapping:
            cells = row.split('|')
            if len(cells) == 4 and cells[2] in patients:
                logging.info('Patient added')
                writer.writerow([cells[2], cells[3]])
