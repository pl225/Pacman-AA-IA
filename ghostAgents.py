# ghostAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from game import Agent
from game import Actions
from game import Directions
import random
from util import manhattanDistance
import util

class GhostAgent( Agent ):
  def __init__( self, index ):
    self.index = index

  def getAction( self, state ):
    dist = self.getDistribution(state)
    if len(dist) == 0: 
      return Directions.STOP
    else:
      return util.chooseFromDistribution( dist )
    
  def getDistribution(self, state):
    "Returns a Counter encoding a distribution over actions from the provided state."
    util.raiseNotDefined()

class RandomGhost( GhostAgent ):
  "A ghost that chooses a legal action uniformly at random."
  def getDistribution( self, state ):
    dist = util.Counter()
    for a in state.getLegalActions( self.index ): dist[a] = 1.0
    dist.normalize()
    return dist

class DirectionalGhost( GhostAgent ):
  "A ghost that prefers to rush Pacman, or flee when scared."
  def __init__( self, index, prob_attack=0.8, prob_scaredFlee=0.8 ):
    self.index = index
    self.prob_attack = prob_attack
    self.prob_scaredFlee = prob_scaredFlee
  
  def getGhostSuccessors(self, legalActions, state):
      return [(state.generateSuccessor(self.index, action), action, state.generateSuccessor(self.index, action).getGhostPosition(self.index)) for action in legalActions]
      
  def getDistribution(self, state):
    from util import PriorityQueue, Counter, manhattanDistance

    ghostState = state.getGhostState(self.index)
    legalActions = state.getLegalActions(self.index)
    isScared = ghostState.scaredTimer > 0
    pacmanPosition = state.getPacmanPosition()
    dist = Counter()

    if not isScared:
      fila = PriorityQueue()
      visitados = set()
      fila.push((state,[]) , 0)

      for e in state.getGhostPositions():
        if e != state.getGhostPosition(self.index): visitados.add(e)
      
      while fila.heap:
        currentState , actionsSequence = fila.pop()
        for nextState, nextAction, nextPosition in self.getGhostSuccessors(currentState.getLegalActions(self.index), currentState):
          if not nextState.getGhostPosition(self.index) in visitados:
            if nextState.getGhostPosition(self.index) == pacmanPosition:
              if len(actionsSequence): dist[actionsSequence[0]] = 1 
              else: dist[state.getLegalActions(self.index)[0]] = 1
              return dist
            acaoCompleto =  actionsSequence + [nextAction]
            fila.push((nextState, acaoCompleto), len(acaoCompleto) + manhattanDistance(nextPosition, pacmanPosition))
            visitados.add(nextPosition)
     
    sucessors = self.getGhostSuccessors(legalActions, state)
    _, actionFlee = max((manhattanDistance(s[2], pacmanPosition), s[1]) for s in sucessors) 
    dist[actionFlee] = 1
    return dist

      