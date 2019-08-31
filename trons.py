# ======================= #
#  OpentronsRobot Module  #
# ======================= #

# DEPENDENCIES - - - - - - - - - - - - - - - - - - - - - - - - - - -

import sys
from time import sleep

from opentrons import robot, instruments, containers
from opentrons.util import environment


# CONEXT MANAGER - - - - - - - - - - - - - - - - - - - - - - - - - -

class Opentron():

	def __init__( self, protocols=[] ):

		self._protocols = protocols
		self._homed = True

	def __enter__( self ):

		try:

			ports = []
			while ( ports == [] ):

				print('\033[2J\033[H', end="") # Clear Screen & Home Cursor
				ports = robot.get_serial_ports_list()
				if not ports:
					print('Please physically connect Opentron robot to computer.\n')
					print("Press '\033[3menter\033[0m' when done.")
					print("Press '\033[3mctrl-c\033[0m' to exit.")
					input()
				else:
					break

			print("Available ports:\n")
			for index, port in enumerate ( ports, 1 ):
				print('{} - {}'.format( index, port ))

			while (1):

				# Get port index
				print("\nSelect Opentron port: ", end="")
				idx = int(input())
				while ( 0 >= idx or idx > len( ports ) ):
					print("\033[A\033[2K\rSelect Opentron port: ", end="")
					idx = int(input())

				# Try to Connect to Robot
				robot.connect( ports[ idx - 1 ] )

				# Case : Successful
				if robot.is_connected():
					print('\nSuccessfully connected.')
					print('\nPreping to start...')
					robot.reset()
					robot.home()
					print('\nTron is fully operational. Proceeding to protocol(s).')
					sleep(1)
					flush()
					print('\033[2J\033[H', end="") # Clear Screen & Home Cursor
					break

				# Case : Unsuccessful
				else:
					print('Failed to connect to robot.')
					ports.remove( ports[idx] )
					if not ports:
						print('Abort - Failed connection.')
						sys.exit(1)

			return robot

		except KeyboardInterrupt:
			print('\nExiting...')
			sys.exit(1)


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

	def interactive( self ):

		# CONTAINERS ===========================================

		print('1 - Containers:\n')
		self._containers = []

		print('How many containers do you need ?')
		total_containers = int(input())
		for i in range(total_containers):
			pass




		# INSTRUMENTS ==========================================

		print('2 - Instruments:\n')
		self._instruments = []




		# SCRIPT ===============================================

		print('Up to you to write the script ¯\_(ツ)_/¯')



	def __exit__( self, exc_type, exc_val, traceback ):

		print('\033[2J\033[H', end="") # Clear Screen & Home Cursor
		print('Homing, Resetting & Disconnectig...')
		robot.home()
		robot.reset()
		robot.disconnect()
		print('Exitig...')
		sleep(2)
		sys.exit(0)
