# -*- coding: utf-8 -*-
import unittest
import shutil
import time
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

class TestCollectDiacriticals(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.path.isdir(test_build_dir) and shutil.rmtree(test_build_dir)

    def test_collect_diacriticals_from_arci(self):
        diac = Diacriticals()
        diac.create_build_folder()
        diac.data_dir = 'D:\\dev\\normlize_and_folding\\arci_data'
        collect_diacriticals("D:\dev\\normlize_and_folding\\arci_data\\arci.gz")
        collect_diacriticals("D:\dev\\normlize_and_folding\\arci_data\\superunif.txt.gz")


if __name__ == '__main__':
    unittest.main()