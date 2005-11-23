#
# Test copying/pasting of controller objects
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
from Products.CMFPlone.tests import PloneTestCase
from Products.CMFFormController.tests import transaction
from Products.CMFFormController.FormAction import FormAction
from Products.CMFFormController.FormValidator import FormValidator

class TestCopyRename(PloneTestCase.PloneTestCase):

    def testRename(self):
        formcontroller = self.portal.portal_form_controller
        self.folder.manage_addProduct['CMFFormController'].manage_addControllerPageTemplate('test', 'Test', '<html>test</html>')

        pt = self.folder.test
        pt.actions.set(FormAction(pt.getId(), 'success', None, None, 'traverse_to', 'test3', self.portal.portal_form_controller))
        self.assertEqual(len(pt.actions.getFiltered(object_id='test')), 1)
        self.assertEqual(pt.actions.match('test', 'success', 'Document', 'submit').getActionArg(), 'test3')

        pt.validators.set(FormValidator(pt.getId(), None, None, 'a,b,c', self.portal.portal_form_controller))
        self.assertEqual(len(pt.validators.getFiltered(object_id='test')), 1)
        self.assertEqual(pt.validators.match('test', 'Document', 'submit').getValidators(), ['a','b','c'])
        
        formcontroller.actions.set(FormAction(pt.getId(), 'success', None, None, 'traverse_to', 'test4', self.portal.portal_form_controller))
        self.assertEqual(len(formcontroller.actions.getFiltered(object_id='test')), 1)
        self.assertEqual(formcontroller.actions.match('test', 'success', 'Document', 'submit').getActionArg(), 'test4')

        formcontroller.validators.set(FormValidator(pt.getId(), None, None, 'd,e,f', self.portal.portal_form_controller))
        self.assertEqual(len(formcontroller.validators.getFiltered(object_id='test')), 1)
        self.assertEqual(formcontroller.validators.match('test', 'Document', 'submit').getValidators(), ['d','e','f'])

        transaction.savepoint(optimistic=True)

        self.loginPortalOwner()
        self.folder.manage_renameObjects(['test'], ['test2'])
        pt2 = self.folder.test2
        self.assertEqual(len(pt2.actions.getFiltered(object_id='test')), 0)
        self.assertEqual(len(pt2.actions.getFiltered(object_id='test2')), 1)
        self.assertEqual(formcontroller.actions.match('test2', 'success', 'Document', 'submit').getActionArg(), 'test4')
        self.assertEqual(formcontroller.actions.match('test', 'success', 'Document', 'submit').getActionArg(), 'test4')

        self.assertEqual(len(pt2.validators.getFiltered(object_id='test')), 0)
        self.assertEqual(len(pt2.validators.getFiltered(object_id='test2')), 1)
        self.assertEqual(formcontroller.validators.match('test2', 'Document', 'submit').getValidators(), ['d','e','f'])
        self.assertEqual(formcontroller.validators.match('test', 'Document', 'submit').getValidators(), ['d','e','f'])

        formcontroller._purge()
        self.assertEqual(formcontroller.validators.match('test2', 'Document', 'submit').getValidators(), ['d','e','f'])
        self.assertEqual(formcontroller.validators.match('test', 'Document', 'submit'), None)

    def testCopy(self):
        formcontroller = self.portal.portal_form_controller
        self.folder.manage_addProduct['CMFFormController'].manage_addControllerPageTemplate('test', 'Test', '<html>test</html>')

        pt = self.folder.test
        pt.actions.set(FormAction(pt.getId(), 'success', None, None, 'traverse_to', 'test3', self.portal.portal_form_controller))
        self.assertEqual(len(pt.actions.getFiltered()), 1)
        self.assertEqual(pt.actions.match('test', 'success', 'Document', 'submit').getActionArg(), 'test3')

        pt.validators.set(FormValidator(pt.getId(), None, None, 'a,b,c', self.portal.portal_form_controller))
        self.assertEqual(len(pt.validators.getFiltered(object_id='test')), 1)
        self.assertEqual(pt.validators.match('test', 'Document', 'submit').getValidators(), ['a','b','c'])
        
        formcontroller.actions.set(FormAction(pt.getId(), 'success', None, None, 'traverse_to', 'test4', self.portal.portal_form_controller))
        self.assertEqual(len(pt.actions.getFiltered()), 1)
        self.assertEqual(formcontroller.actions.match('test', 'success', 'Document', 'submit').getActionArg(), 'test4')

        formcontroller.validators.set(FormValidator(pt.getId(), None, None, 'd,e,f', self.portal.portal_form_controller))
        self.assertEqual(len(formcontroller.validators.getFiltered(object_id='test')), 1)
        self.assertEqual(formcontroller.validators.match('test', 'Document', 'submit').getValidators(), ['d','e','f'])

        transaction.savepoint(optimistic=True)

        self.loginPortalOwner()
        cb = self.folder.manage_copyObjects(['test'])
        self.folder.manage_pasteObjects(cb)
        pt2 = self.folder.copy_of_test
        self.assertEqual(len(pt2.actions.getFiltered(object_id='test')), 0)
        self.assertEqual(len(pt2.actions.getFiltered(object_id='copy_of_test')), 1)
        self.assertEqual(formcontroller.actions.match('copy_of_test', 'success', 'Document', 'submit').getActionArg(), 'test4')
        self.assertEqual(formcontroller.actions.match('test', 'success', 'Document', 'submit').getActionArg(), 'test4')

        self.assertEqual(len(pt2.validators.getFiltered(object_id='test')), 0)
        self.assertEqual(len(pt2.validators.getFiltered(object_id='copy_of_test')), 1)
        self.assertEqual(formcontroller.validators.match('copy_of_test', 'Document', 'submit').getValidators(), ['d','e','f'])
        self.assertEqual(formcontroller.validators.match('test', 'Document', 'submit').getValidators(), ['d','e','f'])

        formcontroller._purge()
        self.assertEqual(formcontroller.actions.match('test', 'success', 'Document', 'submit').getActionArg(), 'test4')
        self.assertEqual(formcontroller.actions.match('copy_of_test', 'success', 'Document', 'submit').getActionArg(), 'test4')
        self.assertEqual(formcontroller.validators.match('copy_of_test', 'Document', 'submit').getValidators(), ['d','e','f'])
        self.assertEqual(formcontroller.validators.match('test', 'Document', 'submit').getValidators(), ['d','e','f'])

        
#        self.assertEqual(temp_doc.meta_type, 'Document')

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCopyRename))
    return suite

if __name__ == '__main__':
    framework()
