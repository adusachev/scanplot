#!/bin/bash

size=$(du -m ./plot2data/pipeline.ipynb | awk '{print $1}')

if (($size > 100)); then
    echo "ok"
else
    echo "ne ok"
fi

