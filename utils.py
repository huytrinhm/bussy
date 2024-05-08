import pyproj
from contextlib import redirect_stdout, redirect_stderr, contextmanager, ExitStack
import os

@contextmanager
def suppress(out=True, err=True):
  with ExitStack() as stack:
    with open(os.devnull, "w") as null:
      if out:
        stack.enter_context(redirect_stdout(null))
      if err:
        stack.enter_context(redirect_stderr(null))
      yield

crs_wgs84 = pyproj.CRS('WGS84')
crs_3405 = pyproj.CRS('epsg:3405')
transformer = pyproj.Transformer.from_crs(crs_wgs84, crs_3405)

def ll2xy(latitude, longitude):
  x, y = transformer.transform(latitude, longitude)
  return x, y

def get_uuid(object):
  if isinstance(object, dict):
    if 'RouteId' not in object or 'RouteVarId' not in object:
      raise Exception('Invalid object')
    route_id = object['RouteId']
    route_var_id = object['RouteVarId']
  else:
    if not hasattr(object, 'RouteId') or not hasattr(object, 'RouteVarId'):
      raise Exception('Invalid object')
    route_id = object.RouteId
    route_var_id = object.RouteVarId

  return f"{route_id}_{route_var_id}"
