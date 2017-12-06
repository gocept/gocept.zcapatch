from setuptools import setup, find_packages


setup(
    name='gocept.zcapatch',
    version='1.1',
    author='Wolfgang Schnerring, Thomas Lotze <mail at gocept dot com>',
    author_email='mail@gocept.com',
    url='https://bitbucket.org/gocept/gocept.zcapatch',
    description="""\
Test helpers to temporarily alter zope.component registrations
""",
    long_description=(
        open('README.rst').read()
        + '\n\n'
        + open('CHANGES.rst').read()),
    keywords="zca testing patch adapter utility remove",
    classifiers="""\
License :: OSI Approved :: Zope Public License
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Programming Language :: Python :: Implementation :: CPython
Programming Language :: Python :: Implementation :: PyPy
"""[:-1].split('\n'),
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    license='ZPL',
    namespace_packages=['gocept'],
    install_requires=[
        'setuptools',
        'zope.component',
    ],
    extras_require=dict(test=[
        'mock',
        'zope.interface',
    ]),
)
