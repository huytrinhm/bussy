from heapq import heappop, heappush
from itertools import count

def stress_centrality(G, weight):
  r"""Modified from networkx betweenness_centrality algorithm.

  Parameters
  ----------
  G : graph
    A NetworkX graph.

  weight : string
    Holds the name of the edge attribute used as weight.
    Weights are used to calculate weighted shortest paths, so they are
    interpreted as distances.

  Returns
  -------
  nodes : dictionary
    Dictionary of nodes with stress centrality as the value.

  References
  ----------
  .. [1] Ulrik Brandes:
    On Variants of Shortest-Path Betweenness
    Centrality and their Generic Computation.
    Social Networks 30(2):136-145, 2008.
    https://doi.org/10.1016/j.socnet.2007.11.001
  """
  stress = dict.fromkeys(G, 0)  # s[v]=0 for v in G
  nodes = G
  for s in nodes:
    S, P, sigma, _ = _single_source_dijkstra_path_basic(G, s, weight)
    stress = _accumulate_endpoints(stress, S, P, sigma, s)

  return stress

def _single_source_dijkstra_path_basic(G, s, weight):
    if G.is_multigraph():
        weight = lambda u, v, d: min(attr.get(weight, 1) for attr in d.values())
    else:
      weight = lambda u, v, data: data.get(weight, 1)

    S = []
    P = {}
    for v in G:
        P[v] = []
    sigma = dict.fromkeys(G, 0)  # sigma[v]=0 for v in G
    D = {}
    sigma[s] = 1
    push = heappush
    pop = heappop
    seen = {s: 0}
    c = count()
    Q = []  # use Q as heap with (distance,node id) tuples
    push(Q, (0, next(c), s, s))
    while Q:
        (dist, _, pred, v) = pop(Q)
        if v in D:
            continue  # already searched this node.
        sigma[v] += sigma[pred]  # count paths
        S.append(v)
        D[v] = dist
        for w, edgedata in G[v].items():
            vw_dist = dist + weight(v, w, edgedata)
            if w not in D and (w not in seen or vw_dist < seen[w]):
                seen[w] = vw_dist
                push(Q, (vw_dist, next(c), v, w))
                sigma[w] = 0
                P[w] = [v]
            elif vw_dist == seen[w]:  # handle equal paths
                sigma[w] += sigma[v]
                P[w].append(v)
    return S, P, sigma, D

def _accumulate_endpoints(stress, S, P, sigma, s):
    stress[s] += len(S) - 1
    delta = dict.fromkeys(S, 0)
    while S:
        w = S.pop()
        for v in P[w]:
            delta[v] += 1 + delta[w]
        if w != s:
            stress[w] += sigma[w]*delta[w]
    return stress
