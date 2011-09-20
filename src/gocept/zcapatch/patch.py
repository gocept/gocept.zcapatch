# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import zope.component


class PatchManager(object):

    def __init__(self, registry=None):
        self.utilities = []
        self.adapters = []
        if registry is None:
            registry = zope.component.getSiteManager()
        self.registry = registry

    def patch_utility(self, interface, new, name=None, registry=None):
        if registry is None:
            registry = self.registry
        orig = registry.queryUtility(interface)
        if orig is not None:
            self.utilities.append((registry, orig, interface, name))
        if name is None:
            registry.registerUtility(new, interface)
        else:
            registry.registerUtility(new, interface, name)
        return new

    def patch_adapter(self, factory, required=None, provided=None,
                      name=u'', registry=None):
        if registry is None:
            registry = self.registry
        orig = registry.adapters.lookup(required, provided, name)
        if orig is not None:
            self.adapters.append((registry, orig, required, provided, name))
        registry.registerAdapter(factory, required, provided, name)
        return factory

    def patch_handler(self, args):
        pass

    def reset(self):
        self._reset_utilities()
        self._reset_adapters()

    def _reset_utilities(self):
        for registry, orig, interface, name in self.utilities:
            if name is None:
                registry.registerUtility(orig, interface)
            else:
                registry.registerUtility(orig, interface, name)

    def _reset_adapters(self):
        for registry, orig, required, provided, name in self.adapters:
            registry.registerAdapter(orig, required, provided, name)
