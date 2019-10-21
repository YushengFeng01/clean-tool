# -*- coding: utf-8 -*-

import unittest

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


class TestCollectNonAscii(unittest.TestCase):
    def test_collect_non_ascii(self):
        diac = Diacriticals()
        diacriticals = diac.diacritical_count(test_data)
        for k, v in diacriticals.items():
            print("{0}: {1}".format(k, v))



if __name__ == '__main__':
    unittest.main()
