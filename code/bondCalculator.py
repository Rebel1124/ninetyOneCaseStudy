# Import Libraries
import numpy as np
import pandas as pd
pd.set_option('mode.chained_assignment', None)


def nperiods(ncd, maturity):
    n = round((((maturity - ncd).days)/(365.25/2)),0)
    return n


def cumex(s, bcd):
    if(s < bcd):
        return 1
    else:
        return 0

 
def daysacc(s, lcd, ncd, cum):

    if (cum == 1):
        days = (s - lcd).days
    else:
        days = (s-ncd).days
    return days


def couponPay(cb, cum):
    cpn=(cb/2)
    cpnNCD = (cpn)*cum
    return cpnNCD


def factor(yieldm):
    f = (1+(yieldm/2))**-1
    return f


def brokenPeriod(s, lcd, ncd, maturity):
    if(ncd == maturity):
        bp = (ncd-s)/(365/2)
    else:
        bp = (ncd-s)/(ncd-lcd)
    
    return bp


def brokenPeriodDF(f, bp, ncd, maturity):
    if(ncd==maturity):
        bpf = f/(f+(bp*(1-f)))
    else:
        bpf = f**bp

    return bpf


def accint(daysacc, cb):
    accint = (daysacc*cb)/365
    return accint


def accintRound(daysacc, cb):
    accint = round((daysacc*cb)/365,7)
    return accint


def aip(n, bpf,cpnncd, cb, f, r):

    cpn=(cb/2)

    if(f==1):
        price=cpnncd+(cpn*n) + r
    else:
        price = bpf*(cpnncd+(cpn*((f*(1-(f**n)))/(1-f))+(r*(f**n))))

    return price


def clean(aip, accint):
    cleanPrice = (aip - accint)
    return cleanPrice


def cleanRound(aip, accint):
    cleanPrice = round((aip - accint),7)
    return cleanPrice


def aipRound(cpRound, accintRound):
    price = (cpRound + accintRound)
    return price


def dbpf(f, bp, bpf, ncd, maturity):
    if(ncd==maturity):
        dbpf = (bp*(bpf**2))/(f**2)
    else:
        dbpf = (bp*bpf)/f

    return dbpf


def d2bpf(f, bp, bpf, dbpf, ncd, maturity):
    if(ncd==maturity):
        d2bpf = (2*dbpf)*((bp*bpf - f)/(f**2))
    else:
        d2bpf = dbpf*((bp-1)/f)

    return d2bpf


def dcpn(n, cb, f):
    cpn = cb/2

    if(f==1):
        dcpn=cpn*((n*(n+1))/2)
    else:
        dcpn=cpn*((1-(n-(n*f)+1)*(f**n))/((1-f)**2))
    
    return dcpn


def d2cpn(n, cb, f):
    cpn=cb/2

    if(f==1):
        d2cpn = cpn*((n*((n**2)-1))/3)
    else:
        d2cpn = cpn*((2-((n*(1-f)*(2+(n-1)*(1-f))+(2*f))*(f**(n-1))))/((1-f)**3))

    return d2cpn


def dr(n,f):
    dr=n*1*(f**(n-1))
    return dr

def d2r(n,f):
    d2r=n*(n-1)*1*(f**(n-2))
    return d2r


def daip(dbpf, aip, bpf, dcpn, dr):

    daip = dbpf*(aip/bpf) + bpf*(dcpn+dr)

    return daip


def d2aip(d2bpf, aip, bpf, dbpf, daip, dcpn, d2cpn, dr, d2r):

    d2aip = d2bpf*(aip/bpf) + dbpf*(((bpf*daip - aip*dbpf)/(bpf**2))+dcpn+dr)+bpf*(d2cpn+d2r)

    return d2aip


def delta(f, daip, dy):

    delta = 1*((f**2)/200)*(daip/(dy))

    return delta


def randperbp(delta):

    rpbp = 100*delta

    return rpbp

