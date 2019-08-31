
from trons import Opentron

with Opentron() as tron:

	# Map(s) =============================================

#   | A2 | B2 | C2 | D2 | E2 |
#   | A1 | B1 | C1 | D1 | E1 |

	tiprack_slots = [ 'A2', ]
	trash_slots   = [ 'B2', ]
	water_slots   = [ 'C2', ]

	tray_slots    = [ 'A1', 'E1', 'E2' ]
	petri_slots   = [ 'B1', 'D1', 'D2' ]


	# Variable(s) ========================================

	tiprack_type  = 'tiprack-200ul'
	water_type    = 'point'
	trash_type    = 'point'

	tray_type     = '96-PCR-flat'
	petri_type    = 'point'


	# Container(s) ========================================

	tipracks = [ container.load ( tiprack_type , slot ) for slot in tiprack_slots ]
	trashes  = [ container.load ( trash_type   , slot ) for slot in trash_slots   ]
	water    = [ container.load ( water_type   , slot ) for slot in water_slots   ]

	petries  = [ container.load ( petri_type   , slot ) for slot in petri_slots   ]
	trays    = [ container.load ( tray_type    , slot ) for slot in tray_slots    ]


	# Pipette(s) ===========================================

	pipette = instruments.Pipette(
		pipette_axis           : 'b'
		pipette_name           : 'p200_Single'
		pipette_channels       : 1
		pipette_min_volume     : 0
		pipette_max_volume     : 200
		pipette_aspirate_speed : 300
		pipette_dispense_speed : 500
		pipette_tip_racks      : [tipracks]
	 )


	# Commands =============================================

	for name, container in robot.get_containers():
    	print( name, container.get_type() )

	for axis, pipette in robot.get_instruments():
		print( pipette.name, axis )

	pipette.pick_up_tip(tiprack.wells('A1'))
	pipette.drop_tip(tiprack.wells('A1'))

	for c in robot.commands():
		print(c)
