from DataManager import load_data, dump_csv
from RouteVarQuery import RouteVarQuery
from StopQuery import StopQuery
from PathQuery import PathQuery
from GraphBuilder import buildGraph
import json
from time import perf_counter

def top_k_centrality(centrality, all_stops, k=10):
  sorted_centrality = sorted(centrality.items(), key=lambda item: item[1], reverse=True)
  results = [{'PathCount': n, 'Stop': all_stops[stop_id].to_dict()} for stop_id, n in sorted_centrality[:k]]
  return results

def main():
  route_vars, all_stops = load_data(
    'data/vars.json',
    'data/stops.json',
    'data/paths.json'
  )
  
  route_var_query = RouteVarQuery(list(route_vars.values()))
  (
    route_var_query
    .searchByAttribute('Outbound', True)
    .searchByCustomFilter(lambda var: var.RunningTime < 40)
  ).toJSON('output1.json')

  stop_query = StopQuery(list(all_stops.values()))
  (
    stop_query
    .searchByAttribute('Zone', 'Quận 1')
  ).toCSV('output2.csv')

  path_query = PathQuery([route_var.Path for route_var in route_vars.values()])
  (
    path_query
    .searchByAttribute('RouteId', '1')
  ).toCSV('output3.csv')

  print('Begin build graph')
  t = perf_counter()
  graph = buildGraph(route_vars, all_stops)
  print(f'Build graph completed in {perf_counter() - t} seconds')

  print('Begin dijkstra')
  t = perf_counter()
  dists, trace, path_counts, visit_orders = graph.dijkstra_all_with_trace(with_preds=False)
  print(f'Dijkstra completed in {perf_counter() - t} seconds')
  dump_csv([['u', 'v', 'time'], *[[u, v, dists[u][v]] for u in dists for v in dists[u]]], 'dists.csv')

  path = graph.shortest_path(1, 50, dists, trace)
  json.dump(path, open('path_from_1_to_50.json', 'w'))
  
  print('Begin centrality calculation')
  t = perf_counter()
  centrality = graph.accumulate_stress_centrality(path_counts, visit_orders, trace, lazy=True)
  print(f'Centrality calculation completed in {perf_counter() - t} seconds')
  top_10 = top_k_centrality(centrality, all_stops, 10)
  json.dump(top_10, open('top_10_important_stops.json', 'w'))


if __name__ == '__main__':
  main()
