#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Sample program to iterate through docs via search, generate an embedding from 
# text in each document, and write the embedding back to a tensor field in the
# same document.
#
# Note, this sample is merely intended as a loose illustration, and also
# requires a tensor field to exist in the schema, along these lines:
#
#   # embedding for the text
#   field myembedding type tensor<float>(x[384]) {
#     indexing: attribute
#   }
#    
#
#

import sys

from sentence_transformers import SentenceTransformer
import venra


# Load the model at start time
model = SentenceTransformer("all-MiniLM-L6-v2")



if __name__ == "__main__":

    # usage
    if len(sys.argv) != 8:
        print("")
        print("Usage:")
        print("> ./example-query-and-embedding.py <doctype> <query> <doc-summary> <namespace> <docid-field> <text-field> <emb-field>")
        print("")
        print("Example:")
        print('> export VESPA_HOST_APP="http://192.168.100.30:8080"')
        print("> ./example-query-and-embedding.py fruitdocs orange full mydocs docidfieldname textfieldname tensorfieldname")
        print("")
        sys.exit(1)

    # params - query
    doctype = sys.argv[1]
    query = sys.argv[2]
    doc_summary = sys.argv[3]

    # params - embedding and doc update
    namespace = sys.argv[4]
    docid_field = sys.argv[5]
    text_field = sys.argv[6]
    emb_field = sys.argv[7]

    # load host env vars
    venra.config.load_overrides_from_env()

    # define query
    qdata = {}
    qdata["yql"] = f"select * from sources {doctype} where userQuery();"
    qdata["hits"] = 250
    qdata["model.queryString"] = f"{query}"
    qdata["model.type"] = "weakAnd"
    qdata["presentation.summary"] = f"{doc_summary}"


    # query and update loop
    limit = 3
    for i, d in enumerate(venra.query.feed(qdata, fields_only=True)):

        print(f"")
        if i >= limit:
            print(f"reached limit: {limit}")
            break

        print(f"::> {d[docid_field]} (fields:{len(d)})")

        if text_field not in d:
            print(f"> text field not found")
            continue

        # generate embedding
        embedding = model.encode(d[text_field]).tolist()
        print(f"> emb: {len(embedding)}")

        # update the document
        operations = [("assign", f"{emb_field}", {"values": embedding})]
        venra.document.update(namespace, doctype, d[docid_field], operations)
        print(f"> op: {str(operations)[:80]}...")

    print("")


