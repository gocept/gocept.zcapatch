# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

from setuptools import setup, find_packages


setup(
    name='gocept.zcapatch',
    version='1.0',
    author='Wolfgang Schnerring <ws at gocept dot com>, Thomas Lotze <tl at gocept dot com>',
    author_email='ws@gocept.com',
    url='http://code.gocept.com/hg/public/gocept.zcapatch',
    description="""\
Test helpers to temporarily alter zope.component registrations
""",
    long_description=(
        open('README.txt').read()
        + '\n\n'
        + open('CHANGES.txt').read()),
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
