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
##########################################################################

import os
from AccessControl import ClassSecurityInfo
import Globals
from Products.CMFCore.FSMetadata import FSMetadata
from ControllerBase import ControllerBase

class FSControllerBase(ControllerBase):
    """Common functions for filesystem objects controlled by portal_form_controller"""

    security = ClassSecurityInfo()


    def _setProperties(self, properties=None):
        if properties:
            # Since props come from the filesystem, this should be
            # safe.
            self.__dict__.update(properties)
            if fullname and properties.get('keep_extension', 0):
                id = fullname

            cache = properties.get('cache')
            if cache:
                self.ZCacheable_setManagerId(cache)


    # Refresh our contents from the filesystem if that is newer and we are
    # running in debug mode.
    def _updateFromFS(self):
        parsed = self._parsed
        if not parsed or Globals.DevelopmentMode:
            fp = expandpath(self._filepath)
            try:
                mtime=stat(fp)[8]
            except:
                mtime=0
            e_fp = fp + '.metadata'
            try:
                mmtime = stat(e_fp)[8]
            except:
                mmtime = 0
            if mmtime > mtime:
                mtime = mmtime
            if not parsed or mtime != self._file_mod_time:
                # if we have to read the file again, remove the cache
                self.ZCacheable_invalidate()
                self._readFile(1)
                self._file_mod_time = mtime
                self._parsed = 1


    def _readFile(self, reparse):
        BaseClass._readfile(self, reparse)

        # re-read .metadata file if it exists
        e_fp = expandpath(self._filepath) + '.metadata'
        if os.path.exists(e_fp):
            metadata = FSMetadata(e_fp)
            metadata.read()
            self._setProperties(metadata.getProperties())
    
            # re-read actions and validators whenever we re-read the file
            self._read_action_metadata(self.getId(), self.filepath)
            self._read_validator_metadata(self.getId(), self.filepath)

Globals.InitializeClass(FSControllerBase)
