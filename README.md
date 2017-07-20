# Pacman-AA-IA

Este trabalho é um projeto da disciplina Inteligência Artificial (2017.1) da UFRRJ, ministrada pelo professor Leandro Alvim.  
O trabalho consiste no término da implementação do jogo Pacman escrito na linguagem Python utilizando o conteúdo visto na disciplina.

O objetivo do jogo é fazer com que o Pacman encontre caminhos no labirinto para chegar a um destino e para coletar comida eficientemente.

A descrição original do trabalho se encontra disponível em: http://www2.ic.uff.br/~bianca/ia/t1.html.  

Neste projeto, foram realizados o passo 4 e 5 descritos no link, brevemente resumidos abaixo:

Passo 4: Utilizar o algoritmo de busca A* de forma que os fantasmas cerquem o Pacman.  
Passo 5: Garantir que o Pacman deve, sempre que possível, tentar coletar utilizando uma rota em que não há fantasmas.  

Links para a visualização do jogo em funcionamento: 

-> Jogo sem fantasmas: https://youtu.be/KXUoPIn6bs8  
-> Jogo com fantasmas: https://youtu.be/wzl4DgcMYD4  

Comandos: </br>
  python pacman.py -g GhostAgent -p PacmanAgent (comida mais próxima) </br>
  python pacman.py -g GhostAgent -p PacmanAgent -k 0 (nenhum fantasma) </br>
  python pacman.py -g GhostAgent -p PacmanAgentFoodManhattan (comida mais próxima distância Manhattan) </br>
  python pacman.py -g GhostAgent -p PacmanAgentFoodManhattan -k 0 </br>
  
  opcional: -l originalClassic OU contestClassic ou outros mapas.

Trabalho realizado por: Matheus Abreu, Julia Rodrigues e João Victor Araújo.

