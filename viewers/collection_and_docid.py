# -*- coding: utf-8 -*-
from lxml import etree

SAMPLE1 = '/home/skywalker/temp_work/clean-tool/XML/batch14/collection=ARCI/part-0.gz'
SAMPLE2 = '/home/skywalker/temp_work/clean-tool/XML/batch14/collection=SUPERUNIF/part-00284-2e3e27cd-bcce-4764-a0c7-81dca7db6a5b-c000.txt.gz'

DOCID_IN_UNIF_XPATH = '/REC/doc_id'
DOCID_IN_ARCI_XPATH = '/REC/static_data/summary/EWUID/WUID/@doc_id'

def collection(gz_path):
    collection = gz_path.rpartition('collection=')[2].split('/')[0]
    print(collection)

def doc_id(xml_doc, collection):
    tree = etree.parse(xml_doc)

    if collection == 'SUPERUNIF':
        doc_id = tree.xpath(DOCID_IN_UNIF_XPATH)
        ids = [i.text for i in doc_id]
    elif collection == 'ARCI':
        doc_id = tree.xpath(DOCID_IN_ARCI_XPATH)
        ids = [i for i in doc_id]

    return id



if __name__ == '__main__':
    # collection(SAMPLE1)
    # collection(SAMPLE2)

    doc_id('../superunif_sample.xml', 'SUPERUNIF')
    doc_id('../arci_sample.xml', 'ARCI')