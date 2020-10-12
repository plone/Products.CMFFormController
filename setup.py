from setuptools import setup, find_packages

version = '4.1.4'

setup(
    name='Products.CMFFormController',
    version=version,
    description=("CMFFormController provides a form validation mechanism "
                 "for CMF."),
    long_description=(open("README.rst").read() + "\n" +
                      open("CHANGES.rst").read()),
    classifiers=[
        "Development Status :: 6 - Mature",
        "Framework :: Plone",
        "Framework :: Plone :: 5.2",
        "Framework :: Zope2",
        "Framework :: Zope :: 4",
        "Framework :: Zope :: 5",
        "License :: OSI Approved :: BSD License",
        "License :: OSI Approved :: Zope Public License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords='Zope CMF Plone form validation',
    author='Geoff Davis',
    author_email='plone-developers@lists.sourceforge.net',
    url='https://pypi.org/project/Products.CMFFormController',
    license='BSD',
    packages=find_packages(),
    namespace_packages=['Products'],
    include_package_data=True,
    zip_safe=False,
    extras_require=dict(
        test=[
            'plone.app.testing',
            'plone.app.contenttypes',
        ]
    ),
    install_requires=[
        'setuptools',
        'zope.interface',
        'zope.structuredtext',
        'zope.tales',
        'Products.CMFCore',
        'Products.GenericSetup>=1.8.3',
        'Acquisition',
        'transaction',
        'Zope2>=4.0.a2',
        'Products.PythonScripts>=4.2',
    ],
)
