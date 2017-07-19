class Estado(object):
	def __init__(self, atual, pai, direcao):
		self.atual = atual
		self.pai = pai
		self.direcao = direcao
	def __eq__(self, other):
		return isinstance(other, Estado) and self.atual == other.atual	
	def __hash__(self):
		return hash(str(self.atual))    	
  
def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  from game import Directions
  from util import PriorityQueue
  
  estadoInicial = problem.getStartState()
  fila = PriorityQueue()
  vistos = set()
  fila.push(Estado(estadoInicial, None, None), 0)
  i = 0
  
  while fila.heap:
	i += 1
	estadoAtual = fila.pop()
	if problem.isGoalState(estadoAtual.atual):
		break
	vistos.add(estadoAtual)
	for estado in problem.getSuccessors(estadoAtual.atual):
		e = Estado(estado[0], estadoAtual, estado[1])
		if e not in vistos:
			prioridade = i + heuristic(e.atual, problem)
			fila.push(e, prioridade)
			
			
##############################################################################################################

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  from game import Directions
  from util import PriorityQueue
  
  estadoInicial = problem.getStartState()
  fila = PriorityQueue()
  vistos = set()
  fila.push(estadoInicial, 0)
  i = 0
  
  while fila.heap:
	i += 1
	estadoAtual = fila.pop()
	if problem.isGoalState(estadoAtual):
		break
	vistos.add(estadoAtual)
	for estado in problem.getSuccessors(estadoAtual):
		if estado[0] not in vistos:
			prioridade = i + heuristic(estado[0], problem)
			fila.push(estado[0], prioridade)