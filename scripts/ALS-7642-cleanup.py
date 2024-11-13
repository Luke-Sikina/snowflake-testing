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


with open('ALS-7642.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    logging.info('filtering out1.csv')
    with open('out1.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for cells in csv_reader:
            if cells[0] in patient_nums_to_omit:
                logging.info("Ommitting line for patient {p}", p=cells[0])
            else:
                writer.writerow(cells)

    logging.info('filtering out.csv')
    with open('out.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for cells in csv_reader:
            if cells[0] in patient_nums_to_omit:
                logging.info("Ommitting line for patient {p}", p=cells[0])
            else:
                writer.writerow(cells)