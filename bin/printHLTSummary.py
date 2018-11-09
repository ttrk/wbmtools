#!/usr/bin/env python

import wbmtools.wbmutil as wbmutil
from wbmtools.wbmparser import WBMParser

wbmparser=WBMParser()

import argparse
parser = argparse.ArgumentParser(description='prints HLT Summary in a given run')
parser.add_argument('--run',required=True,help='326238 or 326238:107:503 where 230 and 1050 are min and max lumi sections')
parser.add_argument('--pathnames',required=True,help='HLT_HIPuAK4CaloJet40Eta5p1_v1,HLT_HIGEDPhoton10_v1,HLT_HIIslandPhoton10_v1\npaths.txt where each line in the file is an HLT path')
parser.add_argument('--colIndex',required=False,help='index of column on WBM\'s HLTSummary table')
parser.add_argument('--outcsv',required=False,help='optional csv output file')
args = parser.parse_args()

#columnTitles = ["n",
#                "Name",
#                "nLS",
#                "L1Pass",
#                "PSPass",
#                "PAccept",
#                "RateHz",
#                "PExcept",
#                "PReject",
#                "L1 Prerequisite"]

run_lumis = args.run.split(":")
run = run_lumis[0]
minLS=0
maxLS=-1
if len(run_lumis) == 3 :
  minLS=run_lumis[1]
  maxLS=run_lumis[2]

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
    if tmpInt > 0 and tmpInt < 11 :
      colIndices.append(tmpInt)
    else :
      print "Given index is",tmpInt
      print "Column index must be greater than 0 and less than 11. Skipping column"

outputCSV = args.outcsv

print "run =",run
print "minLS =",minLS
print "maxLS =",maxLS
print "pathnames =",pathnames
print "colIndices =",colIndices
print "outputCSV =",outputCSV

hltTable = wbmutil.get_HLTSummary(run,minLS,maxLS,wbmparser)

if args.colIndex == None :
  colIndices = range(1, len(hltTable[0]))

columnTitles=[]
i=0
while i < len(hltTable[0]) - 1 : # skip the very last column
  columnTitles.append(hltTable[0][i])
  i += 1

# print selected columns
strCols=columnTitles[colIndices[0]-1]
i=1
while i < len(colIndices) :
  strCols = strCols+", "+columnTitles[colIndices[i]-1]
  i += 1
print strCols

print "### HLTSummary Trigger Paths ###"

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

