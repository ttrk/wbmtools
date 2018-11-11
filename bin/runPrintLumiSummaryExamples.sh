#!/bin/bash

set -x

## Columns in Lumi section table
# Index : Column Name
# ------:-----------
# 1     : LS
# 2     : Presc
# 3     : Time
# 4     : Inst
# 5     : Deliv
# 6     : Live
# 7     : Deadtime
# 8     : Beam 1
# 9     : Beam 2

mkdir -p test_LumiSummary/

## example 1
./printLumiSummary.py --run 326381 &> test_LumiSummary/example1.log

## example 2
./printLumiSummary.py --run 326381 --minLS 57 --maxLS 111 &> test_LumiSummary/example2.log

## example 3
# save the output to a csv file
./printLumiSummary.py --run 326476 --outcsv test_LumiSummary/example3.csv &> test_LumiSummary/example3.log

## example 4
# save the output to a csv file
./printLumiSummary.py --run 326398 --minLS 41 --maxLS 137 --outcsv test_LumiSummary/example4.csv &> test_LumiSummary/example4.log
