"""Setup tests for this package."""
from kitconcept import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFPlone.utils import get_installer
from py76plone.testing import PY76PLONE_INTEGRATION_TESTING  # noqa: E501

import unittest


class TestSetup(unittest.TestCase):
    """Test that py76plone is properly installed."""

    layer = PY76PLONE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.setup = self.portal.portal_setup
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if py76plone is installed."""
        self.assertTrue(self.installer.is_product_installed("py76plone"))

    def test_browserlayer(self):
        """Test that IPY76PLONELayer is registered."""
        from plone.browserlayer import utils
        from py76plone.interfaces import IPY76PLONELayer

        self.assertIn(IPY76PLONELayer, utils.registered_layers())

    def test_latest_version(self):
        """Test latest version of default profile."""
        self.assertEqual(
            self.setup.getLastVersionForProfile("py76plone:default")[0],
            "20221010001",
        )


class TestUninstall(unittest.TestCase):

    layer = PY76PLONE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("py76plone")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if py76plone is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("py76plone"))

    def test_browserlayer_removed(self):
        """Test that IPY76PLONELayer is removed."""
        from plone.browserlayer import utils
        from py76plone.interfaces import IPY76PLONELayer

        self.assertNotIn(IPY76PLONELayer, utils.registered_layers())
