import logging
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.utils import getToolByName
from plone.app.textfield.interfaces import ITransformer
from plone import api
from plone.namedfile.file import NamedBlobFile

log = logging.getLogger('uwosh.oshkoshscholars')


def on_submit_email_advisors(context, event):
    """Email faculty advisors when student submits for review
    """
    if context.portal_type != 'StudentSubmission':
        return
    if event.transition is None or event.transition.id != 'submit':
        return

    mail_host = getToolByName(context, 'MailHost')
    portal_url = getToolByName(context, 'portal_url')

    portal = portal_url.getPortalObject()
    sender = portal.getProperty('email_from_address')

    if not sender:
        log.error('unable to email advisors because the site has no email_from_address set')
        return

    # notify advisors 
    subject = "[Oshkosh Scholar] student submission advisor"
    message = """
A student (%s, %s) has indicated that you are an advisor for their submission \"%s\" to the Oshkosh Scholar publication (%s). 

You can view the submission by clicking on %s and logging in using your NetID. 

If you have any questions or concerns, please reply to this message.
""" % (context.student_name, context.student_email, context.title, portal.absolute_url(), context.absolute_url(),)

    emails = [context.faculty_email, context.faculty_email2]
    for email in emails:
        email = email.strip()
        if email != '' and email is not None:
            mail_host.secureSend(message, email, sender, subject)

    # notify managing editor
    subject = "[Oshkosh Scholar] student submission was submitted for review"
    message = """
%s (%s) has submitted \"%s\" for review

%s 

You can view the submission by clicking on %s and logging in using your NetID. 

""" % (context.student_name, context.student_email, context.title, portal.absolute_url(), context.absolute_url(),)

    emails = [context.email_from_address]
    for email in emails:
        email = email.strip()
        if email != '' and email is not None:
            mail_host.secureSend(message, email, sender, subject)


def event_submission_added(submission, event):
    """Do various things when a submission is added
    """
    if submission.portal_type != 'StudentSubmission':
        return

    # set description / summary
    transformer = ITransformer(submission)
    abstract_text = transformer(submission.abstract, 'text/plain')
    if len(abstract_text) > 497:
        abstract_text = abstract_text[:497]+'...'
    submission.setDescription(abstract_text)

    # set faculty advisor IDs
    pm = getToolByName(submission, 'portal_membership')
    email1 = submission.faculty_email
    if email1 and email1.strip() != '':
        results = pm.searchMembers('email', email1)
        if len(results) > 0:
            faculty_id1 = results[0]['username']
            submission.faculty_id = faculty_id1
    email2 = submission.faculty_email2
    if email2 and email2.strip() != '':
        results2 = pm.searchMembers('email', email2)
        if len(results2) > 0:
            faculty_id2 = results2[0]['username']
            submission.faculty_id2 = faculty_id2

    # grant Reader role to faculty advisors
    faculty_id = submission.faculty_id
    faculty_id2 = submission.faculty_id2
    if faculty_id:
        submission.manage_setLocalRoles(faculty_id, ['Reader',])
    if faculty_id2:
        submission.manage_setLocalRoles(faculty_id2, ['Reader',])

    # grant Reader role to other students listed
    for email in [submission.student_email2,
                  submission.student_email3,
                  submission.student_email4,
                  submission.student_email5]:
        if email and email.strip() != '':
            results = pm.searchMembers('email', email)
            if len(results) > 0:
                userid = results[0]['username']
                submission.manage_setLocalRoles(userid, ['Reader',])

    # copy the submitted file into the submission folder
    file = submission.submission_file
    contained_file_obj = api.content.create(
        submission, 'File',
        id='submitted-file',
        title=file.filename,
        safe_id=True
    )
    contained_file_obj.setFile(file.data, filename=file.filename)

    submission.reindexObject()


def send_email(context, emails, subject, message):
    mail_host = getToolByName(context, 'MailHost')
    portal_url = getToolByName(context, 'portal_url')
    portal = portal_url.getPortalObject()
    sender = portal.getProperty('email_from_address')
    if not sender:
        log.error('unable to send email because the site has no email_from_address set')
        return
    for email in emails:
        email = email.strip()
        if email != '' and email is not None:
            mail_host.secureSend(message, email, sender, subject)


def on_assign_to_reviewer(submission, event):
    """Assign local role for reviewer and notify reviewer by email"""
    if submission.portal_type != 'StudentSubmission':
        return
    if event.transition is None or event.transition.id != 'assign-to-reviewer':
        return
    context = submission
    reviewer_id = submission.reviewer
    deadline = submission.review_deadline
    # grant roles to reviewer
    if reviewer_id:
        context.manage_setLocalRoles(reviewer_id, ['Reader', 'Reviewer',])
    else:
        raise ValueError("You must specify a reviewer before using this transition")
    if not deadline:
        raise ValueError("You must specify a review deadline before using this transition")
    portal_url = getToolByName(context, 'portal_url')
    portal = portal_url.getPortalObject()
    subject = "[Oshkosh Scholar] student submission for your review"
    message = """
A submission \"%s\" requires your review

%s 

You can view the submission by clicking on %s and logging in using your NetID. 

""" % (context.title, portal.absolute_url(), context.absolute_url(),)

    pm = getToolByName(context,'portal_membership')
    reviewer = pm.getMemberById(reviewer_id)
    email_address = reviewer.getProperty('email')
    send_email(context, [email_address,], subject, message)


def on_remove_identifying_info(submission, event):
    """Remove local role for reviewer, and notify managing editor by email"""
    if submission.portal_type != 'StudentSubmission':
        return
    if event.transition is None or event.transition.id != 'remove-reviewer-info':
        return
    context = submission
    reviewer_id = submission.reviewer
    # revoke roles to reviewer
    if reviewer_id != '':
        context.manage_delLocalRoles([reviewer_id])
    portal_url = getToolByName(context, 'portal_url')
    portal = portal_url.getPortalObject()
    subject = "[Oshkosh Scholar] student submission requires removal of identifying info"
    message = """
A submission \"%s\" requires that you remove identifying info:

%s 

You can view the submission by clicking on %s and logging in using your NetID. 

""" % (context.title, portal.absolute_url(), context.absolute_url(),)

    pm = getToolByName(context,'portal_membership')
    email_address = context.email_from_address
    send_email(context, [email_address,], subject, message)


def on_send_back(submission, event):
    """Remove local role for reviewer, and notify submitter by email"""
    if submission.portal_type != 'StudentSubmission':
        return
    if event.transition is None or event.transition.id != 'send-back-to-student':
        return
    context = submission
    reviewer_id = submission.reviewer
    # revoke roles to reviewer
    if reviewer_id != '':
        context.manage_delLocalRoles([reviewer_id])
    portal_url = getToolByName(context, 'portal_url')
    portal = portal_url.getPortalObject()
    subject = "[Oshkosh Scholar] student submission has been sent back"
    message = """
A submission \"%s\" has been sent back to the submitter:

%s 

You can view the submission by clicking on %s and logging in using your NetID. 

""" % (context.title, portal.absolute_url(), context.absolute_url(),)

    pm = getToolByName(context,'portal_membership')
    import pdb;pdb.set_trace()
    owner = pm.getMemberById(context.Owner)
    email_address = owner.getProperty('email')
    send_email(context, [email_address,], subject, message)
