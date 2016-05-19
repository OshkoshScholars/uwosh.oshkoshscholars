from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from plone import api

class StudentView(BrowserView):
    pass


class AddSubmissionHomeFolder(BrowserView):

     def __init__(self, context, request):
          self.context = context
          self.request = request

     def __call__(self):
         pm = getToolByName(self, 'portal_membership')
         home_url = pm.getHomeUrl()
         if home_url:
             self.request.response.redirect(home_url + '/++add++StudentSubmission')
         else:
             portal_url = api.portal.get().absolute_url()
             add_submission_url = portal_url + '/add_submission_in_home_folder'
             self.request.response.redirect(portal_url + '/login_form?came_from=%s' % add_submission_url)
