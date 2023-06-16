from payload.core.core import BasePayload
from enum import Enum


# noinspection PyPep8Naming
class AssemblyPayload(BasePayload):
    RELATIONAL_PROPS = ['belongsTo']

    class Status(Enum):
        WAITING = 0
        ASSEMBLING = 1
        TESTING = 2
        PACKED = 3

    def __init__(self, **kwargs):
        super(AssemblyPayload, self).__init__(**kwargs)
        self.type = kwargs.get('type', 'Part')
        self.startTime = kwargs.get('startTime', '')
        self.endTime = kwargs.get('endTime', '')
        self.statusAssembly = kwargs.get('statusAssembly', 0)
        self.belongsTo = kwargs.get("belongsTo", "")

    @property
    def belongsTo(self) -> str:
        return self._belongsTo

    @belongsTo.setter
    def belongsTo(self, belongsTo: str) -> None:
        self._belongsTo = belongsTo

    @property
    def startTime(self) -> str:
        return self._startTime

    @startTime.setter
    def startTime(self, startTime: str) -> None:
        self._startTime = startTime

    @property
    def endTime(self) -> str:
        return self._endTime

    @endTime.setter
    def endTime(self, endTime: str) -> None:
        self._endTime = endTime

    @property
    def statusAssembly(self) -> int:
        return self._statusAssembly

    @statusAssembly.setter
    def statusAssembly(self, statusAssembly: int) -> None:
        self._statusAssembly = statusAssembly
