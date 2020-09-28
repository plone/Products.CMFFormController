# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.zope import Browser
from plone.protect import createToken

import transaction
import unittest

import Products.CMFFormController


class CMFFormControllerLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=Products.CMFFormController)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'Products.CMFFormController:CMFFormController')


CMFFORMCONTROLLER_FIXTURE = CMFFormControllerLayer()


CMFFORMCONTROLLER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CMFFORMCONTROLLER_FIXTURE,),
    name='CMFFormControllerLayer:FunctionalTesting'
)


class TestRedirectToFunctional(unittest.TestCase):

    layer = CMFFORMCONTROLLER_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.portal_workflow.setChainForPortalTypes(
            ('Document',),
            ('simple_publication_workflow',))
        # Create two pages.
        self.portal.invokeFactory(
            id='page',
            title='Page 1',
            type_name='Document'
        )
        self.portal.invokeFactory(
            id='front-page',
            title='Frontpage',
            type_name='Document'
        )
        self.page = self.portal.page
        transaction.commit()
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization', 'Basic {0}:{1}'.format(
                TEST_USER_NAME, TEST_USER_PASSWORD))

    def tearDown(self):
        # still have to delete the created pages manually
        # because of test isolation problems
        del self.portal['page']
        del self.portal['front-page']
        transaction.commit()
        super(TestRedirectToFunctional, self).tearDown()

    def test_regression(self):
        csrf_token = createToken()
        target = 'front-page'
        path = '/'.join(self.page.getPhysicalPath())
        data = 'workflow_action=publish&paths=%s&orig_template=%s&_authenticator=%s'  # noqa: E501
        data = data % (path, target, csrf_token)
        self.browser.post(self.portal_url + '/folder_publish', data)
        # redirect to frontpage http://attacker.com
        self.assertEqual(
            self.browser.url, self.portal.absolute_url() + '/front-page')

    def test_attacker_redirect(self):
        csrf_token = createToken()
        target = 'http://attacker.com'
        path = '/'.join(self.page.getPhysicalPath())
        data = 'workflow_action=publish&paths=%s&orig_template=%s&_authenticator=%s'  # noqa: E501
        data = data % (path, target, csrf_token)
        self.browser.post(self.portal_url + '/folder_publish', data)
        # no redirect to http://attacker.com, instead to the portal
        self.assertEqual(self.browser.url, self.portal.absolute_url())

        # The same without the testbrowser
        self.assertIsNone(self.request.response.headers.get('location'))
        self.request.environ["REQUEST_METHOD"] = "POST"
        self.request.REQUEST_METHOD = 'POST'
        self.request.form['workflow_action'] = 'publish'
        self.request.form['paths'] = path
        self.request.form['orig_template'] = target
        self.request.form['_authenticator'] = csrf_token
        view = self.portal.restrictedTraverse('folder_publish')
        view()
        # no redirect to http://attacker.com, instead to the portal
        self.assertEqual(
            self.request.response.headers.get('location'),
            self.portal.absolute_url())
