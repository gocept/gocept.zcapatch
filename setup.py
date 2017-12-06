from setuptools import setup, find_packages


setup(
    name='gocept.zcapatch',
    version='1.1.dev0',
    author='Wolfgang Schnerring, Thomas Lotze <tl at gocept dot com>',
    author_email='tl@gocept.com',
    url='https://bitbucket.org/gocept/gocept.zcapatch',
    description="""\
Test helpers to temporarily alter zope.component registrations
""",
    long_description=(
        open('README.rst').read()
        + '\n\n'
        + open('CHANGES.rst').read()),
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
