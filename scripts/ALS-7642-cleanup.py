import csv
import csv
import logging

patient_nums_to_omit = set()
logging.basicConfig(filename='ALS-7642.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info('Pulling in inactives...')
import csv
with open('../../inactive_patnums.txt', 'r') as inactives:
    for patnum in inactives:
        patient_nums_to_omit.add(patnum.strip())

logging.info('Pulled {s} inactives'.format(s=len(patient_nums_to_omit)))
with open('ALS-7642.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    logging.info('filtering bch_data_oct2024.csv')
    with open('bch_data_oct2024.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for cells in csv_reader:
            if cells[0] in patient_nums_to_omit:
                logging.info("Ommitting line for patient {p}", p=cells[0])
            else:
                writer.writerow(cells)