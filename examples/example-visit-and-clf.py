#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Sample program to iterate through docs via visit and run classifier on text
#
# pre-requisites:
# > pip install numpy transformers torch
#
#

from pprint import pprint
import sys

import numpy as np
from transformers import pipeline

import venra


# initialize pre-trained model and pipeline
global pipe
model_name = "valhalla/distilbart-mnli-12-9"
pipe = pipeline("zero-shot-classification", model=model_name)


def classify(doc_text):
    """Return (class, score) via zero shot classification for text on incoming doc
    """
    labels = ["programming", "business", "culture", "productivity"]

    # run classification
    sequences = (doc_text, )
    res = pipe(sequences=sequences, candidate_labels=labels)

    # extract class
    idx = np.argmax(res["scores"])
    cls = res["labels"][idx]
    score = res["scores"][idx]

    return (cls, score)


if __name__ == "__main__":

    # usage
    if len(sys.argv) != 4:
        print("")
        print("Usage:")
        print("> ./example-visit-docs.py <namespace> <doctype> <text-field-name>")
        print("")
        print("Example:")
        print('> export VESPA_HOST_APP="http://192.168.100.30:8080"')
        print("> ./example-visit-docs.py fruitdocs orange text")
        print("")
        sys.exit(1)

    # params
    namespace = sys.argv[1]
    doctype = sys.argv[2]
    text_field_name = sys.argv[3]

    # load host env vars
    venra.config.load_overrides_from_env()

    # visit, classify, and print to the limit
    # note: this non-batching approach is inefficient and just for illustration
    limit = 50
    cl_count = 0
    for i, d in enumerate(venra.visit.feed(namespace, doctype, fields_only=False)):

        # stop after limit is reached
        if i > limit:
            print(f"reached limit: {limit}")
            break

        # run classification
        if text_field_name in d["fields"]:
            cls, score = classify(d["fields"][text_field_name])
            print(f"::> {d['id']} :: class {score:.5f} @ {cls}")
            cl_count += 1
        else:
            print(f"::> {d['id']} :: no text field")


