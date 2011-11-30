# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

from setuptools import setup, find_packages


setup(
    name='gocept.zcapatch',
    version='0.1dev',
    author='gocept <ws at gocept dot com>',
    author_email='ws@gocept.com',
    url='',
    description="""\
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
