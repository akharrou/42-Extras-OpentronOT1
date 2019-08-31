# ======================= #
#  OpentronsRobot Module  #
# ======================= #

# IMPORTS - - - - - - - - - - - - - - - - - - - - - - - - - - -

import sys
from time import sleep

from opentrons import robot, instruments, containers
from opentrons.util import environment


# CLASS - - - - - - - - - - - - - - - - - - - - - - - - - -

class Opentron():

	def __init__( self, protocols=[] ):
		self._protocols = protocols


	# PROPERTIES ========================================

	@property
	def protocols(self):
		return self._protocols

	@protocols.setter
	def protocols(self, protocols):
		self._protocols = protocols

	@protocols.deleter
	def protocols(self):
		self._protocols.clear()


	# METHODS ===========================================

	def connect( self ):

		robot.connect( robot.get_serial_ports_list()[0] )
		if robot.is_connected():
			print('\nSuccessfully connected.')
			robot.reset()
			robot.home()

	def load_protocol( self, protocols=[] ):
		self._protocols.extend( protocols )

	def run( self, protocols=[] ):

		if protocols == []:
			protocols = self.protocols
		else:
			for file in protocols:
				with open( file, 'r' ) as fd:
					exec(
                        compile( source   = file,
                                 filename = 'error.log',
                                 mode     = 'exec'
						)
					)

	def runAll( self ):
		run()


	# WITH STATEMENT ====================================

	def __enter__( self ):

			self.connect()
			return robot

	def __exit__( self, exc_type, exc_val, traceback ):

		print('Homing, Resetting & Disconnectig...')
		robot.home()
		robot.reset()
		robot.disconnect()
		sys.exit(0)
