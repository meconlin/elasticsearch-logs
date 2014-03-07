
import sys
import logging
import time
import re
import json
import hashlib

from prettytable import PrettyTable

# create logger
logger = logging.getLogger('slow_log_report')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(ch)

"""
Elasticsearch slow log parser
Parse an ES slow log and get a results showing common slow queries and the top 10 slowest queries

example output:
+-------+-------+---------+-----+-----+
| query | count | average | min | max |
+-------+-------+---------+-----+-----+
| 1     | 8     | 52.875  | 1   | 221 |
| 2     | 1     | 165.0   | 165 | 165 |
+-------+-------+---------+-----+-----+

1 {"query":{"match_all":{}}}
2 {"query":{"match_all":{}},"facets":{"f1":{"terms":{"field":"description"}}},"size":0}
"""

def _find_stuff_inside_brackets(text):
	return map(''.join, re.findall(r'\[(.*?)\]', text))

def _parse_node_and_indices(text):
	"""
	Get the node name and indices list from this piece of text
	Returns then as tuple (node, [indices])
	"""
	arr =  _find_stuff_inside_brackets(text)
	return arr[3],[arr[4]]

def _parse_took_millis(text):
	"""
	Get the millis as a number from this piece of text
	"""
	arr =  _find_stuff_inside_brackets(text)
	return arr[0]

def _parse_query(text):
	"""
	get the query as a string from the this piece of text
	"""
	arr =  _find_stuff_inside_brackets(text)
	return arr[0]

def _avg(list):
	"""
	calc average from a list
	"""
	return reduce(lambda x, y: x + y / float(len(list)), list, 0)

def _pretty_print(data):
	print 

	"""
	Display stats table for all queries
	Print full queries 
	"""
	x = PrettyTable(["query", "count", "average", "min", "max"])
	x.align = "l"
	ord_queries = []
	for k, v in data.iteritems():
		#print hashlib.md5(k).hexdigest()
		ord_queries.append(k)
		x.add_row([len(ord_queries),v["count"], v["avg"], v["min"], v["max"]])

	print x.get_string(sortby="count", reversesort=True)
	print 

	for idx, val in enumerate(ord_queries):
		print idx+1, val

	print

def read_file(fname):
	"""
	Read the log file, parse into query, count, and time stats
	"""
	query_hist = {}
	parsed = {}

	# query as key : {count:0, times:[]}

	with open(fname) as f:
		for line in f:
			arr = line.split(', ')
			node_and_indices = _parse_node_and_indices(arr[0])
			millis = _parse_took_millis(arr[1])
			query = _parse_query(arr[6])

			sub = query_hist.get(query, {"count":0,"times":[]})
			sub["count"] += 1
			sub["times"].append(int(millis))
			query_hist[query] = sub

	# add averages
	for key, sub in query_hist.iteritems():
		sub["avg"] = _avg(sub["times"])
		sub["min"] = min(sub["times"])
		sub["max"] = max(sub["times"])

	_pretty_print(query_hist)

if __name__ == '__main__':
	if len(sys.argv) <= 1:
		logger.debug("Usage : python slow_log_report.py <filename>")
		sys.exit(1)

	logger.info( "START : slow_log_report ")
	logger.info("-------------------------")
	start = time.time()
	filename = sys.argv[1]
	read_file(filename)
	end = time.time()
	duration = end - start

	logger.info("-------------------------")
	logger.info( "DONE : slow_log_report : took : %d (minutes) "%(duration/60) )