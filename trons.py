
# ======================= #
#  OpentronsRobot Module  #
# ======================= #

# DEPENDENCIES - - - - - - - - - - - - - - - - - - - - - - - - - - -

from sys  import exit
from time import sleep

from opentrons import robot, instruments, containers
from opentrons.util import environment


# CONEXT MANAGER - - - - - - - - - - - - - - - - - - - - - - - - - -

class Opentron():

	def __init__( self, homed=True, protocols=[] ):

		self._protocols = protocols
		self._homed = homed

	def __enter__( self ):

		while (1):

			ports = []
			while ( ports == [] ):

				print('\033[2J\033[H') # Clear Screen & Home Cursor
				ports = robot.get_serial_ports_list()
				if not ports:
					print('Please physically connect Opentron robot to computer.')
					print("When done press '\033[3menter\033[0m'.")
					input()
				else:
					break

			for index, port in enumerate ( ports, 1 ):
				print('{} - {}'.format( index, port ))
			print("Select Opentron robot port index: ")

			try:

				# Get port index
				idx = int(input())
				while ( 0 > idx or idx > len( ports ) ):
					print("\033[A\033[2K\r")
					idx = int(input())

				# Connect
				robot.connect( ports[ idx - 1 ] )

				# Case : Unsuccessful
				if not robot.is_connected():
					print('Failed to connect to robot.')
					ports.remove( ports[idx] )
					if not ports:
						print('Abort - Failed connection.')
						sys.exit(1)

			except Exception as e:
				pass

			return robot


	@property
	def protocols(self):
		return self._protocols

	@protocols.setter
	def protocols(self, protocols):
		self._protocols = protocols

	@protocols.deleter
	def protocols(self):
		self._protocols.clear()

	def loadProtocols( self, protocols=[] ):
		self._protocols.extend( protocols )


	def run( self, protocols=[] ):

		# If no filename(s) were passed
		if self._protocols == []:
			runAll()
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
		for file in self._protocols:
			self.run( file )


	def __exit__( self, exc_type, exc_val, traceback ):

		if not self.homed:
			robot.home()
		robot.reset()
		robot.disconnect()
		sys.exit(0)
