from src.Graph import Graph
import heapq

def modularity_clustering(G: Graph, verbose = False):
    def compute_update_deltas(deltas, a, merge_i, merge_j):
        # computes delta indices that need to be deleted from heap
        # computes new delta values that need to be added to heap
        # -> we delete and insert instead of updating because of the heap datastructure
        sub_deltas = {} # get all deltas that are relevant for current merge choices (tuples containing i or j)
        for idx,(delta,(u,v)) in enumerate(deltas):
            if {u,v} == {merge_i, merge_j}:
                continue
            if u in [merge_i, merge_j] or v in [merge_i,merge_j]:
                sub_deltas[(u,v)]=(delta,idx)   # also save index of where we found it in »deltas« so we can delete it later if necessary

        i_neighbors = set([n for N in G.edges for n in G.edges[N] if N in clusters[merge_i]])
        j_neighbors = set([n for N in G.edges for n in G.edges[N] if N in clusters[merge_j]])
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
            if cl_nodes & j_neighbors and cl_nodes & i_neighbors:
                updated_delta = (delta - delta_j, (u,v))
            elif cl_nodes & i_neighbors:
                updated_delta = (delta + 2*a[merge_i]*a[l], (u,v))
            elif cl_nodes & j_neighbors:
                updated_delta = (delta + 2*a[merge_j]*a[l], (u,v))
            if updated_delta is not None:
                q_idx_to_delete.append(q_idx)
                q_updates.append(updated_delta)
        return q_idx_to_delete, q_updates

    nodes = sorted(list(G.get_internal_nodes()))
    clusters = {i:{n} for i,n in enumerate(nodes)} # save clusters with their "ID"
    degrees = {n: len(G.edges[n]) for n in G.edges}
    a = {i: degrees[n]/(2*G.m) for i,n in enumerate(nodes)}
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
            values = (-change,(i,j)) # init delta = -(init delta) because we have a min heap
            deltas.append(values)
    heapq.heapify(deltas)

    while len(clusters)>1:
        _, (merge_i, merge_j)= heapq.heappop(deltas)
        if verbose:
            print("merge", (merge_i,merge_j))
        clusters[merge_i] = clusters[merge_i] | clusters[merge_j]
        a[merge_i]+=a[merge_j]

        q_idx_to_delete, q_updates = compute_update_deltas(deltas, a, merge_i, merge_j)

        # delete all variables associated with j and update deltas by deletion and re-insertion
        del clusters[merge_j]
        del a[merge_j]
        q_idx_to_delete.reverse() # index array is ordered (ascending). reverse because otherwise indices would not match after deletion
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
    
    # translate internal ids
    new_clusters = [] 
    for c in clusters:
        new_c = set()
        for i in clusters[c]:
            new_c.add(G.internal_ids_node_ids[i])
        new_clusters.append(new_c)

    return new_clusters

if __name__ == "__main__":
    G = Graph()
    G.read_graph_as_edge_list("../../networks/special_case_for_networkx.mtx")
    clusters = modularity_clustering(G)
    print(clusters)