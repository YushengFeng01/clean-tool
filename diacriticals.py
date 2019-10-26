# -*- coding: utf-8 -*-
'''
This module is used to retrieve diacritical characters from our arci and superunif data.
'''
import logging
from logging.handlers import RotatingFileHandler
from collections import OrderedDict, defaultdict
import multiprocessing
import unicodedata
import StringIO
import argparse
import signal
import shutil
import gzip
import sys
import csv
import re
import os

from lxml import etree

ROOTDIR = os.path.normpath((os.path.dirname(__file__)))
children_pids = []

def build_logger(name="diacriticals"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        file_name = os.path.normpath(os.path.join(ROOTDIR, name+'.log'))
        fh = RotatingFileHandler(file_name, mode="a", maxBytes=100*1024*1024, backupCount=10, encoding=None, delay=0)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger

def build_child_logger(name):
    Diacriticals.BUILD_DIR = os.path.normpath(os.path.join(ROOTDIR, 'build'))
    if not os.path.isdir(Diacriticals.BUILD_DIR):
        raise OSError("{0} doesn't exist. Faild to create it.".format(Diacriticals.BUILD_DIR))

    log_dir = os.path.normpath(os.path.join(Diacriticals.BUILD_DIR, 'logs'))
    os.path.isdir(log_dir) or os.mkdir(log_dir)
    file_name = os.path.normpath(os.path.join(log_dir, name + '.log'))

    logger = logging.getLogger(name)
    # https://navaspot.wordpress.com/2015/09/22/same-log-messages-multiple-times-in-python-issue/
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        fh = RotatingFileHandler(file_name, mode="a", maxBytes=100 * 1024 * 1024, backupCount=10, encoding=None, delay=0)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger

class Diacriticals(object):
    NON_ASCII_PATTERN = re.compile(ur'[^\u0000-\u007f]{1}', re.MULTILINE|re.UNICODE)
    TITLE_IN_ARCI_XPATH = '/REC/static_data/summary/titles/title[@transliterated=\'Y\']'
    NAME_IN_ARCI_XPATH = '/REC/static_data/summary/names/name[@transliterated=\'Y\']'
    TITLE_IN_UNIF_XPATH = '/REC/static_data/specific_content[@coll_id=\'ARCI\']/summary/titles/title[@transliterated=\'Y\']'
    NAME_IN_UNIF_XPATH = '/REC/static_data/specific_content[@coll_id=\'ARCI\']/summary/names/name[@transliterated=\'Y\']'
    DOCID_IN_UNIF_XPATH = '/REC/doc_id'
    DOCID_IN_ARCI_XPATH = '/REC/static_data/summary/EWUID/WUID/@doc_id'
    BUILD_DIR = os.path.normpath(os.path.join(ROOTDIR, 'build'))

    def __init__(self):
        super(Diacriticals, self).__init__()
        self._logger = build_logger()
        self.gz_path = None
        self._data_dir = None
        self._nproc = None
        self.create_build_folder()

    @property
    def data_dir(self):
        return self._data_dir

    @data_dir.setter
    def data_dir(self, data_dir):
        self._data_dir = os.path.normpath(os.path.abspath(os.path.realpath(os.path.expanduser(os.path.expandvars(data_dir)))))
        if not os.path.isdir(self._data_dir) or not os.access(self.data_dir, os.R_OK):
            self._logger.error("{0} doesn't exist or you have no permission to access it".format(data_dir))
            raise OSError("{0} doesn't exist or you have no permission to access it".format(data_dir))
        self._logger.info("xml data location: {0}".format(self._data_dir))

    @property
    def nproc(self):
        return self._nproc if self._nproc else multiprocessing.cpu_count()-2

    @nproc.setter
    def nproc(self, num):
        cpu_count = multiprocessing.cpu_count()
        if num < 0 or not num:
            self._nproc = cpu_count - 2
        elif num > cpu_count-2:
            self._nproc = cpu_count - 2
        else:
            self._nproc = num

    @staticmethod
    def diacritical_count(text):
        count = {}
        text_in_unicode = text.decode('utf-8') if not isinstance(text, unicode) else text
        text_in_unicode = unicodedata.normalize('NFKC', text_in_unicode)
        # latins = re.findall(Diacriticals.LATIN_EXTERNAL_PATTERN, text_in_unicode)
        latins = re.findall(Diacriticals.NON_ASCII_PATTERN, text_in_unicode)
        for d in latins:
            d = d.encode('utf-8')
            count.setdefault(d, 0)
            count[d] += 1
        return count, text_in_unicode

    @staticmethod
    def diacritical_child_report(count_dict, gz_file_path):
        output_dir = os.path.normpath(os.path.join(Diacriticals.BUILD_DIR, 'output'))
        pid = 'child_' + str(multiprocessing.current_process().pid) + '.csv'
        csv_report = os.path.normpath(os.path.join(output_dir, pid))
        has_report = os.access(csv_report, os.F_OK)
        with open(csv_report, 'a') as report:
            csv_writer = csv.DictWriter(report, fieldnames=['diacriticals', 'count', 'addition', 'collection', 'doc_id'])
            has_report or csv_writer.writeheader()
            for k, i in count_dict.items():
                f = list(i['Field'])
                e = i['Examples'].values()
                field_example = zip(f, e)
                f2 = ['|'.join([p[0], p[1]]) for p in field_example]
                f3 = '|'.join(f2)
                csv_writer.writerow({
                    'diacriticals': k,
                    'count': i['count'],
                    'addition': f3,
                    'collection': '/'.join(i['collection']),
                    'doc_id': ', '.join(i['doc_id'])
                })

    @staticmethod
    def child_signal_handler(num, frame):
        process = multiprocessing.current_process()
        pid = os.getpid()
        child_output = os.path.normpath(os.path.join(Diacriticals.BUILD_DIR, 'output'))
        status_f = os.path.normpath(os.path.join(child_output, str(pid) + '_killed'))
        open(status_f, 'w').close()
        process.terminate()
        process.join()
        sys.exit("PoolWorker {0} was killed by signal {1}".format(pid, num))

    @staticmethod
    def child_ready():
        child_output = os.path.normpath(os.path.join(Diacriticals.BUILD_DIR, 'output'))
        files = os.listdir(child_output)
        kill_status = [i for i in files if i.rpartition('_killed')[1]]
        return len(kill_status) == 0

    @staticmethod
    def union_addition_info(addition_info, new):
        tags = set(addition_info.split('|')[::2])
        new_tags = set(new.split('|')[::2])
        new_addition_info_l = new.split('|')
        extra_tags = list(new_tags - tags)
        for e in extra_tags:
            e_index = new_addition_info_l.index(e)
            extra_addition_info = '|'.join(new_addition_info_l[e_index:e_index + 2])
            addition_info = addition_info + '|' + extra_addition_info

        return addition_info

    def diacritical_report(self):
        count = {}
        addition = {}
        collection = {}
        doc_id = {}
        child_report_count = 0
        children_dir = os.path.normpath(os.path.join(Diacriticals.BUILD_DIR, 'output'))
        for root, subdir, files in os.walk(children_dir):
            for csv_file in files:
                report = os.path.normpath(os.path.join(root, csv_file))
                child_report_count += 1
                with open(report, 'r') as csv_report:
                    csv_reader = csv.DictReader(csv_report)
                    for row in csv_reader:
                        k = row['diacriticals']
                        count.setdefault(k, 0)
                        count[k] += int(row['count'])

                        collection.setdefault(k, set())
                        collection[k].add(row['collection'])

                        doc_id.setdefault(k, set())
                        doc_id[k].add(row['doc_id'])

                        if k in addition:
                            addition[k] = Diacriticals.union_addition_info(addition[k], row['addition'])
                        else:
                              addition[k] = row['addition']

        self._logger.info("{0} child reports are in {1}".format(child_report_count, children_dir))
        count = OrderedDict(sorted(count.items(), key=lambda t:t[1], reverse=True))
        self._logger.info("There are {0} diacriticals in arci and superunif data.".format(len(count)))
        report = os.path.normpath(os.path.join(Diacriticals.BUILD_DIR, 'diacritical_count.txt'))
        with open(report, 'w') as file:
            for k, v in count.items():
                unicode_char = k if isinstance(k, unicode) else k.decode('utf-8')
                unicode_name = unicodedata.name(unicode_char)
                # https://stackoverflow.com/questions/7291120/get-unicode-code-point-of-a-character-using-python
                code_point = unicode_char.encode('unicode_escape')
                c_ = '/'.join(list(collection[k]))
                ids = ', '.join(list(doc_id[k]))
                id_count = len(ids.split(', '))
                file.write(k+'|'+' '*5+str(v)+'|'+' '*5+code_point+'|'+ ' '*5+unicode_name.lower()+'|'+' '*5+c_+'|'+' '*5+str(id_count)+'|'+' '*5+ids+'|'+' '*5+addition[k]+'\n')


    def create_build_folder(self):
        try:
            os.path.isdir(Diacriticals.BUILD_DIR) and shutil.rmtree(Diacriticals.BUILD_DIR)
            os.path.isdir(Diacriticals.BUILD_DIR) or os.mkdir(Diacriticals.BUILD_DIR)
        except Exception as e:
            self._logger.error(e)
            raise OSError("Failed to remove the folder {0}, other program may be using it. Look into {1} for more details.".format(
                Diacriticals.BUILD_DIR, "diacriticals.log"
            ))

    def collect_gz_paths(self):
        if self.data_dir:
            self.gz_path = os.path.normpath(os.path.join(Diacriticals.BUILD_DIR, os.path.basename(self.data_dir)))
            self.gz_path = os.path.normpath(self.gz_path+'.txt')
            with open(self.gz_path, 'w') as f:
                for root, subdir, files in os.walk(self.data_dir):
                    for f_ in files:
                        if f_.endswith('.gz'):
                            p_ = os.path.normpath(os.path.join(root, f_))
                            p_ = os.path.normpath(p_ + '\n')
                            f.write(p_)
        else:
            self._logger.error("You hasn't specify a data direcotry yet.")
            raise TypeError("You hasn't specify a data direcotry yet.")

    @staticmethod
    def main_terminate(num, frame):
        logger = build_logger()
        for child in children_pids:
            try:
                os.kill(child, signal.SIGTERM)
            except:
                pass
        logger.warn("Main pid {0} was killed".format(os.getpid()))
        os._exit(0)

    @staticmethod
    def child_terminate(num, frame):
        pid = os.getpid()
        logger = build_child_logger(name=str(pid))
        logger.warn("child process {0} was killed by signal {1}".format(pid, num))
        os._exit(0)

    def start(self,func):
        if self.gz_path:
            signal.signal(signal.SIGTERM, Diacriticals.main_terminate)
            signal.signal(signal.SIGINT, Diacriticals.main_terminate)
            self._logger.info("The main pid is {0}".format(os.getpid()))

            output_dir = os.path.normpath(os.path.join(Diacriticals.BUILD_DIR, 'output'))
            os.path.isdir(output_dir) or os.mkdir(output_dir)

            q4jsondata = multiprocessing.Queue(1280)
            for i in range(0, self.nproc):
                pid = os.fork()
                if (pid == 0):
                    rval = func(q4jsondata)
                    os._exit(rval)
                else:
                    children_pids.append(pid)
                    self._logger.info("child {0} starts running".format(pid))

            with open(self.gz_path, 'r') as gz_files:
                for gz in gz_files:
                    q4jsondata.put(gz, block=True, timeout=1200)

            for i in range(0, self.nproc):
                try:
                    os.wait()
                except:
                    pass

            Diacriticals.child_ready() and self.diacritical_report()
        else:
            self._logger.error("no gz path txt file under build folder.")

    @staticmethod
    def extract_doc_id(xml_doc, collection):
        tree = etree.parse(xml_doc)
        ids = []

        if collection == 'SUPERUNIF':
            doc_id = tree.xpath(Diacriticals.DOCID_IN_UNIF_XPATH)
            ids = [i.text for i in doc_id]
        elif collection == 'ARCI':
            doc_id = tree.xpath(Diacriticals.DOCID_IN_ARCI_XPATH)
            ids = [i for i in doc_id]

        return list(set(ids))[0]

    @staticmethod
    def collect_diacriticals(q4jsondata):
        logger = build_child_logger(name=str(os.getpid()))
        signal.signal(signal.SIGTERM, Diacriticals.child_terminate)
        signal.signal(signal.SIGINT, Diacriticals.child_terminate)

        while True:
            try:
                gz_path = q4jsondata.get(block=True, timeout=20)
            except:
                # Queue is empty, and child should exit.
                os._exit(0)

            gz_path = os.path.normpath(gz_path.strip())

            if Diacriticals.child_ready():
                diacritical_count = {}
                logger.info(gz_path)
                with gzip.open(gz_path, 'rb') as gz_file:
                    collection = gz_path.rpartition('collection=')[2].split('/')[0]
                    for record in gz_file:
                        if len(record) < 1:
                            continue

                        # TODO: extract doc_id.
                        id = Diacriticals.extract_doc_id(StringIO.StringIO(record), collection)

                        tree = etree.parse(StringIO.StringIO(record))

                        # Collect diacriticals from "title" elements in arci and superunif xml data.
                        for xp in (Diacriticals.TITLE_IN_ARCI_XPATH, Diacriticals.TITLE_IN_UNIF_XPATH):
                            titles = tree.xpath(xp)
                            if len(titles):
                                for t in titles:
                                    count_, text_in_unicode = Diacriticals.diacritical_count(t.text)
                                    for k, v in count_.items():
                                        diacritical_count.setdefault(k, {})
                                        diacritical_count[k].setdefault('count', 0)
                                        diacritical_count[k]['count'] += v

                                        diacritical_count[k].setdefault('collection', [])
                                        collection in diacritical_count[k]['collection'] or diacritical_count[k]['collection'].append(collection)

                                        diacritical_count[k].setdefault('doc_id', [])
                                        id in diacritical_count[k]['doc_id'] or diacritical_count[k]['doc_id'].append(id)

                                        diacritical_count[k].setdefault('Field', set())
                                        if 'type' in t.attrib:
                                            tag = t.tag + '_' + t.attrib['type']
                                        else:
                                            tag = t.tag
                                        diacritical_count[k]['Field'].add(tag)

                                        diacritical_count[k].setdefault('Examples', {})
                                        examples = diacritical_count[k]['Examples']
                                        if t.tag not in examples:
                                            t_ = t.text.encode('utf-8') if isinstance(t.text, unicode) else t.text
                                            examples[t.tag] = t_

                        # Collect diacriticals from the children of "name" elements in arci and superunif xml data.
                        for xp in (Diacriticals.NAME_IN_ARCI_XPATH, Diacriticals.NAME_IN_UNIF_XPATH):
                            names = tree.xpath(xp)
                            if len(names):
                                for name in names:
                                    for child in name:
                                        count_, text_in_unicode = Diacriticals.diacritical_count(child.text)
                                        for k, v in count_.items():
                                            diacritical_count.setdefault(k, {})
                                            diacritical_count[k].setdefault('count', 0)
                                            diacritical_count[k]['count'] += v

                                            diacritical_count[k].setdefault('collection', [])
                                            collection in diacritical_count[k]['collection'] or diacritical_count[k]['collection'].append(collection)

                                            diacritical_count[k].setdefault('doc_id', [])
                                            id in diacritical_count[k]['doc_id'] or diacritical_count[k]['doc_id'].append(id)

                                            diacritical_count[k].setdefault('Field', set())
                                            diacritical_count[k]['Field'].add(child.tag)

                                            diacritical_count[k].setdefault('Examples', {})
                                            examples = diacritical_count[k]['Examples']
                                            if child.tag not in examples:
                                                t_ = child.text.encode('utf-8') if isinstance(child.text, unicode) else child.text
                                                examples[child.tag] = t_

                Diacriticals.diacritical_child_report(diacritical_count, gz_path)

__all__ = [
    'Diacriticals',
    'ROOTDIR',
]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--data_dir', help='The root dir of json gz data files.', required=True, default="")
    parser.add_argument('-n', '--procnum', help='The number of child processes used to collect diacriticals.', required=False, default=None)
    args = parser.parse_args()

    diac = Diacriticals()
    diac.data_dir = args.data_dir
    diac.nproc = args.procnum
    diac.collect_gz_paths()
    diac.start(Diacriticals.collect_diacriticals)
