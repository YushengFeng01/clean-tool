# -*- coding: utf-8 -*-
import csv
import os

SAMPLE = "wos_standard|Al-Raḥībanī, Muṣṭafā al-Suyūtī|display_name|Al-Raḥībanī, Muṣṭafā al-Suyūtī|title|Magallaẗ al-ḥikmaẗ li-l-dirasat al-tariẖiyyẗ"


def union(addition_info, new):
    tags = set(addition_info.split('|')[::2])
    new_tags = set(new.split('|')[::2])
    new_addition_info_l = new.split('|')
    extra_tags = list(new_tags-tags)
    for e in extra_tags:
        e_index = new_addition_info_l.index(e)
        extra_addition_info = '|'.join(new_addition_info_l[e_index:e_index+2])
        addition_info = addition_info + '|' + extra_addition_info

    return addition_info

def check_addtion_info():
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

                    if k in addition:
                        addition[k] = union(addition[k], row['addition'])
                    else:
                        addition[k] = row['addition']

                    already = addition[k].split('|')[::2]
                    already_s = set(already)

                    diff = tuple(new_s - already_s)
                    # We expect it never displays anything.
                    if len(diff):
                        print(already_s)
                        print(new_s)
                        print(new_s - already_s)




if __name__ == '__main__':
    addition_info_1 = 'wos_standard|Al-Raḥībanī, Muṣṭafā al-Suyūtī|display_name|Al-Raḥībanī, Muṣṭafā al-Suyūtī'
    new = union(addition_info_1, SAMPLE)
    assert new, SAMPLE

    addition_info_2 = 'wos_standard|Al-Raḥībanī, Muṣṭafā al-Suyūtī'
    new = union(addition_info_2, SAMPLE)
    assert new, 'wos_standard|Al-Raḥībanī, Muṣṭafā al-Suyūtī|display_name|Al-Raḥībanī, Muṣṭafā al-Suyūtī'

    addition_info_3 = 'display_name|Al-Raḥībanī, Muṣṭafā al-Suyūtī'
    new = union(addition_info_3, SAMPLE)
    assert new, 'display_name|Al-Raḥībanī, Muṣṭafā al-Suyūtī|wos_standard|Al-Raḥībanī, Muṣṭafā al-Suyūtī|title|Magallaẗ al-ḥikmaẗ li-l-dirasat al-tariẖiyyẗ'

    addition_info_3 = 'wos_standard|Al-Raḥībanī, Muṣṭafā al-Suyūtī|title|Magallaẗ al-ḥikmaẗ li-l-dirasat al-tariẖiyyẗ'
    new = union(addition_info_3, SAMPLE)
    assert  new, 'wos_standard|Al-Raḥībanī, Muṣṭafā al-Suyūtī|title|Magallaẗ al-ḥikmaẗ li-l-dirasat al-tariẖiyyẗ|display_name|Al-Raḥībanī, Muṣṭafā al-Suyūtī'

    addition_info_4 = 'title|Magallaẗ al-ḥikmaẗ li-l-dirasat al-tariẖiyyẗ'
    new = union(addition_info_4, SAMPLE)
    assert new, addition_info_4

    check_addtion_info()