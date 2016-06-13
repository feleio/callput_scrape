import codecs
import xlrd
import datetime
import time
import re
import sys
import urllib2
import db
from bs4 import BeautifulSoup

sys.stdout = codecs.getwriter('utf8')(sys.stdout)

class Warrant:
    issuer = ""
    code = ""
    name = ""
    underlying = ""
    callOrPut = ""
    warrantType = ""
    maturity = datetime.datetime.now()
    currency = ""
    strike = 0.0
    last = 0.0
    bid = 0.0
    ask = 0.0
    underlyingPrice = 0.0
    changePercentage = 0.0
    premiumPercentage = 0.0
    effGearing = 0.0
    ivPercentage = 0.0
    deltaPercentage = 0.0
    outstandingM = 0.0
    outstandingPercentage = 0.0
    turnover000 = 0.0
    ent = 0.0
    lastUpdateTime = datetime.datetime.now()


def getAmount(s):
    if isinstance(s, float):
        return s
    else:
        amountCurrencyPattern = re.compile('^([a-zA-Z]+)\s*(\d+\.\d+|\d+)$')
        match = amountCurrencyPattern.match(s.strip())
        if match:
            currency = match.group(1)
            amount = match.group(2)
            return amount

    raise Exception('invalid price')

def getCurrency(s):
    if isinstance(s, float):
        return 'HKD'
    else:  
        amountCurrencyPattern = re.compile('^([a-zA-Z]+)\s*(\d+\.\d+|\d+)$')
        match = amountCurrencyPattern.match(s.strip())
        if match:
            currency = match.group(1)
            return currency

    raise Exception('invalid price')

def checkNA(s):
    if isinstance(s, float):
        return s
    else:
        if s == 'N/A':
            return 0

# request = urllib2.Request('http://hk.warrants.com/home/en/sgdata/list_e.xls?ucode=&sname=ALL&wtype=ALL&mtype=0&iv1=&iv2=&ptype=0&s1=&s2=&osp1=&osp2=&egear=0&cr1=&cr2=&d1=&d2=&m1=0&m2=0&industry=&order=dbcode%20desc&cnycode_dummy=')
# request.add_header('Referer', 'http://hk.warrants.com/home/ch/sgdata/list_c.cgi')

# print("downloading page")
# response = urllib2.urlopen(request) 

# excel = open("records.xls", "wb")
# excel.write(response.read())

book = xlrd.open_workbook('records.xls')
sheet = book.sheet_by_index(0)
numrow = 0

db.remove_all_warrants_and_lasts()

for rowNum in range(sheet.nrows):
    if rowNum != 0:
        rows = sheet.row_values(rowNum)

        warrant = Warrant()

        warrant.issuer = rows[0].strip()
        warrant.code = rows[1]
        warrant.name = rows[2].strip()
        warrant.underlying = str(rows[3]).strip()
        warrant.callOrPut = rows[4].strip()
        warrant.warrantType = rows[5].strip()
        warrant.maturity = datetime.datetime.strptime(rows[6].strip(), "%Y-%m-%d")
        warrant.strike = getAmount(rows[7])
        warrant.underlyingPrice = getAmount(rows[8])
        warrant.bid = getAmount(rows[9])
        warrant.ask = getAmount(rows[10])
        warrant.last = getAmount(rows[11])
        warrant.currency = getCurrency(rows[11])

        warrant.changePercentage = checkNA(rows[12])
        warrant.premiumPercentage = checkNA(rows[13])
        warrant.effGearing = checkNA(rows[14])
        warrant.ivPercentage = checkNA(rows[15])
        warrant.deltaPercentage = checkNA(rows[16])
        warrant.outstandingM = checkNA(rows[17])
        warrant.outstandingPercentage = checkNA(rows[18])
        warrant.turnover000 = getAmount(rows[19])

        db.add_warrant(warrant.name, warrant.code, warrant.issuer, warrant.underlying, warrant.callOrPut, warrant.warrantType, warrant.maturity, warrant.strike, warrant.ent)

        numrow+=1

print "%s row saved" % numrow 
print("end")
