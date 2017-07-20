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

class PacmanAgent(game.Agent): # Abordagem 1: o objetivo eh a comida mais próxima que nao esta ocupada por um fantasma

    def getPacmanSuccessors(self, legalActions, state):
      return [(state.generateSuccessor(self.index, action), action, state.generateSuccessor(self.index, action).getPacmanPosition()) for action in legalActions]

    def getAction(self, state):
        from util import PriorityQueue, Counter, manhattanDistance

        foodGrid = state.getFood() # carrega o grid de comidas do estado atual
        foodList = list(foodGrid.asList())

        _, nextFood = min([(manhattanDistance(state.getPacmanPosition(), food), food) for food in foodList]) # identifica a comida mais proxima que sera o objetivo

        fila = PriorityQueue() # inicia as estruturas de dados necessarias a busca A*
        fila.push((state, []), 0)
        visitados = set()
        
        while fila.heap:
            currentState, actionSequence = fila.pop() # remove um no da borda

            if currentState.getPacmanPosition() == nextFood: # verifica o objetivo
              if len(actionSequence) > 0:
                return actionSequence[0]
              else:
                return  currentState.getLegalActions[0]

            visitados.add(currentState.getPacmanPosition()) # adiciona estado ao conjunto de visitados

            for nextState, nextAction, nextPosition in self.getPacmanSuccessors(currentState.getLegalActions(self.index), currentState): # procura estados sucessores do estado atual
                if not nextPosition in state.getGhostPositions():# or state.getGhostState(1).scaredTimer > 0: # verifica se a solucao nao possui fantasmas
                  if nextPosition not in visitados:  # adiciona o estado a fila, se ainda nao foi visitado
                    acaoCompleto = actionSequence + [nextAction]  
                    fila.push((nextState, acaoCompleto), len(acaoCompleto) + manhattanDistance(nextFood, state.getPacmanPosition()))

        for _, action, pacmanNextPosition in self.getPacmanSuccessors(state.getLegalPacmanActions(), state): # caso nao exista posicao otima, seleciona a primeira
          if pacmanNextPosition not in state.getGhostPositions() and action != 'Stop': # acao valida que nao possua fantasmas
            return action
        return random.choice(state.getLegalPacmanActions()) # caso o pacman esteja em xeque-mate, seleciona uma acao aleatoria

class PacmanAgentFoodManhattan(game.Agent): # Abordagem 2: o objetivo eh a comida mais proxima que esteja a uma distancia minima de manhattan a um fantasma

    def getPacmanSuccessors(self, legalActions, state):
      return [(state.generateSuccessor(self.index, action), action, state.generateSuccessor(self.index, action).getPacmanPosition()) for action in legalActions]

    def avaliaPosicoes(self, food, posicoesFantasmas, i): # avalia posicoes pela distancia Manhattan ao objeto comida ou fantasma
        from util import manhattanDistance
        for p in posicoesFantasmas:
            if manhattanDistance(p, food) < i:
                return False

        return True

    def getAction(self, state):
        from util import PriorityQueue, Counter, manhattanDistance

        foodGrid = state.getFood() # carrega o grid de comidas do estado atual
        foodList = list(foodGrid.asList())

        _, nextFood = min([(manhattanDistance(state.getPacmanPosition(), food), food) for food in foodList if self.avaliaPosicoes(food, state.getGhostPositions(), 7) or state.getGhostState(1).scaredTimer > 0]) # identifica a comida mais proxima que sera o objetivo

        fila = PriorityQueue() # inicia as estruturas de dados necessarias a busca A*
        fila.push((state, []), 0)
        visitados = set()
        
        while fila.heap:
            currentState, actionSequence = fila.pop() # remove um no da borda

            if currentState.getPacmanPosition() == nextFood: # verifica o objetivo
              if len(actionSequence) > 0:
                return actionSequence[0]
              else:
                return  currentState.getLegalActions[0]

            visitados.add(currentState.getPacmanPosition()) # adiciona estado ao conjunto de visitados

            for nextState, nextAction, nextPosition in self.getPacmanSuccessors(currentState.getLegalActions(self.index), currentState): # procura estados sucessores do estado atual
                if self.avaliaPosicoes(nextPosition, state.getGhostPositions(), 2) or state.getGhostState(1).scaredTimer > 0: # verifica se a solucao nao possui fantasmas
                  if nextPosition not in visitados:  # adiciona o estado a fila, se ainda nao foi visitado
                    acaoCompleto = actionSequence + [nextAction]  
                    fila.push((nextState, acaoCompleto), len(acaoCompleto) + manhattanDistance(nextFood, state.getPacmanPosition()))

        for _, action, pacmanNextPosition in self.getPacmanSuccessors(state.getLegalPacmanActions(), state): # caso nao exista posicao otima, seleciona a primeira
          if pacmanNextPosition not in state.getGhostPositions() and action != 'Stop': # acao valida que nao possua fantasmas
            return action
        return random.choice(state.getLegalPacmanActions()) # caso o pacman esteja em xeque-mate, seleciona uma acao aleatoria


def scoreEvaluation(state):
  return state.getScore()  