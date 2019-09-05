# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                     #
#                       PROTOCOL                      #
#                                                     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

from opentrons import robot, containers, instruments
from opentrons.util.vector import Vector
from math import cos, sin

robot.connect(robot.get_serial_ports_list()[0])
robot.home()
robot.head_speed(17000)

# Container Types ======================================

tiprack_type   = 'tiprack-200ul'
water_type     = 'point'
trash_type     = 'point'

tray_type      = '96-PCR-flat'
petri_type     = 'point'
petri_diameter = 85

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
	tip_racks       = tipracks,
	aspirate_speed  = 300,
	dispense_speed  = 500,
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


def run_protocol( petries, petri_diameter, trays, tiprack, waterbowls, trash ):

	step = (petri_diameter / _b) / len(tray.wells())

	for petri, tray, waterbowl, tip_well in zip( petries, trays, waterbowls, tiprack.wells() ):

		_a, _b, _theta,  = 0, 0.5, 0

		pipette.pick_up_tip( tip_well )

		for tray_well in tray.wells():

			pipette.aspirate( 50 , waterbowl )

			_x, _y = polar_to_cartesian(archimdean_spiral(_a, _b, _theta, _theta_max), _theta)
			_theta += step

			pipette.move_to(( petri, Vector(
				petri._coordinates.coordinates.x + _x,
				petri._coordinates.coordinates.y + _y,
				petri._coordinates.coordinates.z
			)), 'arc' ).aspirate( 50 )

			pipette.dispense( tray_well ).blow_out()

		pipette.drop_tip( trash )


# Run Protocol =================================================

run_protocol( petries, petri_diameter, trays, tipracks[0], waterbowls, trashes[0] )
robot.home()
