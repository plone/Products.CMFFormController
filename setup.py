from setuptools import setup, find_packages

version = '3.0.5'

setup(name='Products.CMFFormController',
      version=version,
      description="CMFFormController provides a form validation mechanism for CMF.",
      long_description=open("README.txt").read() + "\n" +
                       open("CHANGES.txt").read(),
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Framework :: Zope2",
        "License :: OSI Approved :: BSD License",
        "License :: OSI Approved :: Zope Public License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
      ],
      keywords='Zope CMF Plone form validation',
      author='Geoff Davis',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://pypi.python.org/pypi/Products.CMFFormController',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      extras_require=dict(
        test=[
            'plone.app.testing',
        ]
      ),
      install_requires=[
        'setuptools',
        'zope.interface',
        'zope.structuredtext',
        'zope.tales',
        'Products.CMFCore',
        'Products.GenericSetup',
        'Acquisition',
        'transaction',
        'Zope2',
      ],
)
