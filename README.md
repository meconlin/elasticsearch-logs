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

1 {"query":{"match_all":{}}}
2 {"query":{"match_all":{}},"facets":{"f1":{"terms":{"field":"description"}}},"size":0}

```

#### Requirements
Be sure to pip install -r requirements.txt to install [PrettyTable](https://pypi.python.org/pypi/PrettyTable)

#### Expected Log Format

```

[2013-11-15 13:17:22,770][TRACE][index.search.slowlog.query] [<node name>] [<index name>][<shard>] took[1.7ms], took_millis[1], types[sunrise], stats[], search_type[QUERY_THEN_FETCH], total_shards[2], source[{"query":{"match_all":{}},"size":10}], extra_source[],

```
