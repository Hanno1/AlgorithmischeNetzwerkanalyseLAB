from Graph import Graph

def breadthSearch(g: Graph,node_IDs: list,visited: list,parent: list,queue: list):
    current_node = queue.pop()
    for node_id in g.getNeighbors(node_IDs[current_node]):
        node = node_IDs.index(node_id)
        if not visited[node]:
            visited[node] = True
            parent[node] = current_node
            queue.append(node)

def checkCollision(number_of_nodes,s_visited: list,t_visited: list):
    for i in range(number_of_nodes):
         if s_visited[i] == t_visited[i]:
             return i
    return -1

def bidrSearch(g: Graph,s_id,t_id):
    node_IDs = list(g.nodes.keys())
    s = node_IDs.index(s_id); t = node_IDs.index(t_id)
    shortes_path = []

    s_visited = [False]*g.n
    t_visited = [False]*g.n

    s_queue = []
    t_queue = []

    s_parent = [-1]*g.n
    t_parent = [-1]*g.n

    s_visited[s] = True
    s_queue.append(s)
    t_visited[t] = True
    t_queue.append(t)

    while s_queue or t_queue:
        breadthSearch(g,node_IDs,s_visited,s_parent,s_queue)
        breadthSearch(g,node_IDs,t_visited,t_parent,t_queue)
        intersection = checkCollision(g.n,s_visited,t_visited)
        if intersection != -1:
            i = intersection
            shortes_path.append(node_IDs[i])
            while i != s:
                shortes_path.append(node_IDs[s_parent[i]])
                i = s_parent[i]
            shortes_path.reverse()
            i = intersection
            while i != t:
                shortes_path.append(node_IDs[t_parent[i]])
                i = t_parent[i]
            return shortes_path, len(shortes_path)
