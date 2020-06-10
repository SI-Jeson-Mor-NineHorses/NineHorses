# TODO: UCT class
import sys
import math


def calcUctValue(totalVisit, nodeWinScore, nodeVisit):
    if nodeVisit == 0:
        return 0
    return (nodeWinScore / float(nodeVisit)) + 1.4 * math.sqrt(math.log(totalVisit)/float(nodeVisit))


def uctValue(totalVisit, nodeWinScore, nodeVisit):
    if nodeVisit == 0:
        return sys.maxsize
    return (nodeWinScore / float(nodeVisit)) + 1.4 * math.sqrt(math.log(totalVisit)/float(nodeVisit))


def findBestNodeWithUCT(node):
    parentVisit = node.getState().getVisitCount()
    # best = random.choice(node.getChildArray())
    best = node.getChildArray()[0]

    for c in node.getChildArray():
        if c.getState().getVisitCount() < best.getState().getVisitCount():
            best = c

    for c in node.getChildArray():
        x = uctValue(parentVisit, c.getState().getWinScore(), c.getState().getVisitCount())
        # sprawdzić z modulo
        if x > best.getState().getWinScore() and c.getState().getVisitCount() < 50:
            best = c
    return best
