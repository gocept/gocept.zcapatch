# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

from zope.interface import Interface
import gocept.zcapatch
import mock
import unittest
import zope.component.globalregistry
import zope.component.registry


class PatchesTest(unittest.TestCase):

    def test_replaced_utility_is_restored_after_reset(self):
        registry = zope.component.registry.Components()
        registry.registerUtility('foo', Interface)
        self.assertEqual('foo', registry.getUtility(Interface))
        man = gocept.zcapatch.Patches(registry)
        man.patch_utility('bar', Interface)
        self.assertEqual('bar', registry.getUtility(Interface))
        man.reset()
        self.assertEqual('foo', registry.getUtility(Interface))

    def test_utility_with_name_is_restored_after_reset(self):
        registry = zope.component.registry.Components()
        registry.registerUtility('foo', Interface, name='foo')
        self.assertEqual('foo', registry.getUtility(Interface, 'foo'))
        man = gocept.zcapatch.Patches(registry)
        man.patch_utility('bar', Interface, name='foo')
        self.assertEqual('bar', registry.getUtility(Interface, 'foo'))
        man.reset()
        self.assertEqual('foo', registry.getUtility(Interface, 'foo'))

    def test_replaced_adapter_is_restored_after_reset(self):
        registry = zope.component.registry.Components()
        registry.registerAdapter(lambda x: 'foo', (Interface,), Interface)
        self.assertEqual('foo', registry.getAdapter(object(), Interface))
        man = gocept.zcapatch.Patches(registry)
        man.patch_adapter(lambda x: 'bar', (Interface,), Interface)
        self.assertEqual('bar', registry.getAdapter(object(), Interface))
        man.reset()
        self.assertEqual('foo', registry.getAdapter(object(), Interface))

    def test_if_no_interface_given_is_read_from_utility(self):
        class IFoo(Interface):
            pass

        class Util(object):
            zope.interface.implements(IFoo)

        registry = zope.component.registry.Components()
        self.assertIsNone(registry.queryUtility(IFoo))
        man = gocept.zcapatch.Patches(registry)
        man.patch_utility(Util())
        self.assertIsNotNone(registry.queryUtility(IFoo))

    def test_if_no_interface_adapts_given_is_read_from_adapter(self):
        class IFoo(Interface):
            pass

        class IBar(Interface):
            pass

        class Adapter(object):
            zope.component.adapts(IFoo)
            zope.interface.implements(IBar)

            def __init__(self, context):
                pass

        foo = type('Dummy', (object,), {})()
        zope.interface.alsoProvides(foo, IFoo)

        registry = zope.component.registry.Components()
        self.assertIsNone(registry.queryAdapter(foo, IBar))
        man = gocept.zcapatch.Patches(registry)
        man.patch_adapter(Adapter)
        self.assertIsNotNone(registry.queryAdapter(foo, IBar))

    def test_if_no_adapts_given_is_read_from_handler(self):
        class IFoo(Interface):
            pass

        @zope.component.adapter(IFoo)
        def handler(context):
            self.called = True

        foo = type('Dummy', (object,), {})()
        zope.interface.alsoProvides(foo, IFoo)

        self.called = False

        registry = zope.component.registry.Components()
        registry.handle(foo)
        self.assertFalse(self.called)
        man = gocept.zcapatch.Patches(registry)
        man.patch_handler(handler)
        registry.handle(foo)
        self.assertTrue(self.called)

    def test_added_handler_is_removed_after_reset(self):
        registry = zope.component.registry.Components()
        handler = mock.Mock()
        registry.handle(object())
        self.assertFalse(handler.called)

        man = gocept.zcapatch.Patches(registry)
        man.patch_handler(handler, (Interface,))
        registry.handle(object())
        self.assertTrue(handler.called)
        handler.reset_mock()

        man.reset()
        registry.handle(object())
        self.assertFalse(handler.called)

    def test_removed_handler_is_restored_after_reset(self):
        registry = zope.component.registry.Components()
        handler = mock.Mock()
        registry.registerHandler(handler, (Interface,))
        registry.handle(object())
        self.assertTrue(handler.called)
        handler.reset_mock()

        man = gocept.zcapatch.Patches(registry)
        man.remove_handler(handler, (Interface,))
        registry.handle(object())
        self.assertFalse(handler.called)
        handler.reset_mock()

        man.reset()
        registry.handle(object())
        self.assertTrue(handler.called)

    def test_remove_not_registeredhandler_should_noop_and_not_restore(self):
        registry = zope.component.registry.Components()
        handler = mock.Mock()

        man = gocept.zcapatch.Patches(registry)
        man.remove_handler(handler, (Interface,))
        registry.handle(object())
        self.assertFalse(handler.called)

        man.reset()
        registry.handle(object())
        self.assertFalse(handler.called)


class GlobalRegistryTest(unittest.TestCase):

    def setUp(self):
        # don't want to pull in zope.testing just for this,
        # so we duplicate the effect of zope.component.testing.setUp/tearDown
        zope.component.globalregistry.base.__init__('base')

    def tearDown(self):
        self.setUp()

    def test_no_registry_given_uses_getSiteManager(self):
        man = gocept.zcapatch.Patches()
        gsm = zope.component.getSiteManager()
        gsm.registerUtility('foo', Interface)
        self.assertEqual('foo', gsm.getUtility(Interface))
        man.patch_utility('bar', Interface)
        self.assertEqual('bar', gsm.getUtility(Interface))
        man.reset()
        self.assertEqual('foo', gsm.getUtility(Interface))
