# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                     #
#                       PROTOCOL                      #
#                                                     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

from opentrons import containers, instruments
from math import cos, sin

# Container Types ======================================

tiprack_type  = 'tiprack-200ul'
water_type    = 'point'
trash_type    = 'point'

tray_type     = '96-PCR-flat'
petri_type    = 'point'


# Maping(s) ============================================

#   | A3 | B3 | C3 | D3 | E3 |
#   | A2 | B2 | C2 | D2 | E2 |
#   | A1 | B1 | C1 | D1 | E1 |

trash_slots   = [ 'A1', ]
tiprack_slots = [ 'A3', ]

water_slots  = [ 'B3', 'C3', 'D3', ]
petri_slots  = [ 'B2', 'C2', 'D2', ]
tray_slots   = [ 'B1', 'C1', 'D1', ]


# Container(s) =========================================

trashes     = [ containers.load ( trash_type   , slot ) for slot in trash_slots   ]
tipracks    = [ containers.load ( tiprack_type , slot ) for slot in tiprack_slots ]
waterbowls  = [ containers.load ( water_type   , slot ) for slot in water_slots   ]
petries     = [ containers.load ( petri_type   , slot ) for slot in petri_slots   ]
trays       = [ containers.load ( tray_type    , slot ) for slot in tray_slots    ]


# Instruments(s) ======================================

pipette = instruments.Pipette(
	axis            = 'b',
	name            = 'p200_Single',
	channels        = 1,
	min_volume      = 0,
	max_volume      = 200,
	aspirate_speed  = 300,
	dispense_speed  = 500,
	tip_racks       = tipracks,
	trash_container = trashes[0]
)


# Custom Protocol =============================================

def archimdean_spiral(a, b, theta):
	"""
	Archimdean spiral function.
	"""

	r = a + b * theta
	return r

def polar_to_cartesian(r, theta):
	"""
	Convert from Polar coordinates to Cartesian coordinates.
	"""
    x = r * cos(theta)
    y = r * sin(theta)

	return x, y

def run_protocol( petries, trays, tiprack, waterbowls, trash ):

	for petri, tray, waterbowl, tip_well in zip( petries, trays, waterbowls, tiprack.wells() ):

		_a, _b, _theta = 1, 2, 0

		pipette.pick_up_tip( tip_well )

		for tray_well in tray.wells():

			pipette.aspirate( 100 , water )

			_x, _y = polar_to_cartesian(archimdean_spiral(_a, _b, _theta), _theta)
			_theta += 0.3

			pipette.move_to( Vector(
				petri._coordinates.coordinates.x + _x,
				petri._coordinates.coordinates.y + _y,
				petri._coordinates.coordinates.z
			), 'arc' ).aspirate( 100 )

			pipette.dispense( tray_well )

		pipette.drop_tip( trash )


# Run Protocol =================================================

run_protocol( petries, trays, tipracks[0], waterbowls, trashes[0] )
