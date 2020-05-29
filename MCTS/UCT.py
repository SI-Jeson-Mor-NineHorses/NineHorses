# TODO: UCT class
import sys
import math
import MCTS.State

class UCT:

    @staticmethod
    def uctValue(totalVisit, nodeWinScore, nodeVisit):
        if(nodeVisit == 0):
            return sys.maxsize

        return (nodeWinScore / float(nodeVisit)) + 1.41 + math.sqrt(math.log(totalVisit/float(nodeVisit)))

    @staticmethod
    def findBestNodeWithUCT(node):
        parentVisit = node.getState().MCTS.State.getVisitCount()
        best = 0
        for c in node.getChildArray():
            c = UCT.uctValue(parentVisit, c.getState().getWinScore(), c.getState().getVisitCount())
            if c > best:
                best = c
        return best
