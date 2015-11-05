# -*- coding: utf-8 -*-
from plone.app.testing import TEST_USER_ID
from zope.component import queryUtility
from zope.component import createObject
from plone.app.testing import setRoles
from plone.dexterity.interfaces import IDexterityFTI
from plone import api

from uwosh.oshkoshscholars.testing import UWOSH_OSHKOSHSCHOLARS_INTEGRATION_TESTING  # noqa
from uwosh.oshkoshscholars.interfaces import IStudentSubmission

import unittest2 as unittest


class StudentSubmissionIntegrationTest(unittest.TestCase):

    layer = UWOSH_OSHKOSHSCHOLARS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='StudentSubmission')
        schema = fti.lookupSchema()
        self.assertEqual(IStudentSubmission, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='StudentSubmission')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='StudentSubmission')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IStudentSubmission.providedBy(obj))

    def test_adding(self):
        self.portal.invokeFactory('StudentSubmission', 'StudentSubmission')
        self.assertTrue(
            IStudentSubmission.providedBy(self.portal['StudentSubmission'])
        )
