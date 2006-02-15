from Products.GenericSetup.PythonScripts.exportimport \
     import PythonScriptBodyAdapter

from Products.CMFFormController.interfaces import IControllerValidator


class ControllerValidatorBodyAdapter(PythonScriptBodyAdapter):
    """
    Body im- and exporter for ControllerPythonScript.
    """
    __used_for__ = IControllerValidator

    suffix = '.vpy'
