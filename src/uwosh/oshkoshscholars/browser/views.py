from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName


class StudentView(BrowserView):
    pass


class AddSubmissionHomeFolder(BrowserView):

     def __init__(self, context, request):
          self.context = context
          self.request = request

     def __call__(self):
         pm = getToolByName(self, 'portal_membership')
         home_url = pm.getHomeUrl()
         self.request.response.redirect(home_url + '/++add++StudentSubmission')
