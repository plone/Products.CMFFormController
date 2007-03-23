from setuptools import setup, find_packages
import sys, os

version = '2.1b3'

setup(name='Products.CMFFormController',
      version=version,
      description="CMFFormController provides a form validation mechanism for CMF.",
      long_description="""\
      """,
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='Zope CMF Plone form validation',
      author='Geoff Davis',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://svn.plone.org/svn/collective/CMFFormController/trunk',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      download_url='http://plone.org/products/cmfformcontroller/releases',
      install_requires=[
        'setuptools',
      ],
)
