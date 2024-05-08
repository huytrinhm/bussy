import heapq
import math
from typing import List, Tuple

class Node():
  def __init__(self, data: object) -> None:
    self.data = data
    self.edges = []
  
  def __repr__(self) -> str:
    return str(self.edges)

class Graph():
  def __init__(self) -> None:
    self.Nodes = {}
    self.edge_count = 0

  @property
  def node_count(self) -> int:
    return len(self.Nodes)

  def __repr__(self) -> str:
    return str(self.Nodes)
  
  def updateNodes(self, nodes: List[Tuple[int, object]]) -> None:
    for node in nodes:
      k, v = node
      self.Nodes[k] = Node(v)

  def updateEdges(self, edges: List[Tuple[int, int, object]]) -> None:
    for edge in edges:
      u, v, data = edge
      if u not in self.Nodes or v not in self.Nodes:
        raise Exception('Invalid Nodes')
      self.Nodes[u].edges.append((v, data))
    self.edge_count += len(edges)

  def dijkstra(self, source):
    dists = dict.fromkeys(self.Nodes)
    from_edge = dict.fromkeys(self.Nodes)
    pq = []

    dists[source] = 0
    heapq.heappush(pq, (0, source))

    while pq:
      d, u = heapq.heappop(pq)
      
      if dists[u] is not None and d > dists[u]:
        continue

      for edge in self.Nodes[u].edges:
        v, edge_data = edge

        if dists[v] is None or d + edge_data['time'] < dists[v]:
          dists[v] = d + edge_data['time']
          from_edge[v] = {
            'StopId': u,
            **edge_data
          }
          heapq.heappush(pq, (dists[v], v))
    
    return dists, from_edge

  def dijkstra_with_stress_centrality_with_pred(self, source):
    dists = dict.fromkeys(self.Nodes)
    from_edge = dict.fromkeys(self.Nodes)
    path_count = dict.fromkeys(self.Nodes, 0)
    pred = {k: [] for k in self.Nodes}
    visit_order = []
    pq = []

    dists[source] = 0
    path_count[source] = 1
    heapq.heappush(pq, (0, source))

    while pq:
      d, u = heapq.heappop(pq)
      
      if dists[u] is not None and d > dists[u]:
        continue

      visit_order.append(u)
      
      for edge in self.Nodes[u].edges:
        v, edge_data = edge

        if dists[v] is not None and math.isclose(d + edge_data['time'], dists[v]):
          path_count[v] += path_count[u]
          pred[v].append(u)
          continue
        
        if dists[v] is None or d + edge_data['time'] < dists[v]:
          dists[v] = d + edge_data['time']
          from_edge[v] = {
            'StopId': u,
            **edge_data
          }
          path_count[v] = path_count[u]
          pred[v] = [u]
          heapq.heappush(pq, (dists[v], v))
    
    return dists, from_edge, path_count, visit_order, pred
  
  def dijkstra_with_stress_centrality(self, source):
    dists = dict.fromkeys(self.Nodes)
    from_edge = dict.fromkeys(self.Nodes)
    path_count = dict.fromkeys(self.Nodes, 0)
    visit_order = []
    pq = []

    dists[source] = 0
    path_count[source] = 1
    heapq.heappush(pq, (0, source))

    while pq:
      d, u = heapq.heappop(pq)
      
      if dists[u] is not None and d > dists[u]:
        continue

      visit_order.append(u)
      
      for edge in self.Nodes[u].edges:
        v, edge_data = edge

        if dists[v] is not None and math.isclose(d + edge_data['time'], dists[v]):
          path_count[v] += path_count[u]
          continue
        
        if dists[v] is not None and d + edge_data['time'] > dists[v]:
          continue
        
        if dists[v] is None or d + edge_data['time'] < dists[v]:
          dists[v] = d + edge_data['time']
          from_edge[v] = {
            'StopId': u,
            **edge_data
          }
          path_count[v] = path_count[u]
          heapq.heappush(pq, (dists[v], v))
    
    return dists, from_edge, path_count, visit_order

  def dijkstra_all(self):
    all_dists = {}
    all_trace = {}

    for node in self.Nodes:
      dists, from_edge = self.dijkstra(node)
      all_dists[node] = dists
      all_trace[node] = from_edge
    
    return all_dists, all_trace
    
  def dijkstra_all_with_stress_centrality(self):
    all_dists = {}
    all_trace = {}
    stress = dict.fromkeys(self.Nodes, 0)

    for node in self.Nodes:
      dists, from_edge, path_count, visit_order, pred = self.dijkstra_with_stress_centrality_with_pred(node)
      all_dists[node] = dists
      all_trace[node] = from_edge
      
      stress[node] += len(visit_order)
      delta = dict.fromkeys(self.Nodes, 0)
      for v in visit_order[::-1]:
        for u in pred[v]:
          delta[u] += 1 + delta[v]
        if v != node:
          stress[v] += path_count[v]*delta[v] + 1
    
    return all_dists, all_trace, stress
  
  def dijkstra_all_with_trace(self, with_preds=False):
    all_dists = {}
    all_trace = {}
    all_path_counts = {}
    all_visit_orders = {}
    if with_preds:
      all_preds = {}

    for node in self.Nodes:
      if with_preds:
        dists, from_edge, path_count, visit_order, pred = self.dijkstra_with_stress_centrality_with_pred(node)
        all_preds[node] = pred
      else:
        dists, from_edge, path_count, visit_order = self.dijkstra_with_stress_centrality(node)
      all_dists[node] = dists
      all_trace[node] = from_edge
      all_path_counts[node] = path_count
      all_visit_orders[node] = visit_order
    
    if with_preds:
      return all_dists, all_trace, all_path_counts, all_visit_orders, all_preds
    else:
      return all_dists, all_trace, all_path_counts, all_visit_orders
  
  def accumulate_stress_centrality(self, all_path_counts, all_visit_orders, pred_or_trace, lazy=False):
    stress = dict.fromkeys(self.Nodes, 0)
    for node in self.Nodes:
      stress[node] += len(all_visit_orders[node])
      delta = dict.fromkeys(self.Nodes, 0)
      for v in all_visit_orders[node][::-1]:
        if lazy and pred_or_trace[node][v]:
          delta[pred_or_trace[node][v]['StopId']] += 1 + delta[v]
        elif not lazy:
          for u in pred_or_trace[node][v]:
            delta[u] += 1 + delta[v]
        if v != node:
          stress[v] += all_path_counts[node][v]*delta[v] + 1
    return stress
  
  def floyd_warshall(self):
    dists = {u: dict.fromkeys(self.Nodes) for u in self.Nodes}
    from_edges = {u: dict.fromkeys(self.Nodes) for u in self.Nodes}
    
    for u in self.Nodes:
      dists[u][u] = 0
      for v, edge in self.Nodes[u].edges:
        if dists[u][v] is None or dists[u][v] > edge['time']:
          dists[u][v] = edge['time']
          from_edges[u][v] = {
            'StopId': u,
            **edge
          }

    for k in self.Nodes:
      for u in self.Nodes:
        for v in self.Nodes:
          if dists[u][k] is None or dists[k][v] is None:
            continue
          if dists[u][v] is None or dists[u][k] + dists[k][v] < dists[u][v]:
            dists[u][v] = dists[u][k] + dists[k][v]
            from_edges[u][v] = from_edges[k][v]

    return dists, from_edges

  def shortest_path(self, source, target, dists=None, from_edge=None):
    if dists is None or from_edge is None:
      dists, from_edge = self.dijkstra(source)
    
    dists = dists[source]
    from_edge = from_edge[source]
    
    if dists[target] is None:
      return []
    
    path = [{'StopId': target}]
    current = from_edge[target]
    while current is not None:
      path = [current] + path
      current = from_edge[current['StopId']]

    return path

  def stress_centrality(self, dists=None, from_edge=None):
    if dists is None or from_edge is None:
      dists, from_edge = self.dijkstra_all()
    
    centrality = dict.fromkeys(self.Nodes, 0)

    for u in self.Nodes:
      for v in self.Nodes:
        path = self.shortest_path(u, v, dists, from_edge)
        for node in path:
          centrality[node['StopId']] += 1
    
    return centrality
