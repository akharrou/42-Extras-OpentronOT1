# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                     #
#                       PROTOCOL                      #
#                                                     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

from setup import *
from trons import Opentron
from opentrons.util import environment

robot = Opentron()

# Comman:ds =============================================

for i in range( ROUNDS ):

	pipette.pick_up_tip( tiprack.wells(i) )

	for tray_idx in range( TOTAL_TRAY_INDICES ):

		pipette.aspirate( 100 , water )
		pipette.aspirate( 50  , petries[i] )

		pipette.dispense( trays[i].well( tray_idx ) )

	pipette.drop_tip( trash )
