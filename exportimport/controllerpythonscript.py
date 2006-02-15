from Products.GenericSetup.PythonScripts.exportimport \
     import PythonScriptBodyAdapter

from Products.CMFFormController.interfaces import IControllerPythonScript


class ControllerPythonScriptBodyAdapter(PythonScriptBodyAdapter):
    """
    Body im- and exporter for ControllerPythonScript.
    """
    __used_for__ = IControllerPythonScript

    suffix = '.cpy'
