import timeit
from DataManager import load_data
from GraphBuilder import buildGraph, buildRXGraph

def main():
  route_vars, all_stops = load_data(
    'data/vars.json',
    'data/stops.json',
    'data/paths.json'
  )

  benchmark_globals = {
    'buildGraph': buildGraph,
    'buildRXGraph': buildRXGraph,
    'route_vars': route_vars,
    'all_stops': all_stops
  }

  print("---buildGraph---")
  buildGraph_number = 10
  time = timeit.timeit(
    stmt='buildGraph(route_vars, all_stops)',
    globals=benchmark_globals,
    number=buildGraph_number
  ) / buildGraph_number
  print(time)

  print("---dijkstra---")
  dijkstra_number = 5
  time = timeit.timeit(
    stmt='for s in all_stops: graph.dijkstra(s)',
    setup='graph = buildGraph(route_vars, all_stops)',
    globals=benchmark_globals,
    number=dijkstra_number
  ) / dijkstra_number / len(all_stops)
  print(time)

  print("---dijkstra_all---")
  dijkstra_all_number = 5
  time = timeit.timeit(
    stmt='graph.dijkstra_all()',
    setup='graph = buildGraph(route_vars, all_stops)',
    globals=benchmark_globals,
    number=dijkstra_all_number
  ) / dijkstra_all_number
  print(time)

  print("---stress_centrality---")
  stress_centrality_number = 3
  time = timeit.timeit(
    stmt='graph.stress_centrality(dists, trace)',
    setup='graph = buildGraph(route_vars, all_stops); dists, trace = graph.dijkstra_all()',
    globals=benchmark_globals,
    number=stress_centrality_number
  ) / stress_centrality_number
  print(time)

  print("---dijkstra_all_with_stress_centrality---")
  dijkstra_all_with_stress_centrality_number = 5
  time = timeit.timeit(
    stmt='graph.dijkstra_all_with_stress_centrality()',
    setup='graph = buildGraph(route_vars, all_stops)',
    globals=benchmark_globals,
    number=dijkstra_all_with_stress_centrality_number
  ) / dijkstra_all_with_stress_centrality_number
  print(time)

  print("---dijkstra_all_with_trace (with pred)---")
  dijkstra_all_with_trace_pred_number = 5
  time = timeit.timeit(
    stmt='graph.dijkstra_all_with_trace(with_preds=True)',
    setup='graph = buildGraph(route_vars, all_stops)',
    globals=benchmark_globals,
    number=dijkstra_all_with_trace_pred_number
  ) / dijkstra_all_with_trace_pred_number
  print(time)

  print("---dijkstra_all_with_trace (no pred)---")
  dijkstra_all_with_trace_number = 5
  time = timeit.timeit(
    stmt='graph.dijkstra_all_with_trace(with_preds=False)',
    setup='graph = buildGraph(route_vars, all_stops)',
    globals=benchmark_globals,
    number=dijkstra_all_with_trace_number
  ) / dijkstra_all_with_trace_number
  print(time)

  print("---accumulate_stress_centrality---")
  accumulate_stress_centrality_number = 10
  time = timeit.timeit(
    stmt='graph.accumulate_stress_centrality(path_counts, visit_orders, preds, lazy=False)',
    setup='graph = buildGraph(route_vars, all_stops); _, _, path_counts, visit_orders, preds = graph.dijkstra_all_with_trace(with_preds=True)',
    globals=benchmark_globals,
    number=accumulate_stress_centrality_number
  ) / accumulate_stress_centrality_number
  print(time)

  print("---accumulate_stress_centrality (lazy)---")
  accumulate_stress_centrality_lazy_number = 10
  time = timeit.timeit(
    stmt='graph.accumulate_stress_centrality(path_counts, visit_orders, trace, lazy=True)',
    setup='graph = buildGraph(route_vars, all_stops); _, trace, path_counts, visit_orders = graph.dijkstra_all_with_trace(with_preds=False)',
    globals=benchmark_globals,
    number=accumulate_stress_centrality_lazy_number
  ) / accumulate_stress_centrality_lazy_number
  print(time)

  # print("---rustworkx dijkstra---")
  # rustworkx_number = 1
  # time = timeit.timeit(
  #   stmt="rx.all_pairs_dijkstra_shortest_paths(graph, lambda edge: edge)",
  #   setup='import rustworkx as rx; graph, _ = buildRXGraph(route_vars, all_stops)',
  #   globals=benchmark_globals,
  #   number=rustworkx_number
  # )
  # print(time)

if __name__ == '__main__':
  main()