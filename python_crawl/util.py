from urllib.parse import urlparse
import os


def getDomainName(url):
    try:
        results = getSubDomainName(url).split('.')
        return results[-2] + '.' + results[-1]
    except:
        return ''


def getSubDomainName(url):
    try:
        return urlparse(url).netloc
    except:
        return ''

def initAllowElem():
    ret = set()
    with open('.\_allowElem.txt', 'r') as elems:
        arrayOfElem = elems.read().splitlines()
    for elem in arrayOfElem:
        ret.add(elem)
    return ret

def initFolder(path):
    createFolder(path + "/static")
    createFolder(path + "/text")
    createFolder(path + "/html")

    with open("./static/timeCalculate.csv", 'a') as fp:
        fp.write("title, startTime, endTime, total\n")

def createFolder(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            return True
    except OSError:
        print ('Error: Creating directory. ' +  path)
        return False

def getStringAfterLastSlash(path):
    i = len(path) - 1
    x = 1
    if path[i] == '/':
        i = i - 1
        x = x + 1
    while i > 0 and path[i] != '/':
        i = i - 1
    return path[i + 1:len(path) - 1]

def getDeep(path):
    i = len(path) - 1
    deep = 0
    end = 0
    if path[0:8] == "https://":
        end = 7
    if path[end:4] == "www.":
        end = end + 4
    if path[i] == '/':
        i = i - 1
    while i > end:
        if path[i] == '/':
            deep = deep + 1
        i = i - 1
    return deep