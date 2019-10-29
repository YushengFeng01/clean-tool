# -*- coding: utf-8 -*-
import csv
import os

SAMPLE = "wos_standard|Al-Raḥībanī, Muṣṭafā al-Suyūtī|display_name|Al-Raḥībanī, Muṣṭafā al-Suyūtī|title|Magallaẗ al-ḥikmaẗ li-l-dirasat al-tariẖiyyẗ"
EXTRA_SAMPLE = "DOOM|Id Software|wos_standard|Al-Raḥībanī, Muṣṭafā al-Suyūtī|display_name|Al-Raḥībanī, Muṣṭafā al-Suyūtī|title|Magallaẗ al-ḥikmaẗ li-l-dirasat al-tariẖiyyẗ"
MORE_TITLE = "DOOM|Id Software|wos_standard|Al-Raḥībanī, Muṣṭafā al-Suyūtī|display_name|Al-Raḥībanī, Muṣṭafā al-Suyūtī|title|Magallaẗ al-ḥikmaẗ li-l-dirasat al-tariẖiyyẗ|title_item|Mindwalk Stuido|title_hr|Rebacca"


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

def sort_addition_info(addition_info):
    # order: title|title example|display_name|display name example|wos_standard|wos_standard example|other|other example
    addition_l_ = addition_info.split('|')
    addition_l = [i for i in addition_l_ if len(i)]
    titles = sorted([i for i in addition_l if i.startswith('title')])
    tags_ = addition_info.split('|')[::2]
    tags = [i for i in tags_ if len(i)]

    sorted_addition = ''
    if len(titles):
        for t in titles:
            tags.remove(t)
            index = addition_l.index(t)
            title_ ='|' + '|'.join(addition_l[index:index+2])
            sorted_addition += title_
    else:
        sorted_addition += '||'

    sorted_addition += '|'
    if 'display_name' in addition_l:
        tags.remove('display_name')
        index = addition_l.index('display_name')
        sorted_addition += '|'.join(addition_l[index:index+2])
    else:
        sorted_addition += '|'

    sorted_addition += '|'
    if 'wos_standard' in addition_l:
        tags.remove('wos_standard')
        index = addition_l.index('wos_standard')
        sorted_addition += '|'.join(addition_l[index:index+2])
    else:
        sorted_addition += '|'

    if len(tags):
        sorted_addition += '|'
        for t in tags:
            index = addition_l.index(t)
            sorted_addition += '|'.join(addition_l[index:index+2])

    # Remove the first '|'
    return sorted_addition.partition('|')[2]


