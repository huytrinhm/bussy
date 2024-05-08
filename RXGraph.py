def shortest_path(graph, paths, source, target, id_to_indice, indice_to_id):
  source_idx, target_idx = id_to_indice[source], id_to_indice[target]
  if source_idx not in paths or target_idx not in paths[source_idx]:
    return []
  
  path = []
  for u, v in zip(paths[source_idx][target_idx][:-1], paths[source_idx][target_idx][1:]):
    path.append({
      'StopId': indice_to_id[u],
      **min(graph.get_all_edge_data(u, v), key=lambda edge: edge['time'])
    })

  path.append({'StopId': target})

  return path