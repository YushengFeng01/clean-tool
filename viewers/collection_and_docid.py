# -*- coding: utf-8 -*-
import gzip
import StringIO

from lxml import etree

SAMPLE1 = '/home/skywalker/temp_work/clean-tool/XML/batch14/collection=ARCI/part-0.gz'
SAMPLE2 = '/home/skywalker/temp_work/clean-tool/XML/batch14/collection=SUPERUNIF/part-00284-2e3e27cd-bcce-4764-a0c7-81dca7db6a5b-c000.txt.gz'

DOCID_IN_UNIF_XPATH = '/REC/doc_id'
DOCID_IN_ARCI_XPATH = '/REC/static_data/summary/EWUID/WUID/@doc_id'

TITLE_IN_ARCI_XPATH = '/REC/static_data/summary/titles/title[@transliterated=\'Y\']'
TITLE_IN_UNIF_XPATH = '/REC/static_data/specific_content[@coll_id=\'ARCI\']/summary/titles/title[@transliterated=\'Y\']'

def collection(gz_path):
    collection = gz_path.rpartition('collection=')[2].split('/')[0]
    print(collection)

def doc_id(xml_doc, collection):
    tree = etree.parse(xml_doc)
    ids = None

    if collection == 'SUPERUNIF':
        doc_id = tree.xpath(DOCID_IN_UNIF_XPATH)
        ids = [i.text for i in doc_id]
    elif collection == 'ARCI':
        doc_id = tree.xpath(DOCID_IN_ARCI_XPATH)
        ids = [i for i in doc_id]

    return ids

def extract_title_type(xml, collection):
    tree = etree.parse(xml)
    titles = None

    if collection.upper() == 'ARCI':
        titles = tree.xpath(TITLE_IN_ARCI_XPATH)
    elif collection.upper() == 'SUPERUNIF':
        titles = tree.xpath(TITLE_IN_UNIF_XPATH)

    print(titles[0].attrib)

def check_extract_title_type():
    step = 0
    with open('../build/XML.txt', 'r') as gz_paths:
        for gz_path in gz_paths:
            step += 1
            with gzip.open(gz_path.strip(), 'rb') as records:
                for r in records:
                    if not len(r):
                        continue

                    tree = etree.parse(StringIO.StringIO(r))
                    titles = tree.xpath(TITLE_IN_UNIF_XPATH)
                    if len(titles):
                        print('superunif: {0}'.format([i.attrib for i in titles]))

                    titles = tree.xpath(TITLE_IN_ARCI_XPATH)
                    if len(titles):
                        print('arci: {0}'.format([i.attrib for i in titles]))

            if step > 10:
                break





if __name__ == '__main__':
    # collection(SAMPLE1)
    # collection(SAMPLE2)

    # doc_id('../superunif_sample.xml', 'SUPERUNIF')
    # doc_id('../arci_sample.xml', 'ARCI')

    # extract_title_type('../arci_sample.xml', 'ARCI')
    # extract_title_type('../superunif_sample.xml', 'SUPERUNIF')

    check_extract_title_type()