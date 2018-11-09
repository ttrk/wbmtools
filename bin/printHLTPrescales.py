#!/usr/bin/env python

import wbmtools.wbmutil as wbmutil
from wbmtools.wbmparser import WBMParser

wbmparser=WBMParser()

import argparse
parser = argparse.ArgumentParser(description='prints HLT Pre-scale details for a given trigger mode')
parser.add_argument('--mode',required=True,help='l1_hlt_collisionshi2018/v34')
parser.add_argument('--pathnames',required=True,help='HLT_HIPuAK4CaloJet40Eta5p1_v1,HLT_HIGEDPhoton10_v1,HLT_HIIslandPhoton10_v1\npaths.txt where each line in the file is an HLT path')
parser.add_argument('--colIndex',required=False,help='index of column on WBM\'s HLT Pre-scale Sets table')
parser.add_argument('--outcsv',required=False,help='optional csv output file')
args = parser.parse_args()

triggerMode = args.mode

pathnames = args.pathnames.split(",")
if len(pathnames) == 1 and pathnames[0].endswith(".txt") :
  print "Path names are given in a text file"
  text_file = open(pathnames[0], "r")
  lines = text_file.read().splitlines()
  pathnames = lines

colIndices = []
if args.colIndex == None :
  print "No column indices are given. All columns will be shown by default."
else :
  tmpList = args.colIndex.split(",")
  for tmp in tmpList :
    tmpInt = int(tmp)
    if tmpInt > 0 and tmpInt < 20 :
      colIndices.append(tmpInt)
    else :
      print "Given index is",tmpInt
      print "Column index must be greater than 0 and less than 11. Skipping column"

outputCSV = args.outcsv

print "triggerMode =",triggerMode
print "pathnames =",pathnames
print "colIndices =",colIndices
print "outputCSV =",outputCSV

hltTable = wbmutil.get_HLTPrescales(triggerMode,wbmparser)

if args.colIndex == None :
  colIndices = range(1, len(hltTable[0])+1)

columnTitles=[]
i=0
while i < len(hltTable[0]) :
  columnTitles.append(hltTable[0][i])
  i += 1

# print selected columns
strCols=columnTitles[colIndices[0]-1]
i=1
while i < len(colIndices) :
  strCols = strCols+", "+columnTitles[colIndices[i]-1]
  i += 1
print strCols

print "### HLT Pre-scale Sets Details ###"

import csv
if outputCSV != None :
  fout = open(outputCSV, mode='w')

  colTitlesCSV = []
  for colIndex in colIndices :
    colTitlesCSV.append(columnTitles[colIndex-1])
  writer = csv.DictWriter(fout, fieldnames=colTitlesCSV)

  writer.writeheader()

for pathname in pathnames :
  for hltrow in hltTable :
    if pathname in hltrow[1] :
      rowCSV = {}
      tmpIndex = colIndices[0]-1
      if tmpIndex == 1 :
        strLine = pathname
        rowCSV[columnTitles[tmpIndex]] = pathname
      else :
        strLine = hltrow[tmpIndex]
        rowCSV[columnTitles[tmpIndex]] = hltrow[tmpIndex]
      iCol = 1
      while iCol < len(colIndices) :
        tmpIndex = colIndices[iCol]-1
        if tmpIndex == 1 :
          strLine = strLine+", "+pathname
          rowCSV[columnTitles[tmpIndex]] = pathname
        else :
          strLine = strLine+", "+hltrow[tmpIndex]
          rowCSV[columnTitles[tmpIndex]] = hltrow[tmpIndex]
        iCol += 1
      print strLine
      if outputCSV != None :
        writer.writerow(rowCSV)

