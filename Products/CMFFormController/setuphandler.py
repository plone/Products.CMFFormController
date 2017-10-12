# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer

import warnings


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            'Products.CMFFormController:uninstall',
            # bbb:
            'Products.CMFFormController:CMFFormController',
        ]


def deprecate_profiles_confusing_name(tool):
    warnings.warn(
        'The profile with id "Products.CMFFormController:CMFFormController" '
        'was renamed to "Products.CMFFormController:default".',
        DeprecationWarning
    )
