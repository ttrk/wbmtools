#!/usr/bin/env python

def time2sec(str_hhmmss):
    h, m, s = str_hhmmss.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

import wbmtools.wbmutil as wbmutil
from wbmtools.wbmparser import WBMParser

wbmparser=WBMParser()

import argparse
parser = argparse.ArgumentParser(description='prints information about begin and end lumi section in a given run')
parser.add_argument('--run',required=True,help='326398')
parser.add_argument('--minLS',required=False,help='70')
parser.add_argument('--maxLS',required=False,help='440')
parser.add_argument('--outcsv',required=False,help='optional csv output file')
args = parser.parse_args()

#columnTitles = ["LS",
#                "Presc",
#                "Time",
#                "Inst",
#                "Deliv",
#                "Live",
#                "Deadtime",
#                "Beam 1",
#                "Beam 2"]

run = args.run
minLS=1
maxLS=999999
if args.minLS != None and args.maxLS != None :
  minLS=int(args.minLS)
  maxLS=int(args.maxLS)

outputCSV = args.outcsv

print "run =",run
print "minLS =",minLS
print "maxLS =",maxLS
print "outputCSV =",outputCSV

lumiTable = wbmutil.get_LumiSummary(run,wbmparser)
if len(lumiTable) == 0 : 
  print "No Table found on WBM. Exiting."
  quit()

columnTitles=["LS", "Presc", "Time", "Inst", "Deliv", "Live", "Deadtime", "Beam 1", "Beam 2"]

strCols=columnTitles[0]
i=1
while i < len(columnTitles) :
  strCols = strCols+", "+columnTitles[i]
  i += 1
print strCols

print "### Lumi Sections ###"

import csv
fout = 0
if outputCSV != None :
  fout = open(outputCSV, mode='w')
  writer = csv.writer(fout, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

  writer.writerow(["Run", run])

  colTitlesCSV = []
  for colTitle in columnTitles :
    colTitlesCSV.append(colTitle)
  writer.writerow(colTitlesCSV)

iMinLS = -1
iMaxLS = -1
iRow = 1
while iRow < len(lumiTable) :
  lumirow = lumiTable[iRow]
  lumi = int(lumirow[0])
  if not (lumi >= minLS and lumi <= maxLS) : 
    iRow += 1
    continue

  if iMinLS == -1 and lumi >= minLS :
    iMinLS = iRow
  if lumi == maxLS or lumi == len(lumiTable) - 1 :
    iMaxLS = iRow
  
  iRow += 1

lsArr = [int(lumiTable[iMinLS][0]), int(lumiTable[iMaxLS][0])]
presclArr = [int(lumiTable[iMinLS][1]), int(lumiTable[iMaxLS][1])]
timeArr = [lumiTable[iMinLS][2], lumiTable[iMaxLS][2]]
instLumiArr = [float(lumiTable[iMinLS][3]), float(lumiTable[iMaxLS][3])]
delivLumiArr = [float(lumiTable[iMinLS][4]), float(lumiTable[iMaxLS][4])]
liveLumiArr = [float(lumiTable[iMinLS][5]), float(lumiTable[iMaxLS][5])]
deadTimeArr = [float(lumiTable[iMinLS][6]), float(lumiTable[iMaxLS][6])]
beam1Arr = [float(lumiTable[iMinLS][7]), float(lumiTable[iMaxLS][7])]
beam2Arr = [float(lumiTable[iMinLS][8]), float(lumiTable[iMaxLS][8])]

i = 0
while i < 2 :
  strLine = "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (lsArr[i], presclArr[i], timeArr[i], instLumiArr[i], delivLumiArr[i], liveLumiArr[i], deadTimeArr[i], beam1Arr[i], beam2Arr[i])
  print strLine
  if outputCSV != None :
#    rowCSV = {}
#    rowCSV[columnTitles[0]] = lsArr[i]
#    rowCSV[columnTitles[1]] = presclArr[i]
#    rowCSV[columnTitles[2]] = timeArr[i]
#    rowCSV[columnTitles[3]] = instLumiArr[i]
#    rowCSV[columnTitles[4]] = delivLumiArr[i]
#    rowCSV[columnTitles[5]] = liveLumiArr[i]
#    rowCSV[columnTitles[6]] = deadTimeArr[i]
#    rowCSV[columnTitles[7]] = beam1Arr[i]
#    rowCSV[columnTitles[8]] = beam2Arr[i]
    rowCSV = lsArr[i], presclArr[i], timeArr[i], instLumiArr[i], delivLumiArr[i], liveLumiArr[i], deadTimeArr[i], beam1Arr[i], beam2Arr[i]
    writer.writerow(rowCSV)

  i += 1

tmpLS = iMinLS-1
if iMinLS == 1 :
  tmpLS = 1
timeBegin = time2sec(lumiTable[tmpLS][2])
totTime = time2sec(timeArr[1]) - timeBegin
if totTime < 0 : # rolled over to next day
  totTime = (time2sec("23:59:59") - timeBegin) + (time2sec(timeArr[1]))
totTime = int(totTime)
totDelivLumi = delivLumiArr[1] - float(lumiTable[tmpLS][4])
totLiveLumi = liveLumiArr[1] - float(lumiTable[tmpLS][5])
# PbPb inelastic cross section = 7.66 barn, from https://arxiv.org/abs/1710.07098
# Estimates are done using delivered lumi
xs = 7.66
totColl_Deliv = totDelivLumi * 1000 * xs
aveCollRate_Deliv = totColl_Deliv / totTime
totColl_Record = totLiveLumi * 1000 * xs
aveCollRate_Record = totColl_Record / totTime

print "Total Time [sec] =",totTime
print "Total Delivered Lumi [inv mb] =",totDelivLumi
print "Total Live Lumi [inv mb] =",totLiveLumi
print "Total Collisions (based on delivered lumi) =",totColl_Deliv
print "Ave Collision Rate [Hz] (based on delivered lumi) =",aveCollRate_Deliv
print "Total Collisions (based on live lumi) =",totColl_Record
print "Ave Collision Rate [Hz] (based on live lumi) =",aveCollRate_Record

if outputCSV != None :
  writer.writerow(["Total Time [sec]",
                   "Total Delivered Lumi [inv mb]",
                   "Total Live Lumi [inv mb]",
                   "Total Collisions (from deliv lumi)",
                   "Ave Collision Rate [Hz] (from deliv lumi)",
                   "Total Collisions (from live lumi)",
                   "Ave Collision Rate [Hz] (from live lumi)",
                   ])
  writer.writerow([totTime,
                   totDelivLumi,
                   totLiveLumi,
                   totColl_Deliv,
                   aveCollRate_Deliv,
                   totColl_Record,
                   aveCollRate_Record
                   ])

