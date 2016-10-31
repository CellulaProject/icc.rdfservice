import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()


setup(name='icc.rdfservice',
      version=0.1,
      description='icc.rdfservice',
      long_description=README,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pylons",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application"
      ],
      keywords="web services",
      author='',
      author_email='',
      url='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'rdflib',
        'rdflib-jsonld',
        'rdflib-kyotocabinet==0.1',
	'pyramid',
	'waitress',
	'cornice',
	'zope.component [zcml]',
        ],
      dependency_links = [
        'https://github.com/eugeneai/rdflib-kyotocabinet/archive/master.zip#egg=rdflib-kyotocabinet-0.1',
        ],
      package_dir = {'': 'src'},
      entry_points = """\
      [paste.app_factory]
      main=app:main
      """,
      paster_plugins=['pyramid'])