def modfinal(s, lcd, ncd, bcd, maturity, cb, yieldm, dy=1):

    aip = allInPrice(s, lcd, ncd, bcd, maturity, cb, yieldm)

    cpn = cb/2

    f = (1+(yieldm/2))**-1

    n = round((((maturity - ncd).days)/(365.25/2)),0)

    if(ncd == maturity):
        bp = (ncd-s)/(365/2)
    else:
        bp = (ncd-s)/(ncd-lcd)

    if(ncd==maturity):
        bpf = f/(f+(bp*(1-f)))
    else:
        bpf = f**bp

    if(ncd==maturity):
        dbpf = (bp*(bpf**2))/(f**2)
    else:
        dbpf = (bp*bpf)/f

    if(f==1):
        dcpn=cpn*((n*(n+1))/2)
    else:
        dcpn=cpn*((1-(n-(n*f)+1)*(f**n))/((1-f)**2))

    dr=n*1*(f**(n-1))

    daip = dbpf*(aip/bpf) + bpf*(dcpn+dr)

    delta = 1*((f**2)/200)*(daip/(dy))

    dmod = 100*(delta/aip)

    return dmod


def durationfinal(s, lcd, ncd, bcd, maturity, cb, yieldm, dy=1):

    aip = allInPrice(s, lcd, ncd, bcd, maturity, cb, yieldm)

    cpn = cb/2

    f = (1+(yieldm/2))**-1

    n = round((((maturity - ncd).days)/(365.25/2)),0)

    if(ncd == maturity):
        bp = (ncd-s)/(365/2)
    else:
        bp = (ncd-s)/(ncd-lcd)

    if(ncd==maturity):
        bpf = f/(f+(bp*(1-f)))
    else:
        bpf = f**bp

    if(ncd==maturity):
        dbpf = (bp*(bpf**2))/(f**2)
    else:
        dbpf = (bp*bpf)/f

    if(f==1):
        dcpn=cpn*((n*(n+1))/2)
    else:
        dcpn=cpn*((1-(n-(n*f)+1)*(f**n))/((1-f)**2))

    dr=n*1*(f**(n-1))

    daip = dbpf*(aip/bpf) + bpf*(dcpn+dr)

    delta = 1*((f**2)/200)*(daip/(dy))

    dmod = 100*(delta/aip)

    dur = dmod/f

    return dur

def deltafinal(s, lcd, ncd, bcd, maturity, cb, yieldm, dy=1):

    aip = allInPrice(s, lcd, ncd, bcd, maturity, cb, yieldm)

    cpn = cb/2

    f = (1+(yieldm/2))**-1

    n = round((((maturity - ncd).days)/(365.25/2)),0)

    if(ncd == maturity):
        bp = (ncd-s)/(365/2)
    else:
        bp = (ncd-s)/(ncd-lcd)

    if(ncd==maturity):
        bpf = f/(f+(bp*(1-f)))
    else:
        bpf = f**bp

    if(ncd==maturity):
        dbpf = (bp*(bpf**2))/(f**2)
    else:
        dbpf = (bp*bpf)/f

    if(f==1):
        dcpn=cpn*((n*(n+1))/2)
    else:
        dcpn=cpn*((1-(n-(n*f)+1)*(f**n))/((1-f)**2))

    dr=n*1*(f**(n-1))

    daip = dbpf*(aip/bpf) + bpf*(dcpn+dr)

    delta = 1*((f**2)/200)*(daip/(dy))*(-100)

    return delta

def rpbpfinal(s, lcd, ncd, bcd, maturity, cb, yieldm, dy=1):

    aip = allInPrice(s, lcd, ncd, bcd, maturity, cb, yieldm)

    cpn = cb/2

    f = (1+(yieldm/2))**-1

    n = round((((maturity - ncd).days)/(365.25/2)),0)

    if(ncd == maturity):
        bp = (ncd-s)/(365/2)
    else:
        bp = (ncd-s)/(ncd-lcd)

    if(ncd==maturity):
        bpf = f/(f+(bp*(1-f)))
    else:
        bpf = f**bp

    if(ncd==maturity):
        dbpf = (bp*(bpf**2))/(f**2)
    else:
        dbpf = (bp*bpf)/f

    if(f==1):
        dcpn=cpn*((n*(n+1))/2)
    else:
        dcpn=cpn*((1-(n-(n*f)+1)*(f**n))/((1-f)**2))

    dr=n*1*(f**(n-1))

    daip = dbpf*(aip/bpf) + bpf*(dcpn+dr)

    delta = 1*((f**2)/200)*(daip/(dy))

    rpbp = 10000*delta

    return rpbp

