Elasticsearch-Logs 
==================================

Python script to parse elasticsearch logs.

#### slow_log_report.py
Parses slow query log and gathers count and time stats for each query.  

```
python slow_log_report.py resources/index_search_slowlog.log 

+-------+-------+---------+-----+-----+
| query | count | average | min | max |
+-------+-------+---------+-----+-----+
| 1     | 8     | 52.875  | 1   | 221 |
| 2     | 1     | 165.0   | 165 | 165 |
+-------+-------+---------+-----+-----+

1 {"query":{"match_all":{}},"facets":{"f1":{"facet_filter":{"exists":{"field":"answers.name"}},"term_list":{"fields":["answers.name"
2 {"query":{"match_all":{}},"facets":{"f1":{"term_facet_sample":{"field":"answers.name","size":5,"sample":0.1}}},"size":0}

```

### Requirements ###
Be sure to pip install -r requirements.txt to install [PrettyTable](https://pypi.python.org/pypi/PrettyTable)
