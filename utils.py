from random import random, randint, uniform
from math import log, e


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


def generateTimesU(length):
    times = [0]
    while True:
        u = randint(0, length)
        times.append(times[-1] + u)
        if times[-1] >= 4800:
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
        generateTimesU(*args)
