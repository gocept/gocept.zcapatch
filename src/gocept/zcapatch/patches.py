# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import zope.component
import zope.component.registry


class Patches(object):

    def __init__(self, registry=None):
        self.utilities = []
        self.adapters = []
        self.added_handlers = []
        self.removed_handlers = []
        if registry is None:
            registry = zope.component.getSiteManager()
        self.registry = registry

    def patch_utility(self, new, provided=None, name=u'', registry=None):
        if registry is None:
            registry = self.registry
        if provided is None:
            provided = zope.component.registry._getUtilityProvided(new)
        orig = registry.queryUtility(provided, name)
        if orig is not None:
            self.utilities.append((registry, orig, provided, name))
        registry.registerUtility(new, provided, name)
        return new

    def patch_adapter(self, factory, required=None, provided=None,
                      name=u'', registry=None):
        if registry is None:
            registry = self.registry
        if required is None:
            required = zope.component.registry._getAdapterRequired(
                factory, required)
        if provided is None:
            provided = zope.component.registry._getAdapterProvided(factory)
        orig = registry.adapters.lookup(required, provided, name)
        if orig is not None:
            self.adapters.append((registry, orig, required, provided, name))
        registry.registerAdapter(factory, required, provided, name)
        return factory

    def patch_handler(self, handler, required, registry=None):
        if registry is None:
            registry = self.registry
        self.added_handlers.append((registry, handler, required))
        registry.registerHandler(handler, required)

    def remove_handler(self, handler, required, registry=None):
        if registry is None:
            registry = self.registry
        if registry.unregisterHandler(handler, required):
            self.removed_handlers.append((registry, handler, required))

    def reset(self):
        self._reset_utilities()
        self._reset_adapters()
        self._reset_handlers()

    def _reset_utilities(self):
        for registry, orig, interface, name in self.utilities:
            registry.registerUtility(orig, interface, name)

    def _reset_adapters(self):
        for registry, orig, required, provided, name in self.adapters:
            registry.registerAdapter(orig, required, provided, name)

    def _reset_handlers(self):
        self._remove_added_handlers()
        self._restore_removed_handlers()

    def _remove_added_handlers(self):
        for registry, handler, required in self.added_handlers:
            registry.unregisterHandler(handler, required)

    def _restore_removed_handlers(self):
        for registry, handler, required in self.removed_handlers:
            registry.registerHandler(handler, required)
