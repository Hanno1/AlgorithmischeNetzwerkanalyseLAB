# AlgorithmischeNetzwerkanalyseLAB

1. Aufgabenblatt:

Aufgabe 1:

Klasse Knoten:
- name
- id
(- Knotengrad bekommen wir aus der Kantenmenge)

Klasse Graph:
- max Knoten id
- Knotenmenge als Dictionary {1: Instanziierung der Knotenklasse}
- Kanten als Dictionary {1: {2, 3}, 2: {1, 3} ...} Knoten 

- addNode()
- addEdge()

- new Graph() -> erzeugt leeren Graph...

METIS:

Zeile 1: n m (n - Knotenanzahl, m - Kantenanzahl)
Zeile 2 - m (i): Nachbarschaft von Knoten i