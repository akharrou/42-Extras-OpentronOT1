# ======================= #
#  OpentronsRobot Module  #
# ======================= #

# IMPORTS - - - - - - - - - - - - - - - - - - - - - - - - - - -

from opentrons import robot

# CLASS - - - - - - - - - - - - - - - - - - - - - - - - - -

class Opentron():

	def __init__( self, protocols=[] ):

		self._protocols = protocols
		self.connect()


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

		print('Connecting...')
		robot.connect( robot.get_serial_ports_list()[0] )
		if robot.is_connected():
			print('\nSuccessfully Connected.')
			robot.reset()
			robot.home()

	def load_protocols( self, protocols=[] ):
		self._protocols.extend( protocols )

	def remove_protocols( self, protocols=[] ):
		for protocol in protocols:
			self._protocols.remove( protocol )

	def run( self, protocols=[] ):

		if protocols == []:
			protocols = self.protocols
		elif type(protocols) == type(str()):
			protocols = list(protocols)
		for file in protocols:
			with open( file, 'r' ) as fd:
				exec(
					compile(	source=file,
								filename='error.log',
								mode='exec' )
				)

	def runAll( self ):

		run()


	# WITH STATEMENT ====================================

	def __enter__( self ):

		return opentrons.robot

	def __exit__( self, exc_type, exc_val, traceback ):

		print('Homing, Resetting & Disconnectig...')
		robot.home()
		robot.reset()
		robot.disconnect()
