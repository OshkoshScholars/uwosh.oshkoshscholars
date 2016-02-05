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

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='StudentSubmission')
        self.assertTrue(fti)

    # States to check:
    # "accepted-for-publication"
    #     <exit-transition transition_id="retract"/>
    #     <exit-transition transition_id="copyedit-for-published"/>
    #     <exit-transition transition_id="member-withdraws-submission"/>
    # "being-reviewed"
    #     <exit-transition transition_id="deny"/>
    #     <exit-transition transition_id="reject"/>
    #     <exit-transition transition_id="retract"/>
    #     <exit-transition transition_id="remove-reviewer-info"/>
    #     <exit-transition transition_id="member-withdraws-submission"/>
    # "being-revised-by-student"
    #     <exit-transition transition_id="reject"/>
    #     <exit-transition transition_id="remove-identifying-info"/>
    #     <exit-transition transition_id="retract"/>
    #     <exit-transition transition_id="member-withdraws-submission"/>
    # "copyediting-for-honorable-mention"
    #     <exit-transition transition_id="retract"/>
    #     <exit-transition transition_id="finish-copyediting-for-honorable-mention"/>
    #     <exit-transition transition_id="member-withdraws-submission"/>
    # "copyediting-for-honorable-mention-finished"
    #     <exit-transition transition_id="publish-honorable-mention"/>
    #     <exit-transition transition_id="retract"/>
    #     <exit-transition transition_id="member-withdraws-submission"/>
    # "copyediting-for-publication-finished"
    #     <exit-transition transition_id="retract"/>
    #     <exit-transition transition_id="member-withdraws-submission"/>
    #     <exit-transition transition_id="publish"/>
    # "copyediting-for-published"
    #     <exit-transition transition_id="finish-copyediting-for-published"/>
    #     <exit-transition transition_id="retract"/>
    #     <exit-transition transition_id="member-withdraws-submission"/>
    # "denied"
    # "honorable-mention"
    #     <exit-transition transition_id="reject"/>
    #     <exit-transition transition_id="retract"/>
    #     <exit-transition transition_id="deny"/>
    #     <exit-transition transition_id="copyedit-for-honorable-mention"/>
    #     <exit-transition transition_id="member-withdraws-submission"/>
    # "honorable-mention-published"
    #     <exit-transition transition_id="reject"/>
    #     <exit-transition transition_id="retract"/>
    #     <exit-transition transition_id="deny"/>
    #     <exit-transition transition_id="member-withdraws-submission"/>
    # "identifying-info-removal"
    #     <exit-transition transition_id="retract"/>
    #     <exit-transition transition_id="send-to-selection-committee"/>
    #     <exit-transition transition_id="member-withdraws-submission"/>
    # "pending"
    #     <exit-transition transition_id="reject"/>
    #     <exit-transition transition_id="retract"/>
    #     <exit-transition transition_id="assign-to-reviewer"/>
    #     <exit-transition transition_id="deny"/>
    #     <exit-transition transition_id="member-withdraws-submission"/>
    # "private"
    #     <exit-transition transition_id="submit"/>
    # "public"
    # "published"
    #     <exit-transition transition_id="reject"/>
    #     <exit-transition transition_id="retract"/>
    #     <exit-transition transition_id="deny"/>
    #     <exit-transition transition_id="member-withdraws-submission"/>
    # "removing-id-info"
    #     <exit-transition transition_id="send-back-to-student"/>
    #     <exit-transition transition_id="retract"/>
    #     <exit-transition transition_id="member-withdraws-submission"/>
    # "revision"
    # "selection-committee"
    #     <exit-transition transition_id="accept-for-publication"/>
    #     <exit-transition transition_id="reject"/>
    #     <exit-transition transition_id="deny"/>
    #     <exit-transition transition_id="include-as-honorable-mention"/>
    #     <exit-transition transition_id="member-withdraws-submission"/>
    # "withdrawn"
    #     <exit-transition transition_id="reject"/>
    # 
    # Transitions to check:
    # "accept-for-publication" new_state="accepted-for-publication" 
    # "assign-to-reviewer" new_state="being-reviewed" 
    # "copyedit-for-honorable-mention" new_state="copyediting-for-honorable-mention" 
    # "copyedit-for-published" new_state="copyediting-for-published" 
    # "deny" new_state="denied" 
    # "finish-copyediting-for-honorable-mention" new_state="copyediting-for-honorable-mention-finished" 
    # "finish-copyediting-for-published" new_state="copyediting-for-publication-finished" 
    # "include-as-honorable-mention" new_state="honorable-mention" 
    # "member-withdraws-submission" new_state="withdrawn" 
    # "publish" new_state="published" 
    # "publish-honorable-mention" new_state="honorable-mention-published" 
    # "reject" new_state="private" 
    # "remove-identifying-info" new_state="identifying-info-removal" 
    # "remove-reviewer-info" new_state="removing-id-info" 
    # "retract" new_state="private" 
    # "send-back-to-student" new_state="being-revised-by-student" 
    # "send-to-selection-committee" new_state="selection-committee" 
    # "submit" new_state="pending" 
    def test_adding(self):
        portal = self.portal

        # create new submission object
        portal.invokeFactory('StudentSubmission', 'StudentSubmission')
        self.assertTrue('StudentSubmission' in [i for i, j in self.portal.items() ])
        submission = self.portal['StudentSubmission']

        # check initial state
        state = api.content.get_state(obj=submission)
        self.assertTrue(state=='private')

        # check creator
        self.assertTrue(submission.Creator()=='test_user_1_')
        test_user = api.user.get_current()
        self.assertTrue(test_user.id=='test_user_1_')

        # create new user jane
        jane = api.user.create(email='jane@plone.org', username='jane')
        jane_roles = api.user.get_roles(username='jane')
        self.assertTrue(jane_roles == ['Member', 'Authenticated'])

        # check that jane cannot see the submission
        jane_perms = api.user.get_permissions(username='jane', obj=submission)
        jane_perms_true = [p for p in jane_perms if jane_perms[p]]
        self.assertTrue('View' not in jane_perms_true)

        # grant Manager role to jane
        api.user.grant_roles(username='jane', roles=['Manager',])
        new_jane_roles = api.user.get_roles(username='jane')
        self.assertTrue(new_jane_roles == ['Member', 'Manager', 'Authenticated'])

        # check that jane can now see the submission
        new_jane_perms =api.user.get_permissions(username='jane', obj=submission)
        new_jane_perms_true = [p for p in new_jane_perms if new_jane_perms[p]]
        self.assertTrue('View' in new_jane_perms)

#        import pdb;pdb.set_trace()
