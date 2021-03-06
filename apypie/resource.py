from __future__ import print_function, absolute_import

from apypie.action import Action


class Resource:
    """
    Apipie Resource
    """

    def __init__(self, api, name):
        self.api = api
        self.name = name

    @property
    def actions(self):
        return sorted([method['name'] for method in self.api.apidoc['docs']['resources'][self.name]['methods']])

    def action(self, name):
        if self.has_action(name):
            return Action(name, self.name, self.api)
        else:
            raise IOError

    def has_action(self, name):
        return name in self.actions

    def call(self, action, params={}, headers={}, options={}):
        self.api.call(self.name, action, params, headers, options)
