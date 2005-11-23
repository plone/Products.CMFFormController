"""FormController tests package."""

# Zope 2.8-style transaction module
# BBB: Zope 2.7
try:
    import Zope2
except ImportError:
    import transaction_ as transaction
else:
    import transaction
