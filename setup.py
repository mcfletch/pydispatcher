#!/usr/bin/env python
"""Installs PyDispatcher using distutils

Run:
	python setup.py install
to install the package from the source archive.
"""

if __name__ == "__main__":
	import sys,os, string, fnmatch
	from distutils.sysconfig import *
	from distutils.core import setup

	##############
	## Following is from Pete Shinners,
	## apparently it will work around the reported bug on
	## some unix machines where the data files are copied
	## to weird locations if the user's configuration options
	## were entered during the wrong phase of the moon :) .
	from distutils.command.install_data import install_data
	class smart_install_data(install_data):
		def run(self):
			#need to change self.install_dir to the library dir
			install_cmd = self.get_finalized_command('install')
			self.install_dir = getattr(install_cmd, 'install_lib')
			# should create the directory if it doesn't exist!!!
			return install_data.run(self)
	##############
	### The following automates the inclusion of files while avoiding problems with UNIX
	### where case sensitivity matters.
	dataFiles = []
	excludedTypes = ('.py','.pyc','.pyo','.db','.gz','.bat', ".cvsignore")
	excludedDirectories = ('build','dist','cvs')
	def nonPythonFile( file ):
		"""Is the fully-qualified name a non-python file"""
		if os.path.isfile( file ):
			return (os.path.splitext( file )[1]).lower() not in excludedTypes
	def directoryWalker( argument, directory, files, prefix = "pydispatch"):
		"""Walk the particular directory searching for non-python files

		prefix -- prefix directory appended to the destination
			directories, normally the name of the target package
		"""
		if os.path.split(directory.lower())[-1] in excludedDirectories:
			return
		result = []
		for file in files:
			file = os.path.join(directory,file )
			if nonPythonFile( file ):
				result.append( file )
		if result:
			argument.append((os.path.join(prefix,directory), result))
	os.path.walk( '.', directoryWalker, dataFiles)

	from sys import hexversion
	if hexversion >= 0x2030000:
		# work around distutils complaints under Python 2.2.x
		extraArguments = {
			'classifiers': [
				"""License :: OSI Approved :: BSD License""",
				"""Programming Language :: Python""",
				"""Topic :: Software Development :: Libraries :: Python Modules""",
				"""Intended Audience :: Developers""",
			],
			'download_url': "https://sourceforge.net/project/showfiles.php?group_id=79755",
			'keywords': 'dispatcher,dispatch,pydispatch,event,signal,sender,receiver,propagate,multi-consumer,multi-producer,saferef,robustapply,apply',
			'long_description' : """Dispatcher mechanism for creating event models

PyDispatcher is an enhanced version of Patrick K. O'Brien's
original dispatcher.py module.  It provides the Python
programmer with a robust mechanism for event routing within
various application contexts.

Included in the package are the robustapply and saferef
modules, which provide the ability to selectively apply
arguments to callable objects and to reference instance
methods using weak-references.
""",
			'platforms': ['Any'],
		}
	else:
		extraArguments = {
		}

	### Now the actual set up call
	setup (
		name = "PyDispatcher",
		version = "2.0.0",
		description= "Multi-producer-multi-consumer signal dispatching mechanism",
		author = "Patrick K. O'Brien",
		author_email = "pydispatcher-devel@lists.sourceforge.net",
		url = "http://pydispatcher.sourceforge.net",
		license = "BSD-style, see license.txt for details",

		package_dir = {
			'pydispatch':'.',
		},

		packages = [
			'pydispatch', 
			'pydispatch.tests',
			'pydispatch.examples',
		],
		
		options = {
			'sdist':{'use_defaults':0, 'force_manifest':1},
			"install_lib":{"compile":0, "optimize":0},
			'bdist_rpm':{
				'group':'Libraries/Python',
				'provides':'python-dispatcher',
				'requires':"python",
			},
		},
		data_files = dataFiles,
		cmdclass = {'install_data':smart_install_data},

		# registration metadata
		**extraArguments
	)
	
