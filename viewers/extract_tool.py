# -*- coding: utf-8 -*-
import StringIO
import gzip
import csv
import os

from lxml import etree

class ExtractTool(object):
    def __init__(self):
        super(ExtractTool, self).__init__()

    def nodes(self, path, xpath):
        p = os.path.normpath(path)
        with open("./extract_result.csv", 'a') as r:
            csv_writer = csv.writer(r)
            with gzip.open(p, 'rb') as src:
                for i in src:
                    if len(i) < 1:
                        continue

                    tree = etree.parse(StringIO.StringIO(i))
                    elements = tree.xpath(xpath)
                    if len(elements):
                        for e in elements:
                            text = e[0].text
                            text = text.encode('utf-8') if isinstance(text, unicode) else text
                            csv_writer.writerow([text, path])

    def xml_paths(self, path):
        p = os.path.normpath(path)
        with open(p, 'r') as src:
            for i in src:
                self.nodes(i.strip(), "/REC/static_data/summary/titles/title[@transliterated=\'Y\'][@type=\'item\']")




if __name__ == '__main__':
    tool = ExtractTool()
    # tool.nodes("D:\\dev\\clean-tool\\ses-1372\\XML\\batch12\\collection=ARCI\\part-0.gz",
    #            "/REC/static_data/summary/titles/title[@transliterated=\'Y\'][@type=\'item\']")
    tool.xml_paths("/opt/reuters/data/elasticsearch/arci_rosette/diacriticals/clean-tool/build/498b-20191101040805.txt")