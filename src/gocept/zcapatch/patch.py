# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import zope.component


class PatchManager(object):

    def __init__(self, registry=None):
        self.utilities = []
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

    def patch_adpater(self, args):
        pass

    def patch_handler(self, args):
        pass

    def reset(self):
        for registry, orig, interface, name in self.utilities:
            if name is None:
                registry.registerUtility(orig, interface)
            else:
                registry.registerUtility(orig, interface, name)
