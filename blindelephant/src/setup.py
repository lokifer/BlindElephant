from distutils.core import setup

setup(
    name='BlindElephant',
    version='1.0',
    description='Uses static file fingerprinting to determine the version of web applications and plugins installed at a url', 
    author="Patrick Thomas",
    author_email="psthomas@coffeetocode.net", #or pthomas@qualys.com
    url='http://blindelephant.sourceforge.net',
    packages=['blindelephant'],
    package_data={'blindelephant' : ['dbs/*.pkl', 'dbs/*/*.pkl']},
    scripts=['blindelephant/BlindElephant.py'],
    classifiers = [
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "Topic :: Internet :: WWW/HTTP"
        "Programming Language :: Python :: 2.6"
    ]
)