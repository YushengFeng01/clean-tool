## Quick Start
* Copy the file "diacrictials.py", a Python2 script into a directory, e.g `~/temp_work/`
* Copy data files into a directory, e.g `~/temp_work/batch14`. **The data files are all gz files.**
* Run the python script: `nohup python diacriticals.py -d ./batch14 &`

You can find a folder `~/temp_work/build` when the program complete.
The file `~/temp_work/build/diacritical_count.txt` is the result report. You can use it as a csv file whose delimiter is `|`

## Specify the count of child process
Assume you machine has 12 cpu cores, this script would generate 10 (cpu_count-2) to collect diacriticals from xml data files by default.

Speicify 5 child processes:

`nohup python diacriticals.py -d ./batch14 -n 5`

Only generate 10 (cpu_count-2) child processes if the machine only has 12 cpu cores:

`nohup python diacriticals.py -d ./batch14 -n 32`

## Cancel the program immediately
1. Find the main pid of the program. You can find the main pid in the `~/temp_work/diacriticals.log` file

```
cat diacriticals.log
[ec2-user@ip-10-152-12-68 temp]$ cat diacriticals.log
2019-10-31 01:59:57,476 - diacriticals - INFO - xml data location: /opt/reuters/data/elasticsearch/arci_rosette/diacriticals/data
2019-10-31 01:59:57,519 - diacriticals - INFO - The main pid is 44279
2019-10-31 01:59:57,524 - diacriticals - INFO - child 44280 starts running
2019-10-31 01:59:57,525 - diacriticals - INFO - child 44281 starts running
2019-10-31 01:59:57,526 - diacriticals - INFO - child 44282 starts running
2019-10-31 01:59:57,527 - diacriticals - INFO - child 44283 starts running
2019-10-31 01:59:57,528 - diacriticals - INFO - child 44284 starts running
2019-10-31 01:59:57,528 - diacriticals - INFO - child 44285 starts running
2019-10-31 01:59:57,529 - diacriticals - INFO - child 44286 starts running
2019-10-31 01:59:57,530 - diacriticals - INFO - child 44287 starts running
2019-10-31 01:59:57,531 - diacriticals - INFO - child 44288 starts running
2019-10-31 01:59:57,532 - diacriticals - INFO - child 44289 starts running
2019-10-31 01:59:57,532 - diacriticals - INFO - child 44290 starts running
2019-10-31 01:59:57,533 - diacriticals - INFO - child 44291 starts running
2019-10-31 01:59:57,534 - diacriticals - INFO - child 44292 starts running
2019-10-31 01:59:57,535 - diacriticals - INFO - child 44293 starts running
2019-10-31 02:00:42,078 - diacriticals - INFO - 14 child reports are in build/output
2019-10-31 02:00:42,079 - diacriticals - INFO - There are 230 diacriticals in arci and superunif data.

```

2. Kill the main process `kill 44279`

## Note
The program depends on the hierarchical structure of the xml files completely. So you can't use this program directly if your xml structure is different from mine.

## Capture non-ascii characters
I use regular expression to capture non-ascii characters. I attach the code here for convenient.
```
NON_ASCII_PATTERN = re.compile(ur'[^\u0000-\u007f]{1}', re.MULTILINE|re.UNICODE)

def diacritical_count(text):
    count = {}
    text_in_unicode = text.decode('utf-8') if not isinstance(text, unicode) else text
    text_in_unicode = unicodedata.normalize('NFKC', text_in_unicode)
    latins = re.findall(Diacriticals.NON_ASCII_PATTERN, text_in_unicode)
    for d in latins:
        d = d.encode('utf-8')
        count.setdefault(d, 0)
        count[d] += 1
    return count, text_in_unicode
```
## Futional Test
I attach my own funtional test `functional_test.py` here as well. I hope it's helpful for you to run or refer this script.

Email me if you have any question about this script.

Yusheng.Feng@clarivate.com
