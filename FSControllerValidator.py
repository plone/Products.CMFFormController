##############################################################################
#
# Copyright (c) 2001 Zope Corporation and Contributors. All Rights Reserved.
# 
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
# 
##############################################################################
""" Customizable controlled python scripts that come from the filesystem.

$Id: FSControllerValidator.py,v 1.2 2003/09/27 18:28:41 plonista Exp $
"""

import copy
import Globals, Acquisition
from AccessControl import ClassSecurityInfo
from OFS.Cache import Cacheable
from Products.PageTemplates.ZopePageTemplate import Src
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.CMFCore.DirectoryView import registerFileExtension, registerMetaType
from Products.CMFCore.CMFCorePermissions import View, ManagePortal
from Products.CMFCore.FSPythonScript import FSPythonScript as BaseClass
from ControllerValidator import ControllerValidator
from ControllerState import ControllerState
from ControllerBase import ControllerBase
from utils import logException

class FSControllerValidator (BaseClass, ControllerBase):
    """FSControllerValidators act like Controller Python Scripts but are not 
    directly modifiable from the management interface."""

    meta_type = 'Filesystem Controller Validator'

    manage_options=(
           (
            {'label':'Customize', 'action':'manage_main'},
            {'label':'Test', 'action':'ZScriptHTML_tryForm'},
           ) + Cacheable.manage_options)
#            {'label':'Actions','action':'manage_formActionsForm'},             


    # Use declarative security
    security = ClassSecurityInfo()
    security.declareObjectProtected(View)

    def __init__(self, id, filepath, fullname=None, properties=None):
        BaseClass.__init__(self, id, filepath, fullname, properties)
        self.filepath = filepath
        self._read_action_metadata(self.getId(), filepath)


    def __call__(self, *args, **kwargs):
        result = FSControllerValidator.inheritedAttribute('__call__')(self, *args, **kwargs)
#        if getattr(result, '__class__', None) == ControllerState and not result._isValidating():
#            return self.getNext(result, self.REQUEST)
        return result


    security.declarePrivate('manage_afterAdd')
    def manage_afterAdd(self, object, container):
        try:
            BaseClass.manage_afterAdd(self, object, container)
            # Re-read .metadata after adding so that we can do validation checks
            # using information in portal_form_controller.  Since manage_afterAdd
            # is not guaranteed to run, we also call these in __init__
#            self._read_action_metadata(self.getId(), self.filepath)
        except:
            logException()
            raise


    def _createZODBClone(self):
        """Create a ZODB (editable) equivalent of this object."""
        obj = ControllerValidator(self.getId())
        obj.write(self.read())
#        obj.actions = copy.copy(self.actions)
        return obj


    security.declarePublic('writableDefaults')
    def writableDefaults(self):
        """Can default actions and validators be modified?"""
        return 0

Globals.InitializeClass(FSControllerValidator)

registerFileExtension('vpy', FSControllerValidator)
registerMetaType('Controller Validator', FSControllerValidator)
