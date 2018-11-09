#!/bin/bash

set -x

mkdir -p test_HLTprescales/

## example 1
# print all HLT summary columns for given comma separated list of paths
./printHLTPrescales.py --mode l1_hlt_circulatinghi2018/v12 --pathnames HLT_Physics_v7,HLT_Random_v3,HLT_ZeroBias_v6 &> test_HLTprescales/example1.log

## example 2
# print 2nd,5th, and 6th column from HLT Pre-scale Set table
./printHLTPrescales.py --mode l1_hlt_HI_Collisions/v77 --pathnames HLT_HIPuAK4CaloJet40_Eta5p1_v1,HLT_HIPuAK4CaloJet60_Eta5p1_v1,HLT_HIPuAK4CaloJet80_Eta5p1_v1 --colIndex 2,4,5,6,7 &> test_HLTprescales/example2.log

## example 3
# HLT paths to search are in a txt file
# print first 8 columns from HLT Pre-scale Set table
./printHLTPrescales.py --mode l1_hlt_heavyiontest2018-hfminbias17-19/v2 --pathnames test_HLTprescales/HLTpaths.txt --colIndex 1,2,3,4,5,6,7,8 &> test_HLTprescales/example3.log

## example 4
# print first 10 columns from HLT Pre-scale Set table
# save the output to a csv file
./printHLTPrescales.py --mode l1_hlt_circulatinghi2018/v12 --pathnames HLT_Physics_v7,HLT_Random_v3,HLT_ZeroBias_v6 --colIndex 1,2,3,4,5,6,7,8,9,10 --outcsv test_HLTprescales/example4.csv &> test_HLTprescales/example4.log

## example 5
# HLT paths to search are in a txt file
# print all columns from HLT Pre-scale Set table
# save the output to a csv file
./printHLTPrescales.py --mode l1_hlt_collisionshi2018/v34 --pathnames test_HLTprescales/HLTpaths.txt --outcsv test_HLTprescales/example5.csv &> test_HLTprescales/example5.log
