## venra

[![Project Status: WIP](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
![Tests](https://github.com/codycollier/venra/workflows/Tests/badge.svg)
![Release](https://github.com/codycollier/venra/workflows/Python%20Package%20Release/badge.svg)
[![PyPI version](https://badge.fury.io/py/venra.svg)](https://badge.fury.io/py/venra)


Venra is a python client library for [vespa.ai](https://vespa.ai). It provides
a high-level api for interacting with Vespa's query, document, and system apis.


Note: This library is under active development and the api is currently unstable.



### Install

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
response = vquery.search(qdata)

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
user_query = "foo bar baz"
vconfig.vespa_host_app = "http://some.host.here:8080/search/"

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


