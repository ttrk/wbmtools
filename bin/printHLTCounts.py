#!/usr/bin/env python

import wbmtools.wbmutil as wbmutil
from wbmtools.wbmparser import WBMParser

wbmparser=WBMParser()

import argparse
parser = argparse.ArgumentParser(description='prints HLT counts in a given run range')
parser.add_argument('--lumiranges',required=True,help='Option1 : A comma separated list of lumi ranges such as 326238,326499:32:44,326500:1:35 where each element is <run>:<minLS>:<maxLS> or <run>. Option 2 : A txt file where each line is one lumi range. Option 3 : A json file')
parser.add_argument('--pathnames',required=True,help='Option1 : HLT_HIPuAK4CaloJet40Eta5p1_v1,HLT_HIGEDPhoton10_v1,HLT_HIIslandPhoton10_v1. Option2 : A txt file where each line in file is an HLT path')
parser.add_argument('--colIndex',required=False,help='index of columns from ["Name", "L1Pass", "PSPass", "PAccept"]')
parser.add_argument('--outcsv',required=False,help='optional csv output file')
args = parser.parse_args()

#columnTitles = ["Name",
#                "L1Pass",
#                "PSPass",
#                "PAccept"]

lumiRangesStr = args.lumiranges.split(",")
if len(lumiRangesStr) == 1 and lumiRangesStr[0].endswith(".txt") :
  print "Lumi ranges are given in a text file"
  text_file = open(lumiRangesStr[0], "r")
  lines = text_file.read().splitlines()
  lumiRangesStr = lines
elif len(lumiRangesStr) == 1 and lumiRangesStr[0].endswith(".json") :
  import json
  print "Lumi ranges are given in a json file"
  json_file = open(lumiRangesStr[0], "r")
  json_data = json.load(json_file)
  lumiRangesStr = []
  for key in json_data.keys() :
    for value in json_data[key] :
      strTmp = "%s:%s:%s" % (key, value[0], value[1])
      lumiRangesStr.append(strTmp)

lumiRanges = []
for tmp in lumiRangesStr :
  run_lumis = tmp.split(":")
  run = int(run_lumis[0])
  minLS = 0
  maxLS = -1
  if len(run_lumis) == 3 :
    minLS=int(run_lumis[1])
    maxLS=int(run_lumis[2])
  lumiRanges.append([run, minLS, maxLS])

pathnames = args.pathnames.split(",")
if len(pathnames) == 1 and pathnames[0].endswith(".txt") :
  print "Path names are given in a text file"
  text_file = open(pathnames[0], "r")
  lines = text_file.read().splitlines()
  pathnames = lines

columnTitlesAll=["Name", "L1Pass", "PSPass", "PAccept"]  # all columns that can be shown in the output
colIndices = []
columnTitles = []
columnTitlesCount=[]  # columns that contain counts 
if args.colIndex == None :
  print "No column indices are given. All columns will be shown by default."
  columnTitles = columnTitlesAll
  colIndices = range(1, len(columnTitlesAll)+1)
  columnTitlesCount = columnTitlesAll[1:len(columnTitlesAll)]
else :
  tmpList = args.colIndex.split(",")
  for tmp in tmpList :
    i = int(tmp)
    if i > 0 and i < 5 :
      columnTitles.append(columnTitlesAll[i-1])
      colIndices.append(i)
      if i > 1 :
        columnTitlesCount.append(columnTitlesAll[i-1])
    else :
      print "Given index is",i
      print "Column index must be greater than 0 and less than 5. Skipping column"

nColsCount = len(columnTitlesCount)

## create list to store counts for each path
counts = []
for pathname in pathnames :
  counts.append([0]*nColsCount)

outputCSV = args.outcsv

print "lumiRanges ="
for lumiRange in lumiRanges :
  tmp = "%s" % (lumiRange[0])
  if lumiRange[1] <= lumiRange[2] :
    tmp = "%s, %s, %s" % (lumiRange[0], lumiRange[1], lumiRange[2])
  print tmp

print "pathnames =",pathnames
print "colIndices =",colIndices
print "outputCSV =",outputCSV

## connect to WBM and get counts
for lumiRange in lumiRanges :
  strTmp = "processing Run %s, [%s, %s]" % (lumiRange[0], lumiRange[1], lumiRange[2])
  print strTmp
  hltTable = wbmutil.get_HLTSummary(lumiRange[0], lumiRange[1], lumiRange[2], wbmparser)
  wbmColTitles = hltTable[0]
  i = 0
  nPaths = len(pathnames)
  while i < nPaths :  
    for hltrow in hltTable :
      if pathnames[i] in hltrow[1] :
        j = 0
        while j < nColsCount :
          colTmp = columnTitlesCount[j]
          if colTmp in wbmColTitles :
            indexTmp = wbmColTitles.index(colTmp)
            countTmp = int(hltrow[indexTmp])
            counts[i][j] += countTmp
          j += 1
    i += 1    
## done with WBM

print "### HLT Trigger Counts ###"
# print selected columns
strCols=columnTitles[0]
i=1
while i < len(columnTitles) :
  strCols = strCols+", "+columnTitles[i]
  i += 1
print strCols

import csv
fout = 0
if outputCSV != None :
  fout = open(outputCSV, mode='w')

  colTitlesCSV = []
  for colTitle in columnTitles :
    colTitlesCSV.append(colTitle)
  writer = csv.DictWriter(fout, fieldnames=colTitlesCSV)

  writer.writeheader()

i = 0
nPaths = len(pathnames)
while i < nPaths :
  pathname = pathnames[i]
  strLine = ""
  rowCSV = {}
  if columnTitles[0] == "Name" :
    strLine = pathname
    rowCSV["Name"] = pathname
  else :
    indexCount = columnTitlesCount.index(columnTitles[0])
    strLine = "%s" % (counts[i][indexCount])
    rowCSV[columnTitles[0]] = counts[i][indexCount]
  iCol = 1
  while iCol < len(colIndices) :
    if columnTitles[iCol] == "Name" :
      strLine = strLine+", "+pathname
      rowCSV["Name"] = pathname
    else :
      indexCount = columnTitlesCount.index(columnTitles[iCol])
      strLine = "%s, %s" % (strLine, counts[i][indexCount])
      rowCSV[columnTitles[iCol]] = counts[i][indexCount]
    iCol += 1
  print strLine
  if outputCSV != None :
    writer.writerow(rowCSV)
  i += 1