def convexityfinal(s, lcd, ncd, bcd, maturity, cb, yieldm, dy=1):

    aip = allInPrice(s, lcd, ncd, bcd, maturity, cb, yieldm)

    cpn = cb/2

    f = (1+(yieldm/2))**-1

    n = round((((maturity - ncd).days)/(365.25/2)),0)


    if(ncd == maturity):
        bp = (ncd-s)/(365/2)
    else:
        bp = (ncd-s)/(ncd-lcd)

    if(ncd==maturity):
        bpf = f/(f+(bp*(1-f)))
    else:
        bpf = f**bp

    if(ncd==maturity):
        dbpf = (bp*(bpf**2))/(f**2)
    else:
        dbpf = (bp*bpf)/f

    if(ncd==maturity):
        d2bpf = (2*dbpf)*((bp*bpf - f)/(f**2))
    else:
        d2bpf = dbpf*((bp-1)/f)

    if(f==1):
        dcpn=cpn*((n*(n+1))/2)
    else:
        dcpn=cpn*((1-(n-(n*f)+1)*(f**n))/((1-f)**2))

    if(f==1):
        d2cpn = cpn*((n*((n**2)-1))/3)
    else:
        d2cpn = cpn*((2-((n*(1-f)*(2+(n-1)*(1-f))+(2*f))*(f**(n-1))))/((1-f)**3))

    dr=n*1*(f**(n-1))

    d2r=n*(n-1)*1*(f**(n-2))

    daip = dbpf*(aip/bpf) + bpf*(dcpn+dr)

    d2aip = d2bpf*(aip/bpf) + dbpf*(((bpf*daip - aip*dbpf)/(bpf**2))+dcpn+dr)+bpf*(d2cpn+d2r)

    diff2 = ((((daip/dy)*(f**3))/2) + (((d2aip/(dy**2))*(f**4))/4))/10000

    conv = (10000/aip)*diff2

    return conv


def dmod(delta,aip):
    dmod = 100*(delta/aip)
    return dmod


def seconddiff(daip, d2aip, f, dy):
    diff2 = ((((daip/dy)*(f**3))/2) + (((d2aip/(dy**2))*(f**4))/4))/10000
    return diff2

def conv(aip, diff2):
    conv = (10000/aip)*diff2
    return conv

def allInPrice(s, lcd, ncd, bcd, maturity, coupon, yieldm):

    n = round((((maturity - ncd).days)/(365.25/2)),0)

    if(s < bcd):
        cum = 1
    else:
        cum = 0

    if (cum == 1):
        daysacc = (s - lcd).days
    else:
        daysacc = (s-ncd).days

    cpn=(coupon/2)
    
    cpnNCD = (cpn)*cum

    f = (1+(yieldm/2))**-1

    if(ncd == maturity):
        bp = (ncd-s)/(365/2)
    else:
        bp = (ncd-s)/(ncd-lcd)


    if(ncd==maturity):
        bpf = f/(f+(bp*(1-f)))
    else:
        bpf = f**bp

    accint = (daysacc*coupon)/365

    accintRound = round((daysacc*coupon)/365,7)

    if(f==1):
        price=cpnNCD+(cpn*n) + 1
    else:
        price = bpf*(cpnNCD+(cpn*((f*(1-(f**n)))/(1-f))+(1*(f**n))))

    cleanPriceRound = round((price - accint),7)

    priceRound = (cleanPriceRound  + accintRound)

    return priceRound
    