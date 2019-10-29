## ChangedLog
#### 2019-10-22
* Add unicode name in the final report.
* Add "Field", "Example" in the  child process csv report.

#### 2019-10-23
* Add "Field" and "Example" columns in the report.

#### 2019-10-25
* Add "Collection" and "Doc_id" columns in the report

#### 2019-10-26
* sort the field and example columns
* add "ut" and "ut_count" columns
* check title type: the title containing `trasnliterated='Y'` are all source type so far.

## TODO:
~~1. Add columns **unicode, field and example**~~

~~1. The "Field" and "Example" should be like this: `{"title":"...", "wos_standard":"", "display_name":""}`~~

~~2. Modify the process of gerneating final report.~~
~~3. Some characters don't appear in excel.~~

~~1. Add "collection" and "doc id" columns after each "Example" column.~~
~~1. List `type` attriutes for each title field in the report.~~
~~1. Add a "UT" column in the report.~~ 
~~2. Explain why line 152 in report_v1.3.2 has  no ut.~~
~~4. Dedup doc_id list and ut_list columns.~~
~~5. **Some record's type aren't `src` in superunfi. So the ut field is empty for some characters, especially the name element in superunif. Add type='src' into UNIF XPATH?**~~
6. `sort_addition_info`, its logic is a little complicated. I need to simplify it later. The name elements may contain more children.
7. Add more unit test cases, e.g `child process result validation`

## Cluster
cluster_1.snapshot.dev
curl -s -H 'Content-Type: application/json' -XGET 'elasticsearch.cluster_1.wos.us-west-2.snapshot.dev.oneplatform.build:9200/_cat/indices?v'
curl -s -H 'Content-Type: application/json' -XPOST 'elasticsearch.cluster_1.wos.us-west-2.snapshot.dev.oneplatform.build:9200/arci-201910160/_search?pretty' -d '
{
  "query" : {
     "bool": {
        "must": [
           { "match" : {"source" : "Dirasat wa abḥaṯ (Al-galfaẗ )"} }
        ]
     }
  }
}'