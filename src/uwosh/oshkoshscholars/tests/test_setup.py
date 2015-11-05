# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from uwosh.oshkoshscholars.testing import UWOSH_OSHKOSHSCHOLARS_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that uwosh.oshkoshscholars is properly installed."""

    layer = UWOSH_OSHKOSHSCHOLARS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if uwosh.oshkoshscholars is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'uwosh.oshkoshscholars'))

    def test_browserlayer(self):
        """Test that IOshkoshScholarsLayer is registered."""
        from uwosh.oshkoshscholars.interfaces import (
            IOshkoshScholarsLayer)
        from plone.browserlayer import utils
        self.assertIn(IOshkoshScholarsLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = UWOSH_OSHKOSHSCHOLARS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['uwosh.oshkoshscholars'])

    def test_product_uninstalled(self):
        """Test if uwosh.oshkoshscholars is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'uwosh.oshkoshscholars'))
