from src.Graph import Graph
import matplotlib.pyplot as plt
import time
import src.communities.two_plexe as Tp
import numpy as np
from src.communities.two_plex_real import search_2_plex_main


"""plt.rcParams.update({'font.size': 8})
G = Graph("../networks/out.ucidata-zachary_")
names = ["original", "first\nImprovement", "second\nImprovement",
         "third\nImprovement", "fourth\nImprovement", "test1", "test2"]
times = []
times_det = []

for i in range(7):
    start_time = time.time()
    Tp.search_2_plex(G, i)
    times.append(time.time() - start_time)

    start_time = time.time()
    Tpc.search_2_plex_det(G, i)
    times_det.append(time.time() - start_time)

fig = plt.figure(figsize=(7, 3))

X_axis = np.arange(len(names))

plt.bar(X_axis - 0.2, times, 0.4, label='nicht deterministisch')
#plt.bar(X_axis + 0.2, times_det, 0.4, label='deterministisch')

plt.xticks(X_axis, names)
plt.xlabel("Level of Improvement")
plt.ylabel("Time")
plt.title("Laufzeit der Algorithmen")
plt.legend()
plt.show()"""

G = Graph()
G.add_edge(1, 2)
G.add_edge(1, 3)
G.add_edge(2, 4)
G.add_edge(3, 4)
G.add_edge(2, 3)
G.add_edge(4, 5)
G.add_edge(0, 1)
