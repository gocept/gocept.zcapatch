===============
gocept.zcapatch
===============

This packages allows you to replace, add or delete `zope.component`_
registrations of utilities, adapters and event handlers, and to later on undo
the changes you made.

.. _`zope.component`: http://pypi.python.org/pypi/zope.component

.. contents:: :depth: 1

Usage
=====

To change something in a registry, instantiate ``gocept.zcapatch.Patches`` for
that registry (if no registry is given, the current one as returned by
``zope.component.getSiteManager()`` is used). It offers the following methods:

:patch_utility(new, provided=None, name=u'', registry=None):
    Register the given ``new`` object as a utility, instead of what is
    currently registered for this interface (and name).

    If no ``provided`` interface is given, it is read from the object's
    ``zope.interface.implements`` declaration.

    If you want to delete a utility registration, pass ``new=None``.

:patch_adapter(factory, required=None, provided=None, name=u'', registry=None):
    Register the given ``factory`` as an adapter, instead of what is
    currently registered for these required and provided interfaces (and name).

    Any of the ``required`` or ``provided`` interfaces not given will be read
    from the object's ``zope.component.adapts`` and
    ``zope.interface.implements`` declarations.

    If you want to delete an adapter registration, pass
    ``factory=lambda *args: None``.

:patch_handler(handler, required, registry=None):
    Register the given ``handler`` instead of what is
    currently registered for the required interfaces.

    If no ``required`` interfaces are given, they are read from the object's
    ``zope.component.adapts`` declaration.

    If you want to delete a handler registration, use **remove_handler**.

:remove_handler(handler, required=None, registry=None):
    Delete the specified registration of ``handler``.
    (Since handlers are set-valued, you cannot delete one without explicitly
    specifying which one you mean.)

    If no ``required`` interfaces are given, they are read from the object's
    ``zope.component.adapts`` declaration.

:reset:
    Undo all changes made via this ``Patches`` instance:
    Unregister all utilities, adapters and handlers added, and restore
    any previously present registrations that were replaced or removed.


Here's a typical usage example::

    import gocept.zcapatch
    import unittest


    class TestCase(unittest.TestCase):

        def setUp(self):
            self.zca = gocept.zcapatch.Patches()

        def tearDown(self):
            self.zca.reset()

        def test_something(self):
            self.zca.patch_utility(...)


Development
===========

The source code is available in the mercurial repository at
https://code.gocept.com/hg/public/gocept.zcapatch

Please report any bugs you find at
https://projects.gocept.com/projects/projects/gocept-zcapatch/issues
