import logging
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.utils import getToolByName


log = logging.getLogger('uwosh.oshkoshscholars')


def on_submit_email_advisors(context, event):
    """Email faculty advisors when student submits for review
    """
    if context.portal_type != 'StudentSubmission':
        return
    if event.transition.id != 'submit':
        return

    mail_host = getToolByName(context, 'MailHost')
    portal_url = getToolByName(context, 'portal_url')

    portal = portal_url.getPortalObject()
    sender = portal.getProperty('email_from_address')

    if not sender:
        log.error('unable to email advisors because the site has no email_from_address set')
        return

    subject = "[Oshkosh Scholar] student submission advisor"
    message = "A student (%s, %s) has indicated that you are an advisor for their submission \"%s\" to the Oshkosh Scholar publication (%s). \n\nYou can view the submission by clicking on %s and logging in using your NetID" % (context.student_name, context.student_email, context.title, portal.absolute_url(), context.absolute_url(),)

    emails = [context.faculty_email, context.faculty_email2]
    for email in emails:
        email = email.strip()
        if email != '' and email is not None:
            mail_host.secureSend(message, email, sender, subject)


def event_submission_added(submission, event):
    """Do various things when a submission is added
    """
    if submission.portal_type != 'StudentSubmission':
        return

    # set faculty advisor IDs
    
    pm = getToolByName(submission, 'portal_membership')
    email1 = submission.faculty_email
    if email1.strip() != '':
        results = pm.searchMembers('email', email1)
        if len(results) > 0:
            faculty_id1 = results[0]['username']
            submission.faculty_id = faculty_id1
        
    email2 = submission.faculty_email2
    if email2.strip() != '':
        results2 = pm.searchMembers('email', email2)
        if len(results2) > 0:
            faculty_id2 = results2[0]['username']
            submission.faculty_id2 = faculty_id2

    # grant Reader role to faculty advisors
    if faculty_id1 != '':
        submission.manage_setLocalRoles(faculty_id1, ['Reader',])
    if faculty_id2 != '':
        submission.manage_setLocalRoles(faculty_id2, ['Reader',])

    # force reindex
    submission.reindexObject()

