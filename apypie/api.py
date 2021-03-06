from __future__ import print_function, absolute_import

import json
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin
import requests

from apypie.resource import Resource


class Api:
    """
    Apipie API bindings
    """

    def __init__(self, apifile):
        with open(apifile, 'r') as f:
            self.apidoc = json.load(f)

    @property
    def resources(self):
        return sorted(self.apidoc['docs']['resources'].keys())

    def resource(self, name):
        if name in self.resources:
            return Resource(self, name)
        else:
            raise IOError

    def call(self, resource_name, action_name, params={}, headers={}, options={}):
        resource = Resource(self, resource_name)
        action = resource.action(action_name)
        if not options.get('skip_validation', False):
            action.validate(params)

        return self.call_action(action, params, headers, options)

    def call_action(self, action, params={}, headers={}, options={}):
        route = action.find_route(params)
        get_params = dict((key, value) for key, value in params.items() if key not in route.params_in_path)
        return self.http_call(
            route.method,
            route.path_with_params(params),
            get_params,
            headers, options)

    def http_call(self, http_method, path, params=None, headers=None, options=None):
        full_path = urljoin('https://example.com', path)
        kwargs = {'headers': headers or {}}
        if http_method == 'get':
            kwargs['params'] = params or {}
        else:
            kwargs['data'] = params or {}
        request = requests.request(http_method, full_path, **kwargs)
        request.raise_for_status()
        return request.json()
