#!/bin/bash

# translate existing VRP-REP instance, write it to file
frvcpy-translate ../data/vrprep-instance.xml new-frvcp-instance.json

frvcpy --instance=new-frvcp-instance.json --route=0,40,12,33,38,16,0 --qinit=16000 --output=../results/my-solution.xml
# Duration: 7.339
# Energy-feasible route:
# [(0, None), (40, None), (12, None), (33, None), (48, 6673.379615520617), (38, None),(16, None), (0, None)]

