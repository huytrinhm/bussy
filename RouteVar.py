from Stop import Stop
from Path import Path

class RouteVar():
  def __init__(
    self, RouteId, RouteVarId, RouteVarName, RouteVarShortName,
    RouteNo, StartStop, EndStop, Distance, Outbound, RunningTime,
    Stops=None, Path=None
  ):
    self.RouteId = RouteId
    self.RouteVarId = RouteVarId
    self.RouteVarName = RouteVarName
    self.RouteVarShortName = RouteVarShortName
    self.RouteNo = RouteNo
    self.StartStop = StartStop
    self.EndStop = EndStop
    self.Distance = Distance
    self.Outbound = Outbound
    self.RunningTime = RunningTime
    self.Stops = Stops
    self.Path = Path

  def __repr__(self):
    s = ''
    s += 'RouteVar(\n'
    s += f'  RouteId={self.RouteId!r}\n'
    s += f'  RouteVarId={self.RouteVarId!r}\n'
    s += f'  RouteVarName={self.RouteVarName!r}\n'
    s += f'  RouteVarShortName={self.RouteVarShortName!r}\n'
    s += f'  RouteNo={self.RouteNo!r}\n'
    s += f'  StartStop={self.StartStop!r}\n'
    s += f'  EndStop={self.EndStop!r}\n'
    s += f'  Distance={self.Distance!r}\n'
    s += f'  Outbound={self.Outbound!r}\n'
    s += f'  RunningTime={self.RunningTime!r}\n'
    if self.Stops is None:
      s += f'  Stops=None\n'
    else:
      s += f'  Stops=[{len(self.Stops)} Stop(s)]\n'
    if self.Path is None:
      s += f'  Path=None\n'
    else:
      s += f'  Path={self.Path}\n'
    
    s += ')'

    return s
  
  def to_dict(self):
    return {
      k[1:]: v
      for k, v in self.__dict__.items()
      if k not in ['_Stops', '_Path']
    }

  @property
  def RouteId(self):
    return self._RouteId
  @RouteId.setter
  def RouteId(self, value):
    self._RouteId = value

  @property
  def RouteVarId(self):
    return self._RouteVarId
  @RouteVarId.setter
  def RouteVarId(self, value):
    self._RouteVarId = value

  @property
  def RouteVarName(self):
    return self._RouteVarName
  @RouteVarName.setter
  def RouteVarName(self, value):
    self._RouteVarName = value

  @property
  def RouteVarShortName(self):
    return self._RouteVarShortName
  @RouteVarShortName.setter
  def RouteVarShortName(self, value):
    self._RouteVarShortName = value

  @property
  def RouteNo(self):
    return self._RouteNo
  @RouteNo.setter
  def RouteNo(self, value):
    self._RouteNo = value

  @property
  def StartStop(self):
    return self._StartStop
  @StartStop.setter
  def StartStop(self, value):
    self._StartStop = value

  @property
  def EndStop(self):
    return self._EndStop
  @EndStop.setter
  def EndStop(self, value):
    self._EndStop = value

  @property
  def Distance(self):
    return self._Distance
  @Distance.setter
  def Distance(self, value):
    self._Distance = value

  @property
  def Outbound(self):
    return self._Outbound
  @Outbound.setter
  def Outbound(self, value):
    self._Outbound = value

  @property
  def RunningTime(self):
    return self._RunningTime
  @RunningTime.setter
  def RunningTime(self, value):
    self._RunningTime = value

  @property
  def Stops(self):
    return self._Stops
  @Stops.setter
  def Stops(self, stops):
    self._Stops = stops
    
  @property
  def Path(self):
    return self._Path
  @Path.setter
  def Path(self, path):
    self._Path = path
