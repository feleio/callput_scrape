import codecs
import datetime
import time
import db
import re
import sys
import urllib2
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
    amountPattern = re.compile('^(\d+\.\d+)$')
    match = amountPattern.match(s)
    if match:
        return s
    else:  
        amountCurrencyPattern = re.compile('^(\d+\.\d+|\d+)\s*\(([a-zA-Z]+)\)$')
        match = amountCurrencyPattern.match(s)
        if match:
            amount = match.group(1)
            currency = match.group(2)
            return amount

    raise Exception('invalid price')

def getCurrency(s):
    amountPattern = re.compile('^(\d+\.\d+)$')
    match = amountPattern.match(s)
    if match:
        return 'HKD'
    else:  
        amountCurrencyPattern = re.compile('^(\d+\.\d+|\d+)\s*\(([a-zA-Z]+)\)$')
        match = amountCurrencyPattern.match(s)
        if match:
            amount = match.group(1)
            currency = match.group(2)
            return currency

    raise Exception('invalid price')

def checkNANumber(s):
    if s == 'N/A':
        return 0
    else:
        return s

def checkNAString(s):
    if s == 'N/A':
        return ''
    else:
        return s


#request = urllib2.Request('http://hk.warrants.com/home/ch/sgdata/list_f_real_c.cgi?order=dbcode%20desc&ucode=&sname=ALL&wtype=ALL&mtype=0&iv1=&iv2=&ptype=0&s1=&s2=&osp1=&osp2=&egear=0&cr1=&cr2=&d1=&d2=&m1=0&m2=0&industry=&cnycode_dummy=')

# request = urllib2.Request('http://hk.warrants.com/home/en/sgdata/list_f_real_e.cgi?order=dbcode%20desc&ucode=&sname=ALL&wtype=ALL&mtype=0&iv1=&iv2=&ptype=0&s1=&s2=&osp1=&osp2=&egear=0&cr1=&cr2=&d1=&d2=&m1=0&m2=0&industry=&cnycode_dummy=')
# request.add_header('Referer', 'http://hk.warrants.com/home/ch/sgdata/list_c.cgi')

# print("downloading page")
# response = urllib2.urlopen(request)
# html = response.read().decode("Big5")

file = codecs.open("web_output_old_one.html", encoding="utf-8")
html = file.read()

print("processing downloaded page")
soup = BeautifulSoup(html,"html.parser")

db.remove_all_warrants_and_lasts()

numOfRecord = 0;
for tr in soup.tr("tr"):
    warrant = Warrant()
    if numOfRecord == 0:
        tdItr = iter(tr("td"))
        tdItr.next()

        currentTd = tdItr.next()
        warrant.issuer = currentTd.string.strip()

        currentTd = tdItr.next()
        warrant.code = currentTd.string.strip()

        currentTd = tdItr.next()
        warrant.name = currentTd.string.strip()

        currentTd = tdItr.next()
        warrant.callOrPut = currentTd.string.strip()

        currentTd = tdItr.next()
        warrant.warrantType = checkNAString(currentTd.string.strip())

        currentTd = tdItr.next()
        warrant.maturity = datetime.datetime.strptime(currentTd.string.strip(),"%Y-%m-%d")

        currentTd = tdItr.next()
        warrant.strike = float(getAmount(currentTd.string.strip()))

        currentTd = tdItr.next()
        warrant.last = float(getAmount(currentTd.string.strip()))

        warrant.currency = getCurrency(currentTd.string.strip())

        currentTd = tdItr.next()
        warrant.changePercentage = float(checkNANumber(currentTd.string.strip()))

        currentTd = tdItr.next()
        warrant.premiumPercentage = float(checkNANumber(currentTd.string.strip()))

        currentTd = tdItr.next()
        print currentTd.string.strip()
        warrant.effGearing = float(checkNANumber(currentTd.string.strip()))

        currentTd = tdItr.next()
        warrant.ivPercentage = float(checkNANumber(currentTd.string.strip()))

        currentTd = tdItr.next()
        warrant.deltaPercentage = float(checkNANumber(currentTd.string.strip()))

        currentTd = tdItr.next()
        warrant.outstandingM = float(checkNANumber(currentTd.string.strip()))

        currentTd = tdItr.next()
        warrant.outstandingPercentage = float(checkNANumber(currentTd.string.strip()))

        currentTd = tdItr.next()
        warrant.turnover000 = float(getAmount(currentTd.string.strip()))

        currentTd = tdItr.next()
        warrant.ent = float(checkNANumber(currentTd.string.strip()))

        currentTd = tdItr.next()
        TodayStr = datetime.datetime.now().strftime("%Y-%m-%d")
        lastUpdateTimeStr = TodayStr + " " + currentTd.string.strip()
        warrant.lastUpdateTime = time.strptime(lastUpdateTimeStr, "%Y-%m-%d %H:%M")

        db.add_warrant(warrant.name, warrant.code, warrant.issuer, warrant.underlying, warrant.call_or_put, warrant.warrant_type, warrant.maturity, warrant.strike, warrant.ent)
        
        print warrant.maturity
        print warrant.lastUpdateTime

    numOfRecord += 1

print "numOfRecord: %s" % numOfRecord

# file = codecs.open("web_output.html", "w", "utf-8")
# file.write(html)
# file.close()
print("end")
