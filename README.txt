CMFFormController

    CMFFormController replaces the portal_form form validation mechanism from
    Plone. It should work just fine in plain CMF as well.

Requires

    CMF 1.5+
    Zope 2.8.5+

Quickstart

    For CMF 1.5:
    1) Create an external method, module CMFFormController.Install,
       function: install
    2) Run it

    Profiling CMFFormController scripts:
    * If you want to use CallProfiler with CMFFormController, you will
      need to download and install the CMFFormControllerPatch product
      from the Collective.
      (Thanks to Andy McKay)

Documentation

    See www/docs.stx
