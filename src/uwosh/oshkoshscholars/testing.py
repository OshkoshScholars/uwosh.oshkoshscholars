# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import uwosh.oshkoshscholars


class OshkoshScholarsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=uwosh.oshkoshscholars)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'uwosh.oshkoshscholars:default')


UWOSH_OSHKOSHSCHOLARS_FIXTURE = OshkoshScholarsLayer()


UWOSH_OSHKOSHSCHOLARS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(UWOSH_OSHKOSHSCHOLARS_FIXTURE,),
    name='OshkoshScholarsLayer:IntegrationTesting'
)


UWOSH_OSHKOSHSCHOLARS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(UWOSH_OSHKOSHSCHOLARS_FIXTURE,),
    name='OshkoshScholarsLayer:FunctionalTesting'
)


UWOSH_OSHKOSHSCHOLARS_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        UWOSH_OSHKOSHSCHOLARS_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='OshkoshScholarsLayer:AcceptanceTesting'
)
