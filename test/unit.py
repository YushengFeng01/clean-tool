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
test_build_dir = os.path.normpath(os.path.join(ROOTDIR, 'build'))

class DiacriticalsUnitTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.path.isdir(test_build_dir) and shutil.rmtree(test_build_dir)

    def test_collect_diacriticals_from_a_text(self):
        diac = Diacriticals()
        diacriticals = diac.diacritical_count(test_data)
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
        diac.create_build_folder()
        self.assertTrue(os.path.isdir(
            os.path.normpath(test_build_dir)
        ))

    def test_remove_build_dir_even_it_not_empty(self):
        os.path.isdir(test_build_dir) or os.mkdir(test_build_dir)
        open(os.path.normpath(os.path.join(test_build_dir, 'temp.txt')), 'w').close()
        self.assertGreater(len(os.listdir(test_build_dir)), 0)

        diac = Diacriticals()
        diac.create_build_folder()
        self.assertTrue(os.path.isdir(
            os.path.normpath(test_build_dir)
        ))

    def test_raise_an_exception_if_we_specif_an_invalid_location(self):
        diac = Diacriticals()
        self.assertIsNone(diac.data_dir)
        with self.assertRaises(OSError):
            diac.data_dir = "./nonexist/"

    def test_collect_gz_paths_in_data_directory(self):
        diac = Diacriticals()
        diac.create_build_folder()
        with self.assertRaises(TypeError):
            diac.collect_gz_paths()

        diac.data_dir = 'arci_data'
        diac.collect_gz_paths()
        p = os.path.normpath(os.path.join(test_build_dir, 'arci_data.txt'))
        self.assertTrue(os.access(p, os.F_OK))
        with open(p, 'r') as f:
            gz_path = [_.strip() for _ in f]
        self.assertListEqual(gz_path, [os.path.normpath(os.path.join(diac.data_dir, 'arci.gz')),
            os.path.normpath(os.path.join(diac.data_dir, 'superunif.txt.gz'))])


    @classmethod
    def tearDownClass(cls):
        os.path.isdir(test_build_dir) and shutil.rmtree(test_build_dir)



if __name__ == '__main__':
    unittest.main()
