import json
import os
import re
import sys

# get indexes information
def getInfo():
    os.system("curl -X GET 'https://localhost:9200/*/_settings?pretty' --user elastic:Tolt5Driv -k > resault")



# load json information from file
f = open('./resault.json')
jf = json.load(f)
list_of_indexes = []




# get date of indexes to remove
def removeDate():
    list_of_dates = []
    for i in jf:
        exclude = re.compile(r'.*(mikrotik|winlogbeat|auditbeat).*')
        if not exclude.search(i):
            list_of_indexes.append(i)
            getdate = re.compile(r'^(fortigate-|cisco-ftd-outgoing-|filebeat-cisco-ftd-|filebeat-7.1.1-)(\d+\.\d+\.\d+)$')
            dateofindex = getdate.search(i)
            if dateofindex:
                list_of_dates.append(dateofindex.group(2).replace(".", ""))
        else:
            pass
    list_of_dates.sort()
    a,b,c,d,e,f,g,h = list_of_dates[0]
    datetoremove = a+b+c+d+"."+e+f+"."+g+h
    return datetoremove



# removing indexes of the date that pass by removeDate()
def removeIndexes(datetoremove):
    for i in ["fortigate-", "cisco-ftd-outgoing-", "filebeat-cisco-ftd-", "filebeat-7.1.1-"]:
        indextoremove = i+datetoremove
        if indextoremove in list_of_indexes:
            stdinput = input(f'index {indextoremove} is going to remove, press (y) for removing it: ')
            if stdinput == "y":
                os.system("curl -X DELETE 'http://localhost:9200/{indextoremove}' --user elastic:Tolt5Driv -k")
            else:
                print("### aborted ... ###")



# find indexes have been readonly
def findReadonlyIndex():
    for i in jf:
        aa = jf[i]["settings"]["index"]
        if "blocks" in aa:
            if "read_only" in aa["blocks"].keys():
                readonlyvalue = aa["blocks"]["read_only"]
                if readonlyvalue == "true":
                    datetoremove = removeDate()
                    removeIndexes(datetoremove)
                    # print(f'### indexes of date {datetoremove} removed ###')
                    break
                else:
                    print("### good to GO... ###")


def RUN():
    # getInfo()
    findReadonlyIndex()

RUN()