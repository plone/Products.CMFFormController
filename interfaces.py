from Products.GenericSetup.PythonScripts.interfaces import IPythonScript

class IControllerPythonScript(IPythonScript):
    """
    Interface to differentiate btn regular python scripts and controller
    python scripts.
    """

class IControllerValidator(IPythonScript):
    """
    Interface to differentiate btn regular python scripts and controller
    validator scripts.
    """
