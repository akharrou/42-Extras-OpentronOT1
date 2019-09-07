# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                     #
#                       PROTOCOL                      #
#                                                     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

from opentrons.containers import unpack_location
from opentrons import robot, containers, instruments
from opentrons.util.vector import Vector
from math import cos, sin

robot.connect(robot.get_serial_ports_list()[0])
robot.head_speed(20000)
robot.home()

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
    aspirate_speed  = 2000,
    dispense_speed  = 2000,
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
    Convert Polar coordinates to Cartesian coordinates.
    """

    x = r * cos(theta)
    y = r * sin(theta)

    return x, y


def run_protocol( petries, petri_diameter, trays, tiprack, waterbowls, trash ):

    _a, _b = 5, 1

    for petri, tray, waterbowl, tip_well in zip( petries, trays, waterbowls, tiprack.wells() ):

        _theta = 1
        step = (petri_diameter / 2 - 2 - _a) / _b / len(tray.wells())

        pipette.pick_up_tip( tip_well )

        for tray_well in tray.wells():

            pipette.move_to(( waterbowl, Vector(0, 0, 20) ), 'arc').aspirate(60)
            pipette.aspirate( 50 , waterbowl )

            dx, dy = polar_to_cartesian(archimdean_spiral(_a, _b, _theta), _theta)
            _theta += step

            pipette.move_to(( petri, Vector(dx, dy, 10)), 'arc')
            pipette.aspirate(20)
            pipette.move_to(( petri, Vector(dx, dy, 0)), 'arc').aspirate(70)

            # Jiggle
            pipette.move_to(( petri, Vector(dx + 2, dy, 0)), 'direct')
            pipette.move_to(( petri, Vector(dx + -2, dy, 0)), 'direct')
            pipette.move_to(( petri, Vector(dx, dy, 0)), 'direct')
            pipette.move_to(( petri, Vector(dx, dy + 2, 0)), 'direct')
            pipette.move_to(( petri, Vector(dx, dy + -2, 0)), 'direct')

            pipette.dispense( 200, tray_well ).blow_out()

        pipette.drop_tip( trash )


# Run Protocol =================================================

run_protocol( petries, petri_diameter, trays, tipracks[0], waterbowls, trashes[0] )
robot.home()
