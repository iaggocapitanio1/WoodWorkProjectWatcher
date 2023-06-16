from payload.core.core import BasePayload
from enum import Enum


class ConsumablePayload(BasePayload):
    RELATIONAL_PROPS = ['belongsTo']

    class Status(Enum):
        WAITING_ORDER = 0
        PREPARING = 1
        AVAILABLE = 2
        CAUGHT = 3

    def __init__(self, **kwargs):
        super(ConsumablePayload, self).__init__(**kwargs)
        self.name = kwargs.get('name', '')
        self.amount = kwargs.get('amount', -1)
        self.status = kwargs.get('status', 0)
        self.belongsTo = kwargs.get('belongsTo', '')
        self.image = kwargs.get('image', '')

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def amount(self) -> float:
        return self._amount

    @amount.setter
    def amount(self, amount: float) -> None:
        self._amount = amount

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, status: str) -> None:
        self._status = status

    @property
    def belongsTo(self) -> str:
        return self._belongsTo

    @belongsTo.setter
    def belongsTo(self, belongsTo: str) -> None:
        self._belongsTo = belongsTo

    @property
    def image(self) -> str:
        return self._image

    @image.setter
    def image(self, image: str) -> None:
        self._image = image
