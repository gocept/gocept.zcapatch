# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

from zope.interface import Interface
import gocept.zcapatch
import unittest
import zope.component.registry


class PatchManagerTest(unittest.TestCase):

    def test_replaced_utility_is_restored_after_reset(self):
        registry = zope.component.registry.Components()
        registry.registerUtility('foo', Interface)
        self.assertEqual('foo', registry.getUtility(Interface))
        man = gocept.zcapatch.PatchManager(registry)
        man.patch_utility(Interface, 'bar')
        self.assertEqual('bar', registry.getUtility(Interface))
        man.reset()
        self.assertEqual('foo', registry.getUtility(Interface))
