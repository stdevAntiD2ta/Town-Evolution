from random import random, randint, uniform, shuffle 
from math import log, e
from colors import *
import logging

datefmt ='%Y-%m-%d %H:%M:%S'
formatC  = f'%(color)s%(levelname)s{RESET} - {BLACKB}%(name)s{RESET} - {GREEN}%(method)s{RESET} - %(message)s'
formatF  = f'%(asctime)s - %(levelname)s - %(name)s - %(method)s - %(message)s'

breakup = {
    (12, 15): 0.0815,
    (15, 21): 0.0415,
    (21, 35): 0.0415,
    (35, 45): 0.0208,
    (45, 60): 0.0105,
    (60, 125): 0.0052,
    (125, 200): 0.0000001
}

deathM = {
    (0, 12): 0.25,
    (12, 45): 0.1,
    (45, 76): 0.3,
    (76, 125): 0.7,
    (125, 200): 1.0
}

deathF = {
    (0, 12): 0.25,
    (12, 45): 0.15,
    (45, 76): 0.35,
    (76, 125): 0.65,
    (125, 200): 1.0
}

pregnant = {
    (12, 15): 0.2,
    (15, 21): 0.45,
    (21, 35): 0.8,
    (35, 45): 0.4,
    (45, 60): 0.2,
    (60, 125): 0.05,
    (125, 200): 0.0
}

childrenNumber = {
    1: 0.6,
    2: 0.75,
    3: 0.35,
    4: 0.2,
    5: 0.1,
    99999: 0.05
}

wishCouple = {
    (12, 15): 0.6,
    (15, 21): 0.65,
    (21, 35): 0.8,
    (35, 45): 0.6,
    (45, 60): 0.5,
    (60, 125): 0.2,
    (125, 200): 0.0
}

makeCouple = {
    (0, 5): 0.45,
    (5, 10): 0.4,
    (10, 15): 0.35,
    (15, 20): 0.25,
    (20, 100): 0.15,
    (100, 200): 0.0
}

childrenBorn = {
    1: 0.7,
    2: 0.18,
    3: 0.06,
    4: 0.04,
    5: 0.02
}


def LoggerFactory(name="root", log=False):
    '''
    Create a custom logger to use colors in the logs
    '''
    logging.setLoggerClass(Logger)
    if log:
        logging.basicConfig(format=formatF, datefmt=datefmt, filename='./logs/log.log', filemode='w')
    else:
        logging.basicConfig(format=formatC, datefmt=datefmt)
    return logging.getLogger(name=name)


class Logger(logging.getLoggerClass()):
    
    def __init__(self, name = "root", level = logging.NOTSET):
        self.debug_color =  BLUEB
        self.info_color = YELLOWB
        self.error_color = REDB
        return super().__init__(name, level)
        
    def debug(self, msg, mth=""):
        super().debug(msg, extra={"color": self.debug_color, "method": mth})
        
    def info(self, msg, mth=""):
        super().info(msg, extra={"color": self.info_color, "method": mth})
        
    def error(self, msg, mth=""):
        super().error(msg, extra={"color": self.error_color, "method": mth})
        
    def change_color(self, method, color):
        setattr(self, f"{method}_color", color)


def Bernoulli(p):
    return random() <= p


def exponential(lamb, u):
    return -log(u) / lamb


def poissonHomogeneous(lamb, t):         
    accum = 1                   
    n = 0               
    data = [0]                                           
    while True:
        u = random()  
        accum *= u 
        ex = exponential(lamb, u)
        data.append(ex + data[len(data) - 1])
        n += 1
        if (-log(accum)/lamb) > t:
            return n, data


def generateTimesU(length, top):
    times = [0]
    while True:
        u = randint(0, length)
        times.append(times[-1] + u)
        if times[-1] >= top:
            return times
        

def generateTimesP(lamb, top):
    accum = 0
    last = 0
    times = [0]
    while True:
        _, data = poissonHomogeneous(lamb, top)
        for i in data[1:]:
            times.append(int(last + i))
            if last + i >= 4800:
                return times
        accum += data[-1]
        last = accum
    

def generateTimes(kind, *args):
    if kind == "Poisson":
        return generateTimesP(*args)
    elif kind == "Uniform":
        return generateTimesU(*args)

def generateChildrenNumber():
    cn = [(p, n) for n, p in childrenNumber.items()]
    cn.sort()
    u = random()
    for p in cn:
        if u <= p[0]:
            return p[1]
    return cn[-1][1]


def getAgeRange(age, d):
    for l, h in d.keys():
        if l <= age//48 and age//48 < h:
            return (l, h)


def generateDeath(sex, age, date):
    deathP = {}
    if sex == 'male':
        deathP = deathM
    else:
        deathP = deathF

    ageRange = getAgeRange(age, deathP)
    t = randint(date, date + ageRange[1] * 48 - age)
    return Bernoulli(deathP[ageRange]), t


def generateBreakup(age):
    ageRange = getAgeRange(age, breakup)
    return int(exponential(breakup[ageRange], random()))


def generateWishCouple(age):
    ageRange = getAgeRange(age, wishCouple)
    return Bernoulli(wishCouple[ageRange])


def marry(age1, age2):
    dif = abs(age1 - age2) // 48
    for t, p in makeCouple.items():
        if dif < t[1]:
            return Bernoulli(p)
    

def generatePregnancy():
    cb = [(p, n) for n, p in childrenBorn.items()]
    cb.sort()
    u = random()
    for p in cb:
        if u <= p[0]:
            return p[1]
    return cb[-1][1]
    

def generateBirth(age):
    ageRange = getAgeRange(age, pregnant)
    return Bernoulli(pregnant[ageRange])