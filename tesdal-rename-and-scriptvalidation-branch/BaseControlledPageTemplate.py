# ###########################################################################

import Globals
from AccessControl import ClassSecurityInfo
from ZPublisher.Publish import missing_name, dont_publish_class
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.CMFCore.CMFCorePermissions import ManagePortal, View
from Products.CMFCore.utils import getToolByName
from ControlledBase import ControlledBase
from ControllerState import ControllerState
from FormValidator import FormValidatorKey, FormValidator
from FormAction import FormActionKey, FormAction
from globalVars import ANY_CONTEXT, ANY_BUTTON

import sys
from urllib import quote


class BaseControlledPageTemplate(ControlledBase):

    security = ClassSecurityInfo()
    security.declareObjectProtected(View)
    
    def _call(self, inherited_call, *args, **kwargs):
        # Intercept a call to a form and see if REQUEST.form contains the
        # value form.submitted.  If so, perform validation.  If not, update
        # the controller state and treat as a normal form.

        REQUEST = self.REQUEST

        controller = getToolByName(self, 'portal_form_controller')
        controller_state = controller.getState(self, is_validator=0)

        form_submitted = REQUEST.form.get('form.submitted', None)        
        if form_submitted:
            controller_state = self.getButton(controller_state, REQUEST)
            validators = self.getValidators(controller_state, REQUEST).getValidators()
            controller_state = controller.validate(controller_state, REQUEST, validators)
            del REQUEST.form['form.submitted']
            return self.getNext(controller_state, REQUEST)

        kwargs['state'] = controller_state
        return inherited_call(self, *args, **kwargs)


    def getButton(self, controller_state, REQUEST):
        for k in REQUEST.form.keys():
            if k.startswith('form.button.'):
                controller_state.setButton(k[len('form.button.'):])
                return controller_state
        return controller_state


Globals.InitializeClass(BaseControlledPageTemplate)