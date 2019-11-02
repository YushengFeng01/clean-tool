# -*- coding: utf-8 -*-
import unicodedata
import csv
import os

def normalizer(data_path):
    with open('normalizer_diff_report.csv', 'w') as csv_report:
        csv_writer = csv.DictWriter(csv_report, fieldnames=['character', 'code_point', 'name', 'nfkd',
                                                            'nfkd_ascii_code', 'nfd', 'nfd_ascii_code',
                                                            'nfkc', 'nfkc_ascii_code',
                                                            'nfc', 'nfc_ascii_code'])
        csv_writer.writeheader()

        with open(data_path, 'r') as src:
            for i in src:
                c = i.strip()
                nfkd_form = unicodedata.normalize('NFKD', c.decode('utf8')).encode('ascii', 'ignore')
                nfd_form = unicodedata.normalize('NFD', c.decode('utf8')).encode('ascii', 'ignore')
                nfkc_form = unicodedata.normalize('NFKC', c.decode('utf8')).encode('ascii', 'ignore')
                nfc_form = unicodedata.normalize('NFC', c.decode('utf8')).encode('ascii', 'ignore')

                csv_writer.writerow(
                    {
                        'character': c,
                        'code_point': c.decode('utf-8').encode('unicode_escape'),
                        'name': unicodedata.name(c.decode('utf-8')).lower(),
                        'nfkd': nfkd_form,
                        'nfkd_ascii_code': ord(nfkd_form) if len(nfkd_form) else '',
                        'nfd': nfd_form,
                        'nfd_ascii_code': ord(nfd_form) if len(nfd_form) else '',
                        'nfkc': nfkc_form,
                        'nfkc_ascii_code': ord(nfkc_form) if len(nfkc_form) else '',
                        'nfc': nfc_form,
                        'nfc_ascii_code': ord(nfc_form) if len(nfc_form) else ''
                    }
                )

if __name__ == '__main__':
    normalizer('additional.txt')