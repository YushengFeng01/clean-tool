# -*- coding: utf-8 -*-
import gzip
import StringIO

from lxml import etree

UT_IN_ARCI_XPATH = '/REC/static_data/summary[@type=\'src\']/EWUID/@uid'
UT_IN_SUPERUNIF_XPATH = '/REC/static_data/specific_content/summary[@type=\'src\']/EWUID/@uid'

def extract_ut_from_xml(xml, collection):
    uts = None
    tree = etree.parse(xml)
    if collection.upper() == 'ARCI':
        uts = tree.xpath(UT_IN_ARCI_XPATH)
    elif collection.upper() == 'SUPERUNIF':
        uts = tree.xpath(UT_IN_SUPERUNIF_XPATH)

    return uts

def check_textract_ut_from_xml():
    step = 0
    with open('../build/XML.txt', 'r') as xml_paths:
        for path in xml_paths:
            with gzip.open(path.strip(), 'rb') as gz_file:
                for record in gz_file:
                    if not len(record):
                        continue

                    tree = etree.parse(StringIO.StringIO(record))
                    uts = tree.xpath(UT_IN_ARCI_XPATH)
                    if len(uts):
                        print('ARCI: {0}'.format(uts))

                    uts = tree.xpath(UT_IN_SUPERUNIF_XPATH)
                    if len(uts):
                        print('SUPERUNIF: {0}'.format(uts))

            step += 1
            if step > 20:
                break


if __name__ == '__main__':
   uts = extract_ut_from_xml('../arci_sample.xml', 'ARCI')
   print('arci: {0}'.format(uts))

   uts = extract_ut_from_xml('../superunif_sample.xml', 'SUPERUNIF')
   print(uts)

   check_textract_ut_from_xml()