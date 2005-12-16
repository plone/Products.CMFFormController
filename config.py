# BBB CMF < 1.5
try:
    from Products.CMFCore.permissions import AddPortalContent
except ImportError:
    from Products.CMFCore.CMFCorePermissions import AddPortalContent

ADD_CONTENT_PERMISSION = AddPortalContent
PROJECTNAME = 'CMFFormController'
SKINS_DIR = 'skins'

GLOBALS = globals()
