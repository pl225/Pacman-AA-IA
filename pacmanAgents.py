# pacmanAgents.py
# ---------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from pacman import Directions
from game import Agent
import random
import game
import util
from searchAgents import PositionSearchProblem

class LeftTurnAgent(game.Agent):
  "An agent that turns left at every opportunity"
  
  def getAction(self, state):
    legal = state.getLegalPacmanActions()
    current = state.getPacmanState().configuration.direction
    if current == Directions.STOP: current = Directions.NORTH
    left = Directions.LEFT[current]
    if left in legal: return left
    if current in legal: return current
    if Directions.RIGHT[current] in legal: return Directions.RIGHT[current]
    if Directions.LEFT[left] in legal: return Directions.LEFT[left]
    return Directions.STOP

class GreedyAgent(Agent):
  def __init__(self, evalFn="scoreEvaluation"):
    self.evaluationFunction = util.lookup(evalFn, globals())
    assert self.evaluationFunction != None
        
  def getAction(self, state):
    # Generate candidate actions
    legal = state.getLegalPacmanActions()
    if Directions.STOP in legal: legal.remove(Directions.STOP)
      
    successors = [(state.generateSuccessor(0, action), action) for action in legal] 
    scored = [(self.evaluationFunction(state), action) for state, action in successors]
    bestScore = max(scored)[0]
    bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
    return random.choice(bestActions)

class PacmanAgent(game.Agent):

    def getPacmanSuccessors(self, legalActions, state):
      return [(state.generateSuccessor(self.index, action), action, state.generateSuccessor(self.index, action).getPacmanPosition()) for action in legalActions]

    def getAction(self, state):
        from util import PriorityQueue, Counter, manhattanDistance

        foodGrid = state.getFood()
        foodList = list(foodGrid.asList())

        _, nextFood = min([(manhattanDistance(state.getPacmanPosition(), food), food) for food in foodList])

        fila = PriorityQueue()
        fila.push((state, []), 0)
        visitados = set()
        
        while fila.heap:
            currentState, actionSequence = fila.pop()

            if currentState.getPacmanPosition() == nextFood:
              if len(actionSequence) > 0:
                return actionSequence[0]
              else:
                return  currentState.getLegalPacmanActions()[0]

            for nextState, nextAction, nextPosition in self.getPacmanSuccessors(currentState.getLegalActions(self.index), currentState):
                if not nextPosition in state.getGhostPositions():
                  if nextPosition not in visitados:
                    visitados.add(nextPosition)  
                    acaoCompleto = actionSequence + [nextAction]  
                    fila.push((nextState, acaoCompleto), len(acaoCompleto) + manhattanDistance(nextFood, state.getPacmanPosition()))

        for _, action, pacmanNextPosition in self.getPacmanSuccessors(state.getLegalPacmanActions(), state):
          if pacmanNextPosition not in state.getGhostPositions() and action != 'Stop': 
            return action
        return random.choice(state.getLegalPacmanActions())

def scoreEvaluation(state):
  return state.getScore()  