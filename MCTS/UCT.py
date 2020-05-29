# TODO: UCT class
import sys
import math
import MCTS.State


def uctValue(totalVisit, nodeWinScore, nodeVisit):
    if nodeVisit == 0:
        return sys.maxsize

    return (nodeWinScore / float(nodeVisit)) + 1.41 + math.sqrt(math.log(totalVisit)/float(nodeVisit))


def findBestNodeWithUCT(node):
    parentVisit = node.getState().getVisitCount()
    max = 0
    best = None
    for c in node.getChildArray():
        x = uctValue(parentVisit, c.getState().getWinScore(), c.getState().getVisitCount())
        if x > best:
            best = c
    return best
