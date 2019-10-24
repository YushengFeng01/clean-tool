# -*- coding: utf-8 -*-
import csv
import os

SAMPLE = "wos_standard|Al-Raḥībanī, Muṣṭafā al-Suyūtī|display_name|Al-Raḥībanī, Muṣṭafā al-Suyūtī|title|Magallaẗ al-ḥikmaẗ li-l-dirasat al-tariẖiyyẗ"

def addtion_info():
    addition = {}
    for root, subdir, files in os.walk('../build/output'):
        for csv_file in files:
            report = os.path.normpath(os.path.join(root, csv_file))
            with open(report, 'r') as csv_report:
                csv_reader = csv.DictReader(csv_report)
                for row in csv_reader:
                    k = row['diacriticals']
                    k_addition = row['addition']
                    k_addition_tag = k_addition.split('|')[::2]
                    new_s = set(k_addition_tag)

                    if k not in addition:
                        addition[k] = row['addition']
                    else:
                        # union according to tag.
                        # union_addtion_info(addition[k], new_s)
                        already = addition[k].split('|')[::2]
                        already_s = set(already)
                        print(already_s)
                        print(new_s)
                        # Find the tag in new_s but not in already_s
                        print(new_s - already_s)
                        diff = tuple(new_s - already_s)
                        print(diff)
                        # partition elements in diff and partition "|"
                        print('='*10)

def draft():
    a = {'a', 'b', 'c'}
    b = {'b'}
    print(a & b)


if __name__ == '__main__':
    addtion_info()