def check_addtion_info():
    addition = {}
    for root, subdir, files in os.walk('D:\\dev\\clean-tool\\build1028\\build\\output'):
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
    assert new == SAMPLE

    addition_info_2 = 'wos_standard|Al-Raḥībanī, Muṣṭafā al-Suyūtī'
    new = union(addition_info_2, SAMPLE)
    assert new == 'wos_standard|Al-Raḥībanī, Muṣṭafā al-Suyūtī|display_name|Al-Raḥībanī, Muṣṭafā al-Suyūtī|title|Magallaẗ al-ḥikmaẗ li-l-dirasat al-tariẖiyyẗ'

    addition_info_3 = 'display_name|Al-Raḥībanī, Muṣṭafā al-Suyūtī'
    new = union(addition_info_3, SAMPLE)
    assert new == 'display_name|Al-Raḥībanī, Muṣṭafā al-Suyūtī|wos_standard|Al-Raḥībanī, Muṣṭafā al-Suyūtī|title|Magallaẗ al-ḥikmaẗ li-l-dirasat al-tariẖiyyẗ'

    addition_info_3 = 'wos_standard|Al-Raḥībanī, Muṣṭafā al-Suyūtī|title|Magallaẗ al-ḥikmaẗ li-l-dirasat al-tariẖiyyẗ'
    new = union(addition_info_3, SAMPLE)
    assert  new, 'wos_standard|Al-Raḥībanī, Muṣṭafā al-Suyūtī|title|Magallaẗ al-ḥikmaẗ li-l-dirasat al-tariẖiyyẗ|display_name|Al-Raḥībanī, Muṣṭafā al-Suyūtī'

    addition_info_4 = 'title|Magallaẗ al-ḥikmaẗ li-l-dirasat al-tariẖiyyẗ'
    new = union(addition_info_4, SAMPLE)
    assert new == 'title|Magallaẗ al-ḥikmaẗ li-l-dirasat al-tariẖiyyẗ|wos_standard|Al-Raḥībanī, Muṣṭafā al-Suyūtī|display_name|Al-Raḥībanī, Muṣṭafā al-Suyūtī'

    check_addtion_info()

    sorted_addition = sort_addition_info('wos_standard|Al-ʿAẓamī, Muḥammad Ḍiyā’ al-Raḥman|display_name|Al-ʿAẓamī, Muḥammad Ḍiyā’ al-Raḥman|title_source|Al-mağallaẗ al-urdunniyyaẗ fī idāraẗ al-aʻmāl')
    # print(sorted_addition)
    assert sorted_addition == 'title_source|Al-mağallaẗ al-urdunniyyaẗ fī idāraẗ al-aʻmāl|display_name|Al-ʿAẓamī, Muḥammad Ḍiyā’ al-Raḥman|wos_standard|Al-ʿAẓamī, Muḥammad Ḍiyā’ al-Raḥman'

    sorted_addition = sort_addition_info('wos_standard|Al-ʿAẓamī, Muḥammad Ḍiyā’ al-Raḥman')
    # print(sorted_addition)
    assert sorted_addition == '||||wos_standard|Al-ʿAẓamī, Muḥammad Ḍiyā’ al-Raḥman'

    sorted_addition = sort_addition_info('display_name|Al-Raḥībanī, Muṣṭafā al-Suyūtī')
    # print(sorted_addition)
    assert sorted_addition == '||display_name|Al-Raḥībanī, Muṣṭafā al-Suyūtī||'

    sorted_addition = sort_addition_info('title_source|Al-mağallaẗ al-urdunniyyaẗ fī idāraẗ al-aʻmāl')
    # print(sorted_addition)
    assert sorted_addition == 'title_source|Al-mağallaẗ al-urdunniyyaẗ fī idāraẗ al-aʻmāl||||'

    addition_info_5 = 'title|Magallaẗ al-ḥikmaẗ li-l-dirasat al-tariẖiyyẗ|wos_standard|Al-Raḥībanī, Muṣṭafā al-Suyūtī|display_name|Al-Raḥībanī, Muṣṭafā al-Suyūtī'
    new = union(addition_info_5, EXTRA_SAMPLE)
    assert new == 'title|Magallaẗ al-ḥikmaẗ li-l-dirasat al-tariẖiyyẗ|wos_standard|Al-Raḥībanī, Muṣṭafā al-Suyūtī|display_name|Al-Raḥībanī, Muṣṭafā al-Suyūtī|DOOM|Id Software'

    sorted_addition = sort_addition_info(EXTRA_SAMPLE)
    # print(sorted_addition)
    assert sorted_addition == 'title|Magallaẗ al-ḥikmaẗ li-l-dirasat al-tariẖiyyẗ|display_name|Al-Raḥībanī, Muṣṭafā al-Suyūtī|wos_standard|Al-Raḥībanī, Muṣṭafā al-Suyūtī|DOOM|Id Software'

    sorted_addition = sort_addition_info(MORE_TITLE)
    # print(sorted_addition)
    assert sorted_addition == 'title|Magallaẗ al-ḥikmaẗ li-l-dirasat al-tariẖiyyẗ|title_hr|Rebacca|title_item|Mindwalk Stuido|display_name|Al-Raḥībanī, Muṣṭafā al-Suyūtī|wos_standard|Al-Raḥībanī, Muṣṭafā al-Suyūtī|DOOM|Id Software'
