#
# Test the RedirectTo action.
#

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing.bbb import PloneTestCase
from plone.protect import createToken

import transaction


class TestRedirectToFunctional(PloneTestCase):
    # Functional tests, using the folder_publish.cpy script from
    # Products.CMFPlone, which could be persuaded to redirect to an external
    # website, which is not what it is meant for.

    def afterSetUp(self):
        # Update settings.
        # self.app = self.layer['app']
        # self.portal = self.layer['portal']
        # self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.portal_workflow.setChainForPortalTypes(
            ('Document',),
            ('simple_publication_workflow',))
        # Create page.
        self.portal.invokeFactory(
            id='page',
            title='Page 1',
            type_name='Document'
        )
        self.page = self.portal.page

    def beforeTearDown(self):
        # Weird that we have to remove this page manually.  Otherwise with the
        # second test we get an error:
        # BadRequest: The id "page" is invalid - it is already in use.
        # Strangely this does not happen when you run
        # bin/test -s Products.CMFFormController -m testRedirectTo
        # which is the only test case that uses portal.page,
        # and it does happen when you run all the tests:
        # bin/test -s Products.CMFFormController
        # We may want to switch to the real plone.app.testing
        # instead of bbb.PloneTestCase.
        self.portal._delObject('page')
        transaction.commit()

    def test_regression(self):
        csrf_token = createToken()
        env = {'HTTP_X_CSRF_TOKEN': csrf_token}
        target = 'front-page'
        url = (
            '%s/folder_publish'
            '?workflow_action=publish'
            '&paths=%s'
            '&orig_template=%s') % (
                '/'.join(self.portal.getPhysicalPath()),
                '/'.join(self.page.getPhysicalPath()),
                target
        )
        response = self.publish(
            url,
            basic='%s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD),
            env=env,
            extra={'orig_template': target,
                   '_authenticator': csrf_token},
            request_method='POST',
            handle_errors=False,
        )
        self.assertNotEqual(response.headers.get('location'), None)
        self.assertEqual(response.headers.get('location'),
                         self.portal.absolute_url() + '/front-page')

    def test_attacker_redirect(self):
        csrf_token = createToken()
        env = {'HTTP_X_CSRF_TOKEN': csrf_token}
        target = 'http://attacker.com'
        url = (
            '%s/folder_publish'
            '?workflow_action=publish'
            '&paths=%s'
            '&orig_template=%s') % (
                '/'.join(self.portal.getPhysicalPath()),
                '/'.join(self.page.getPhysicalPath()),
                target
        )
        response = self.publish(
            url,
            basic='%s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD),
            env=env,
            extra={'orig_template': target,
                   '_authenticator': csrf_token},
            request_method='POST',
            handle_errors=False,
        )
        self.assertNotEqual(response.headers.get('location'), None)
        self.assertNotEqual(response.headers.get('location'),
                            'http://attacker.com')
