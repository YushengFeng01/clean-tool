# -*- coding: utf-8 -*-
import unittest
import shutil
import os

from diacriticals import *

test_data = """
    Al-Maǧalaẗ al-arabiaẗ li-l-dirasat al-amniaẗ
Magallat gil ḥuquq al-insan
Dirasat - Al-Ǧamiat al-urdunniyyat. Al-ulum al-tarbawiyyat
Magallaẗ al-Aqṣa
Maǧallaẗ abḥaṯ al-baṣraẗ. Al-ʻilmiyyat
Maǧalaẗ ṟisalaẗ al-ẖaliǧ al-arạbi
Magallaẗ ʿulum al-tarbiyyaẗ al-riyaḍiyyaẗ
"""
test_data2 = """Nicholson, R"""
# https://unicode-table.com/en/blocks/latin-1-supplement/
latin_supplment_data = """
¢ ¢ ö ö Õ Õ ã ã
"""
# https://unicode-table.com/en/blocks/latin-extended-a/
latin_extend_a_data = """
Ħ Ħ š š Ę Ę
"""
# https://unicode-table.com/en/blocks/latin-extended-b/
latin_extend_b_data = """
ƀ ƀ Ǎ Ǎ ǻ a ǻ
"""
# https://unicode-table.com/en/blocks/latin-extended-c/
# https://unicode-table.com/en/blocks/latin-extended-d/
# These two tables don't contain English letters associated with diacriticals.
test_build_dir = os.path.normpath(os.path.join(ROOTDIR, 'build'))

class DiacriticalsUnitTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.path.isdir(test_build_dir) and shutil.rmtree(test_build_dir)

    def test_collect_diacriticals_from_a_text(self):
        diac = Diacriticals()
        diacriticals = diac.diacritical_count(test_data, 'title')
        for k, v in diacriticals.items():
            print("{0}: {1}".format(k, v))

    def test_collect_latin_supplement_from_a_text(self):
        diac = Diacriticals()
        print('LATIN SUPPLEMENT')
        diacriticals = diac.diacritical_count(latin_supplment_data, 'title')
        for k, v in diacriticals.items():
            print("{0}: {1}".format(k, v))

    def test_collect_latin_extended_a_from_a_text(self):
        diac = Diacriticals()
        print('LATIN EXTENDED a')
        diacriticals = diac.diacritical_count(latin_extend_a_data, 'title')
        for k, v in diacriticals.items():
            print("{0}: {1}".format(k, v))

    def test_collect_latin_extended_b_from_a_text(self):
        diac = Diacriticals()
        print('LATIN EXTENDED b')
        diacriticals = diac.diacritical_count(latin_extend_b_data, 'title')
        for k, v in diacriticals.items():
            print("{0}: {1}".format(k, v))

    def test_create_build_dir_if_it_noneixsts(self):
        diac = Diacriticals()
        os.path.isdir(test_build_dir) and shutil.rmtree(test_build_dir)
        self.assertFalse(os.path.isdir(
            os.path.normpath(test_build_dir)
        ))

        diac.create_build_folder()
        self.assertTrue(os.path.isdir(
            os.path.normpath(test_build_dir)
        ))

    def test_remove_then_create_new_build_dir_if_it_exists_already(self):
        os.path.isdir(test_build_dir) or os.mkdir(test_build_dir)
        self.assertTrue(os.path.isdir(
            os.path.normpath(test_build_dir)
        ))
        diac = Diacriticals()
        self.assertTrue(os.path.isdir(
            os.path.normpath(test_build_dir)
        ))

    def test_remove_build_dir_even_it_not_empty(self):
        os.path.isdir(test_build_dir) or os.mkdir(test_build_dir)
        open(os.path.normpath(os.path.join(test_build_dir, 'temp.txt')), 'w').close()
        self.assertGreater(len(os.listdir(test_build_dir)), 0)

        diac = Diacriticals()
        self.assertTrue(os.path.isdir(
            os.path.normpath(test_build_dir)
        ))

    def test_raise_an_exception_if_we_specif_an_invalid_location(self):
        diac = Diacriticals()
        self.assertIsNone(diac.data_dir)
        with self.assertRaises(OSError):
            diac.data_dir = "./nonexist/"

    def test_collect_gz_paths(self):
        pass


    @classmethod
    def tearDownClass(cls):
        os.path.isdir(test_build_dir) and shutil.rmtree(test_build_dir)



if __name__ == '__main__':
    unittest.main()
