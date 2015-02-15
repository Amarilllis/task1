import sys
import time
import csv
from xml.dom.minidom import *
import sys


def InvDiv(x):
    try:
        res = 1 / x
    except ZeroDivisionError:
        res = float('inf')
    return res


def Floyd(graph):
    d = graph
    n = len(graph)
    for i in range(n):
        d[i][i] = 0

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if i != j:
                    d[i][j] = InvDiv(InvDiv(d[i][j]) + InvDiv(d[i][k]+d[k][j]))
    return d


def printMatrix(arr, mfile):
    writer = csv.writer(open(mfile, "w", newline=''), delimiter=',')
    for line in arr:
        newline = ["%.6f" % x for x in line]
        writer.writerow(newline)


def parseMatrix(mfile):
    elems = parse(mfile)

    nets = elems.getElementsByTagName("net")
    resistors = elems.getElementsByTagName("resistor")
    capactors = elems.getElementsByTagName("capactor")
    diods = elems.getElementsByTagName("diode")

    n = len(nets)

    graph = [[float('inf')] * n for i in range(n)]
    for i in range(n):
        graph[i][i] = 0

    for x in resistors:
        u = int(x.attributes['net_from'].value) - 1
        v = int(x.attributes['net_to'].value) - 1
        w = float(x.attributes['resistance'].value)
        graph[u][v] = InvDiv(InvDiv(w) + InvDiv(graph[u][v]))
        graph[v][u] = InvDiv(InvDiv(w) + InvDiv(graph[v][u]))

    for x in capactors:
        u = int(x.attributes['net_from'].value) - 1
        v = int(x.attributes['net_to'].value) - 1
        w = float(x.attributes['resistance'].value)
        graph[u][v] = InvDiv(InvDiv(w) + InvDiv(graph[u][v]))
        graph[v][u] = InvDiv(InvDiv(w) + InvDiv(graph[v][u]))

    for x in diods:
        u = int(x.attributes['net_from'].value) - 1
        v = int(x.attributes['net_to'].value) - 1
        w_from = float(x.attributes['resistance'].value)
        w_to = float(x.attributes['reverse_resistance'].value)
        graph[u][v] = InvDiv(InvDiv(w_from) + InvDiv(graph[u][v]))
        graph[v][u] = InvDiv(InvDiv(w_to) + InvDiv(graph[v][u]))

    return graph


def Solve():
    runtime = time.clock()
    inputfile, outputfile = sys.argv[1], sys.argv[2]

    graph = parseMatrix(inputfile)

    res = Floyd(graph)
    printMatrix(res, outputfile)

    print(time.clock() - runtime)

Solve()
