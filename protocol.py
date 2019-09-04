# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                     #
#                       PROTOCOL                      #
#                                                     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

from setup import *


# Custom Protocol =============================================

def run_protocol( petries, trays, tiprack, water, trash ):

	for petri, tray, tip_well in
		zip( petries, trays, tiprack.wells() ):

		pipette.pick_up_tip( tip_well )

		for tray_well in tray.wells():

			pipette.aspirate( 100 , water )
			pipette.aspirate( 50  , petri )
			pipette.dispense( tray_well )

		pipette.drop_tip( trash )


# Run Protocol =================================================

run_protocol( petries, trays, tiprack, water_trough, trash )
