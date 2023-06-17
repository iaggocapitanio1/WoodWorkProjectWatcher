from typing import List, Dict, Any
import requests
import inspect
import json
import settings
from client import oauth
import functools


class BasePayload(object):
    PROPS_TO_EXCLUDE: List[str] = ['context', 'headers', 'url', 'id', 'type', 'link_headers']
    GEO_PROPERTY: List[str] = []
    RELATIONAL_PROPS: List[str] = []
    RESOURCE = 'part/'

    def __init__(self, **kwargs) -> None:
        self.session = requests.Session()
        self.session.headers = kwargs.get('headers', settings.HEADERS)
        self.session.auth = oauth
        self.url = kwargs.get('url', settings.URL + self.RESOURCE)
        self.type = kwargs.get('type', 'Part')
        self.id = kwargs.get('id', None)

    @staticmethod
    def validate_props(props: list) -> List:
        return props

    @functools.cache
    def get_props_to_exclude(self):
        return self.validate_props(props=self.PROPS_TO_EXCLUDE)

    @functools.cache
    def get_relational_props(self):
        return self.validate_props(props=self.RELATIONAL_PROPS)

    @functools.cache
    def get_geo_props(self):
        return self.validate_props(props=self.GEO_PROPERTY)

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, identifier) -> None:
        self._id = identifier

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, _type) -> None:
        self._type = _type

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, url: str) -> None:
        self._url = url

    @functools.cache
    def get_all_properties(self) -> List[str]:
        return [prop[0] for prop in inspect.getmembers(self.__class__, lambda inst: isinstance(inst, property))]

    @functools.cache
    def clean_properties(self) -> List[str]:
        return [prop for prop in self.get_all_properties() if prop not in self.get_props_to_exclude() +
                self.get_relational_props() + self.get_geo_props()]

    @staticmethod
    def create_field(_type: str, value: Any, relationship=False) -> Dict[str, Any]:
        return dict(type=_type, object=value) if relationship else dict(type=_type, value=value)

    def body(self) -> dict:
        payload_body = dict(id=self.id, type=self.type)
        for prop in self.clean_properties():
            payload_body[prop] = self.create_field(_type='Property', value=getattr(self, prop))
        for prop in self.get_relational_props():
            payload_body[prop] = self.create_field(_type='Relationship', value=getattr(self, prop), relationship=True)
        for prop in self.get_geo_props():
            payload_body[prop] = self.create_field(_type='GeoProperty', value=getattr(self, prop))
        return payload_body

    def partial_body(self) -> dict:
        partial_body = dict()
        response: requests.Response = self.get(dict(options='keyValues'))
        if response.status_code != 200:
            raise Exception(f"Error while getting entity: {response.status_code}, {response.text}")
        actual = self.get().json()
        for prop in self.clean_properties():
            value = getattr(self, prop)
            actual_value = actual.get(prop, None)
            if actual_value is not None and not value == actual_value:
                partial_body[prop] = self.create_field(_type='Property', value=value)
        return partial_body

    def json(self):
        return json.dumps(self.body())

    def partial_json(self):
        return json.dumps(self.partial_body())

    def post(self):
        return self.session.post(self.url, self.json())

    def url_with_pk(self):
        if self.url.endswith('/'):
            return self.url + f"{self.id}/"
        return self.url + f"/{self.id}/"

    def get(self, params=None):
        if not params:
            params = {}
        return self.session.get(self.url_with_pk(), params=params)

    def patch(self, params=None):
        return self.session.patch(self.url_with_pk(), self.partial_json(),  params=params)

    def delete(self):
        return self.session.delete(self.url_with_pk())

    def list(self, params=None):
        return self.session.get(self.url, params=params)
