from src.Graph import Graph

if __name__ == "__main__":
    import heapq
    G = Graph()
    G.add_edge(1,2)
    G.add_edge(3,2)
    G.add_edge(4,2)
    G.add_edge(4,1)
    G.add_edge(5,6)
    G.add_node(7)
    nodes = sorted(list(G.get_internal_nodes()))
    print(nodes)
    # save clusters with their "ID"
    clusters = {i:{n} for i,n in enumerate(nodes)}
    degrees = {n: len(G.edges[n]) for n in G.edges}
    a = {n: degrees[n]/(2*G.m) for n in degrees}
    deltas = []
    # init deltas
    for i in range(G.n):
        n_i = nodes[i]
        for j in range(i+1, G.n):
            n_j = nodes[j]
            if n_j in G.edges[n_i]: 
                change = 1/G.m - (2*degrees[n_i]*degrees[n_j])/(4*G.m**2)
            else:
                change = - (2*degrees[n_i]*degrees[n_j])/(4*G.m**2)
            values = (-change,(n_i,n_j)) # init delta = -(init delta) because we have a min heap
            deltas.append(values)
    heapq.heapify(deltas)
    while len(clusters)>1:
        _, (merge_i, merge_j)= heapq.heappop(deltas)
        clusters[merge_i] = clusters[merge_i] | clusters[merge_j]
        a[merge_i]+=a[merge_j]
        union_neighbors = G.edges[merge_i] | G.edges[merge_j]
        i_neigbors = G.edges[merge_i] - G.edges[merge_j]
        j_neigbors = G.edges[merge_j] - G.edges[merge_i]

        sub_deltas = {} # get all deltas that are relevant for current merge choices (tuples containing i or j)
        for idx,(delta,(u,v)) in enumerate(deltas):
            if {u,v} == {merge_i, merge_j}:
                continue
            if u in [merge_i, merge_j] or v in [merge_i,merge_j]:
                sub_deltas[(u,v)]=(delta,idx)   # also save index of where we found it in »deltas« so we can change it later
        # example sub_deltas = {(0, 1): (-0.08, 1), (1, 3): (-0.08, 3), (1, 6): (-0.0, 4), (2, 4): (0.02, 5), 
        #                       (2, 6): (-0.0, 6), (0, 2): (0.04, 7), (2, 3): (0.04, 10), (1, 4): (0.06, 11)}
        # for merge_i = 1, merge_j=2 

        q_idx_to_delete = []
        q_updates = []

        # now we need to update the deltas
        for c_idx in sub_deltas: # iterate over all deltas that might change
            u, v = c_idx  # cluster indices
            delta, q_idx = sub_deltas[c_idx] # get the delta for cluster-change (u,v) and the associated queue-index q_idx for »deltas»
            if merge_j in [u,v]: # if the "merged-in" cluster is part of the delta-variable it is not changed (its deleted later)
                q_idx_to_delete.append(q_idx) # for deletion of with merge_j associated variables later
                continue
            l = v if u == merge_i else u # assign l to the other cluster-index, thats not part of the merge
            cl_nodes =set() 
            for n in clusters[l]:
                try:
                    cl_nodes |= G.edges[n]
                except:
                    pass

            if merge_j>l: # get change for cluster-merge (merge_j, l)
                delta_j, _ = sub_deltas[(l,merge_j)]
            else:
                delta_j, _ = sub_deltas[(merge_j,l)]

            # update deltas depending on cluster l nodes' connections with the merged clusters
            # update = -(update) from lectures because we have a min heap
            updated_delta = None
            if cl_nodes & j_neigbors and cl_nodes & i_neigbors:
                updated_delta = (delta - delta_j, (u,v))
            elif cl_nodes & i_neigbors:
                updated_delta = (delta + 2*a[merge_i]*a[l], (u,v))
            elif cl_nodes & j_neigbors:
                updated_delta = (delta + 2*a[merge_j]*a[l], (u,v))
            if updated_delta is not None:
                q_idx_to_delete.append(q_idx)
                q_updates.append(updated_delta)

        # delete all variables associated with j 
        del clusters[merge_j]
        del a[merge_j]
        q_idx_to_delete.reverse()
        for idx in q_idx_to_delete:
            del deltas[idx]
        for update in q_updates:
            heapq.heappush(deltas,update)

        done = True
        for (d,_) in deltas: # check if done: if all values in queue are > 0 (because we have a min-heap and we reversed the deltas)
            if d<0:
                done=False
                break
        if done:
            break
    print(clusters) 