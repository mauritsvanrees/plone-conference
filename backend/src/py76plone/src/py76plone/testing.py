from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing.zope import WSGI_SERVER_FIXTURE

import py76plone


class PY76PLONELayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=py76plone)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "py76plone:default")
        applyProfile(portal, "py76plone:initial")


PY76PLONE_FIXTURE = PY76PLONELayer()


PY76PLONE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PY76PLONE_FIXTURE,),
    name="PY76PLONELayer:IntegrationTesting",
)


PY76PLONE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PY76PLONE_FIXTURE, WSGI_SERVER_FIXTURE),
    name="PY76PLONELayer:FunctionalTesting",
)


PY76PLONEACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        PY76PLONE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        WSGI_SERVER_FIXTURE,
    ),
    name="PY76PLONELayer:AcceptanceTesting",
)
