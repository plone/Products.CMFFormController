from StringIO import StringIO

def install(self):
    out = StringIO()

    if not hasattr(self, 'portal_form_controller'):
        addTool = self.manage_addProduct['CMFFormController'].manage_addTool
        addTool('Form Controller Tool')
        out.write('Added Form Controller Tool\n')

    return out.getvalue()
