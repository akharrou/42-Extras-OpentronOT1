# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                     #
#                       PROTOCOL                      #
#                                                     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

import setup

# Commands =============================================

for i in range( ROUNDS ):

	pipette.pick_up_tip( tiprack.wells(i) )

	for tray_idx in range( TOTAL_TRAY_INDICES ):

		pipette.aspirate( 100 , water )
		pipette.aspirate( 50  , petries[i] )

		pipette.dispense( tray.well( tray_idx ) )

	pipette.drop_tip( trash )
