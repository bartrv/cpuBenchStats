# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 11:15:29 2023

@author: bvoigt
"""

# scatterChart - CPU Benchmark - https://www.cpubenchmark.net/high_end_cpus.html
# H:\eLearning\python3\cpuBenchmark.net\HighEndCPU_20230208.txt
import re
from copy import copy as cp
from matplotlib import pyplot as plt

dataFileString = "H:/eLearning/python3/cpuBenchmark.net/HighEndCPU_20230208.txt"

with open(dataFileString) as file:
    data = file.read()

data = [n for n in data.split("\n") if 'p(event,' in n]
#<li id="pk5088"><span class="more_details" onclick="p(event, '124,119', 1, 1, 96, 2, '$11,805.00*', null, null);"></span><a href="cpu.php?cpu=AMD+EPYC+9654&amp;id=5088"><span class="prdname">AMD EPYC 9654</span><div><span class="index pink" style="width: 34.5%">(34.5%)</span></div><span class="count">10.5</span><span class="mark-neww">124,119</span><span class="price-neww">$11,805.00*</span></a></li>
cpuData = []


for i,n in enumerate(data):
    #print('line',i)
    cpuName = re.search("(?<=(<span class=\"prdname\">)).*?(?=(<\/span>))",n)[0]
    cpuManuf = "Unknown"
    cpuSeries = "Unknown"
    cpuSKU = "Unknown"
    
    if cpuName[0:3] == "AMD":
            cpuManuf = "AMD"
            cpuSeries = ""
            cpuSKU = ""
    elif cpuName[0:5] == "Intel":
            cpuManuf = "Intel"
            cpuSeries = ""
            cpuSKU = ""
    elif cpuName[0:3] == "ARM":
            cpuManuf = "ARM"
            cpuSeries = ""
            cpuSKU = ""
    elif cpuName[0:5] == "Apple":
            cpuManuf = "Apple"
            cpuSeries = ""
            cpuSKU = ""
            
    cpuID = re.search("(?<=(<li id=\")).*?(?=(\">))",n)[0]
    #print('ID=',cpuID)
    cpuScore = re.search("(?<=(<span class=\"mark-neww\">)).*?(?=(<\/span>))",n)[0]
    #print('cpuScore=',cpuScore)
    cpuRank = re.search("(?<=(p\(event, '"+cpuScore+"', )).*?(?=,)",n)[0]
    cpuSamples = re.search("(?<=(p\(event, \'"+cpuScore+"\', "+cpuRank+", )).*?(?=,)",n)[0]
    cpuCores = re.search("(?<=(p\(event, \'"+cpuScore+"\', "+cpuRank+", "+cpuSamples+", )).*?(?=,)",n)[0]
    cpuTMult = re.search("(?<=(p\(event, \'"+cpuScore+"\', "+cpuRank+", "+cpuSamples+", "+cpuCores+", )).*?(?=,)",n)[0]
    cpuMpMax = 1
    cpuPrice = re.search("(?<=(<span class=\"price-neww\">)).{0,14}(?=(<\/span>))",n)[0]
    
    cpuScore = int("".join([x for x in cpuScore if x.isdigit()]))
    cpuPrice = -10 if cpuPrice=='NA' else float("".join([x for x in cpuPrice if (x.isdigit() or x==".")]))
    
    cpuCores = int(cpuCores)
    cpuTMult = int(cpuTMult)
    
    cpuData.append({"name":cpuName,"manuf":cpuManuf,"series":cpuSeries,"sku":cpuSKU,"id":cpuID,"rank":cpuRank,"score":cpuScore,"cores":cpuCores,"threads":(cpuCores*cpuTMult),"mpMax":cpuMpMax,"price":cpuPrice})
    
IntelPerfListX = [x["score"] for x in cpuData if x["manuf"]=="Intel"]
AMD__PerfListX = [x["score"] for x in cpuData if x["manuf"]=="AMD"]
ARM__PerfListX = [x["score"] for x in cpuData if x["manuf"]=="ARM"]
ApplePerfListX = [x["score"] for x in cpuData if x["manuf"]=="Apple"]
IntelPerfListY = [x["price"] for x in cpuData if x["manuf"]=="Intel"]
AMD__PerfListY = [x["price"] for x in cpuData if x["manuf"]=="AMD"]
ARM__PerfListY = [x["price"] for x in cpuData if x["manuf"]=="ARM"]
ApplePerfListY = [x["price"] for x in cpuData if x["manuf"]=="Apple"]
EPYCListX = [x["score"] for x in cpuData if x["name"][4:8]=="EPYC"]
EPYCListY = [x["price"] for x in cpuData if x["name"][4:8]=="EPYC"]
XeonListX = [x["score"] for x in cpuData if x["name"][6:10]=="Xeon"]
XeonListY = [x["price"] for x in cpuData if x["name"][6:10]=="Xeon"]
CoreListX = [x["score"] for x in cpuData if x["name"][6:10]=="Core"]
CoreListY = [x["price"] for x in cpuData if x["name"][6:10]=="Core"]
RyzenListX = [x["score"] for x in cpuData if x["name"][4:9]=="Ryzen"]
RyzenListY = [x["price"] for x in cpuData if x["name"][4:9]=="Ryzen"]
"""
x = range(100)
y = range(100,200)
"""
# https://matplotlib.org/stable/gallery/mplot3d/wire3d.html

fig = plt.figure()
ax1 = fig.add_subplot(111)

#ax1.scatter(IntelPerfListX, IntelPerfListY, s=7, c='b', marker="o", label='Intel')
#ax1.scatter(AMD__PerfListX, AMD__PerfListY, s=7, c='r', marker="s", label='AMD')
#ax1.scatter(ARM__PerfListX, ARM__PerfListY, s=7, c='g', marker="^", label='ARM')
#ax1.scatter(ApplePerfListX, ApplePerfListY, s=7, c='y', marker="D", label='Apple')
ax1.scatter(EPYCListX, EPYCListY, s=7, c='b', marker="o", label='EPYC')
ax1.scatter(XeonListX, XeonListY, s=7, c='r', marker="s", label='XEON')
ax1.scatter(RyzenListX, RyzenListY, s=7, c='g', marker="^", label='Ryzen')
ax1.scatter(CoreListX, CoreListY, s=7, c='y', marker="d", label='Core')
plt.legend(loc='upper left')
plt.show()

