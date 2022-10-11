## venra

[![Project Status: WIP](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
![Tests](https://github.com/codycollier/venra/workflows/Tests/badge.svg)
![Release](https://github.com/codycollier/venra/workflows/Python%20Package%20Release/badge.svg)
[![PyPI version](https://badge.fury.io/py/venra.svg)](https://badge.fury.io/py/venra)


Venra provides a simple, high-level api for [vespa.ai](https://vespa.ai).

Venra targets subsets of Vespa's query, document, and system apis. It aims to 
encapsulate the complexity of dealing with the Vespa http interfaces, response
behaviors, and json responses for common client tasks.

Venra is well suited for web backends, command line tools, and enrichment
programs which need to retrieve, process, and update documents.


```python
import venra

qdata = {}
qdata["yql"] = "select * from sources awesome_docs;"
response = venra.query.search(qdata)

docs = venra.query.extract_docs(response)
for r, doc in enumerate(docs):
    print(f"rank: {r} >> {doc.some_id} title: {doc.title}")
```

Note: This library is under active development and the api is currently unstable.



### Installation

```bash
$ pip install venra
```


### Usage


Basic Query:

```python

import venra

# Build query
qdata = {}
qdata["yql"] = "select * from sources baz;"

# Run query
response = venra.query.search(qdata)

# Extract results via helpers
metrics = venra.query.extract_metrics(response)
docs = venra.query.extract_docs(response)

```


User Query and Grouping:
```python

from pprint import pprint

from venra import config as vconfig
from venra import query as vquery


# Configure
user_query = "machine learning"
vconfig.vespa_host_app = "http://localhost:8080"

# Build query including a grouping
qdata = {}
qdata["yql"] = "select post_id, post_date from sources baz where userQuery()"
qdata["yql"] += f" | all(group(time.date(post_date)) order(-max(post_date)) max(32) each(output(count())) as(day_counts) );"
qdata["hits"] = 10
qdata["timeout"] = "3300ms"
qdata["model.queryString"] = user_query
qdata["model.type"] = "weakAnd"
qdata["presentation.summary"] = "full"
qdata["presentation.timing"] = "true"

# Run query
response = vquery.search(qdata)

# Extract results via helpers
metrics = vquery.extract_metrics(response)
groups = vquery.extract_groups(response)
myfacet = vquery.extract_group_pairs(groups, "day_counts", "count()")
docs = vquery.extract_docs(response)

# Query results ready for use in app
pprint(metrics)
pprint(myfacet)
pprint(docs)
```


