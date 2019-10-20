# -*- coding: utf-8 -*-
import unittest

from diacriticals import *


class FunctionalTest(unittest.TestCase):
    def test_retrieve_diacriticals_from_arci(self):
        # "aws s3 cp" arci or superunif json gz files into a directory, e.g "./data/arci"
        # Go to the folder where "diacritical.py" is and run this command "python diacriticals.py --datadir=./data/arci"
        # A folder called "build" appears. If a "build" folder already exists,
        # this script removes then creates a new "build" folder.
        diac = Diacriticals()
        diac.create_build_folder()

        # We download ARCI or superunif json gz files into a folder.
        # This script visit the folder.
        # If we specify an invalid location, the script will raise an OSError. You can find error info in the log file
        with self.assertRaises(OSError):
            diac.data_dir = 'nonexist_dir'

        # IF we specify an existence folder, but we have no permission to access it, the script will raise an OSError.
        # And you can find error info in the log file.

        # We have specified a valid data directory. There may be many files in this folder.
        # We collect all the gz file paths into a txt file in the "build" folder.
        # The name of this txt file should be the data directory name, e.g arci_data.txt
        # python diacriticals.py --data_dir=D:\\dev\\normlize_and_folding\\batch14
        diac.data_dir = 'D:\\dev\\normlize_and_folding\\batch14'
        diac.collect_gz_paths()

        # We have already collected all the gz file paths under the data directory.
        # We create multi child processes to process these gz files.
        # Each child process has a individual log file, named by its pid number.
        # We can kill the child process with its pid.

        # Now we start to handle each gz file in a child process.
        # We can find log and output files for each child process in build folder.
        # The log files for each child process are in "build/logs" folder.
        # The name of a log file is like this, "20836.log". 20836 is the child process' pid.
        # If the program is killed, remove the build folder.

        # This program is run on aws instance. We just kill the main pid, all the pool workers and main process
        # can be terminated due to the default signal handler.
        # This is quite different from Windows. We need to specify signal handlers to quit gracefully.
        # process.terminate() in pool just cancel the current job. It'll start again when new data
        # is ready.

        # This is the xml location: ip-10-152-12-68
        # /opt/reuters/data/elasticsearch/eileenx/ses-1372/

        # "title" and "name" elements contain the attribute "transliterated="Y"".
        # We collect diacriticals from "title" elements from arci and superunif xml records.
        # We collect diacriticals from the children of "name" elements from arci and superunif xml records.
        # Save the result in a csv file. The name of the csv result is the child pid.
        # Main pid aggregate the children results to generate the final report.
        diac.start(collect_diacriticals)



if __name__ == '__main__':
    unittest.main()
