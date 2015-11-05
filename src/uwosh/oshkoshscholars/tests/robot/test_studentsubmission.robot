# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s uwosh.oshkoshscholars -t test_studentsubmission.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src uwosh.oshkoshscholars.testing.UWOSH_OSHKOSHSCHOLARS_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_studentsubmission.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a StudentSubmission
  Given a logged-in site administrator
    and an add studentsubmission form
   When I type 'My StudentSubmission' into the title field
    and I submit the form
   Then a studentsubmission with the title 'My StudentSubmission' has been created

Scenario: As a site administrator I can view a StudentSubmission
  Given a logged-in site administrator
    and a studentsubmission 'My StudentSubmission'
   When I go to the studentsubmission view
   Then I can see the studentsubmission title 'My StudentSubmission'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add studentsubmission form
  Go To  ${PLONE_URL}/++add++StudentSubmission

a studentsubmission 'My StudentSubmission'
  Create content  type=StudentSubmission  id=my-studentsubmission  title=My StudentSubmission


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I submit the form
  Click Button  Save

I go to the studentsubmission view
  Go To  ${PLONE_URL}/my-studentsubmission
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a studentsubmission with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the studentsubmission title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
