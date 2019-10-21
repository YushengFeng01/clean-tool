#-*- coding: utf-8 -*-
import multiprocessing
import unittest
import shutil
import os

from diacriticals import *


class DiacriticalFunctionalTest(unittest.TestCase):
    """
    Quick Start
        Copy the script "diacrictials.py" into a directory, e.g "~/temp_work/clean-tool"
        Copy the xml data files into a directory, e.g "~/temp_work/batch14"
        Run the python script like this: # nohup python diacriticals.py -d ./batch14
        Assume you machine had 12 cpu cores, this script would generate 10 (cpu count - 2)
        to collect diacriticals from xml data files.
        You can alse specify the number of child processes, like this:
        nohup python diacriticals.py -d ./batch14 -n 5 , speicify 5 child processes.
        nohup python diacriticals.py -d ./batch14 -n 32, still generate 10 child processes
        because your machine only has 12 cpu cores.

        This program generates an output folder, called "build". The file "diacritical_count.txt" is the report file.

        We can cancel the running script like this:
        # Get the main pid
        tail diacritical.log

        # 2019-10-20 16:42:09,256 - diacriticals - INFO - The main pid is 7705
        # kill the main process
        kill 7705
    """
    def test_collect_transliterated_characters_from_arci_and_superunif_xml(self):
        # This file generates a folder, called "build" first.
        # If a build folder already exists, it deletes it then creates a new one
        os.path.isdir('../build') and shutil.rmtree('../build')
        diac = Diacriticals()
        self.assertTrue(os.path.isdir('../build'))

        # This script receives and validate the options passed from command line.
        # It rase an exception is the data directory doesn't exist.
        with self.assertRaises(OSError):
            diac.data_dir = 'nonexist'

        # The data directory must exist and you have the permission to access it.
        diac.data_dir = '../batch14'

        # The number of child processes is from 1 to cpu_count-2
        # The default number of child porcesses is cpu_count-2
        cpu_count = multiprocessing.cpu_count()
        # If we specify a too large number, the actual number is cpu_count-2
        diac.nproc = cpu_count+10
        self.assertEqual(diac.nproc, cpu_count-2)

        # If we specify 0 or None, the actual number is still cpu_count-2
        diac.nproc = 0
        self.assertEqual(diac.nproc, cpu_count-2)
        diac.nproc = -2
        self.assertEqual(diac.nproc, cpu_count-2)

        # We can specify a number between 1 and cpu_count-2
        diac.nproc = 2 # The cpu_count is larger than 2
        self.assertEqual(diac.nproc, 2)

        # We specify 2 child processes to collect diacriticals.
        # The program collect all the file paths, which end with ".gz" in a txt file, named with
        # data directory base name, batch14.txt.
        diac.collect_gz_paths()
        self.assertTrue(os.access('../build/batch14.txt', os.F_OK))
        # The directory  "../batch14/collection=SUPERUNIF" has a file "_SUCCESS", it doesn't end with ".gz"
        # This file doesn't appear in "batch14.txt" file.
        with open('../build/batch14.txt', 'r') as f:
            gz_files = [i.strip() for i in f]
        self.assertNotIn('_SUCCESS', gz_files)
        no_gz_files = [i for i in gz_files if not i.endswith(".gz")]
        self.assertEqual(len(no_gz_files), 0)

        # The script generate 2 child porcesses to collect diacriticals from these gz files, listed in build/batch14.txt.
        # The script scans the "title" and "name" elements in the xml files, and collects all the non-ascii
        # character.
        diac.start(Diacriticals.collect_diacriticals)

        # The file build/diacritical_count.txt is the result report.
        self.assertTrue(os.access('../build/diacritical_count.txt', os.F_OK))



if __name__ == '__main__':
    unittest.main()
