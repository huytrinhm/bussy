from Graph import Graph
from shapely.geometry import Point, LineString
from utils import ll2xy, suppress
import rustworkx as rx
from typing import Tuple, Dict

def cut(line, distance):
  if distance <= 0.0 or distance >= 1.0:
    return LineString(line)
  coords = list(line.coords)
  for i, p in enumerate(coords):
    pd = line.project(Point(p), normalized=True)
    if pd == distance:
      return LineString(coords[i:])
    if pd > distance:
      cp = line.interpolate(distance, normalized=True)
      return LineString([(cp.x, cp.y)] + coords[i:])

def buildRouteVar(route_var, all_stops, indices_map=None):
  if indices_map is None:
    indices_map = lambda u: u
  total_time = route_var.RunningTime
  length = route_var.Distance

  path = [ll2xy(lat, lng) for lng, lat in zip(route_var.Path.lng, route_var.Path.lat)]
  path = LineString(path)
  origninal_length = path.length

  stop_points = [
    Point(ll2xy(
      all_stops[stop_id].Lat,
      all_stops[stop_id].Lng
    ))
    for stop_id in route_var.Stops
  ]

  edges = []
  for i, (u, v, u_point, v_point) in enumerate(zip(
    route_var.Stops[:-1], route_var.Stops[1:],
    stop_points[:-1], stop_points[1:]
  )):
    u_dist = path.project(u_point, normalized=True)
    v_dist = path.project(v_point, normalized=True)
    dist = (v_dist - u_dist) * path.length / origninal_length
    if i + 1 < len(stop_points) - 1:
      path = cut(path, v_dist)
    assert dist > 0, (route_var.RouteId, route_var.RouteVarId, u, v)

    edges.append((indices_map(u), indices_map(v), {
      'RouteId': route_var.RouteId,
      'RouteVarId': route_var.RouteVarId,
      'dist': length * dist,
      'time':  total_time * dist
    }))

    # edges.append((indices_map(u), indices_map(v), total_time * dist))

  return edges

def buildGraph(route_vars, all_stops) -> Graph:
  graph = Graph()
  graph.updateNodes([(k, v) for k, v in all_stops.items()])
  
  with suppress():
    edges = []
    for route_var in route_vars.values():
      edges.extend(buildRouteVar(route_var, all_stops))

  graph.updateEdges(edges)

  return graph

# def buildNetworkXGraph(route_vars, all_stops) -> nx.MultiDiGraph:
#   graph = nx.MultiDiGraph()
#   graph.add_nodes_from([(k, {'Stop': v}) for k, v in all_stops.items()])

#   edges = []
#   for route_var in route_vars.values():
#     edges.extend(buildRouteVar(route_var, all_stops))

#   graph.add_edges_from(edges)

#   return graph

def buildRXGraph(route_vars, all_stops) -> Tuple[rx.PyDiGraph, Dict[int, int]]:
  graph = rx.PyDiGraph()
  node_indices = graph.add_nodes_from(list(all_stops))
  node_indices = {k: i for k, i in zip(all_stops, node_indices)}

  with suppress():
    edges = []
    for route_var in route_vars.values():
      edges.extend(buildRouteVar(route_var, all_stops, lambda u: node_indices[u]))

  graph.add_edges_from(edges)

  return graph, node_indices