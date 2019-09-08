"""
Opentron OT1 -- Custom Protocol:

    NAME
        Mushroom Divi-up

    DESCRIPTION
        With this protocol you can divide up a living organism
        (held on a standard petri dish) into smaller pieces
        and have them grow independently in tray wells (water is
        provided in each tray well).

        Note: we extract the organism from distinct points in the
        petri dish, the end shape that is aimed for is that of a
        (archimedian) spiral.

    MATERIALS NEEDED
        
        Labware:
            - tiprack
            - trash
            - waterbowl(s)
            - petri dish(es)
            - 96-PCR flat tray(s)
            
        Instruments:
            - Single (200-1000ul) Pipette (set on the b axis)

    CONFIGURABLES
    
        - waterbowl dimensions
        - petri dish dimensions
        - pipette size (200-1000ul)
"""

from opentrons import robot, containers, instruments
from opentrons.util.vector import Vector
from math import cos, sin


# Connect to & Configure Robot ==========================

robot.connect(robot.get_serial_ports_list()[0])
robot.head_speed(20000)
robot.home()


# Define Container Types ==============================

tiprack_type   = 'tiprack-200ul'
water_type     = 'point'
trash_type     = 'point'

tray_type      = '96-PCR-flat'
petri_type     = 'point'


# Define Container Mapping(s) =========================

#   | A3 | B3 | C3 | D3 | E3 |
#   | A2 | B2 | C2 | D2 | E2 |
#   | A1 | B1 | C1 | D1 | E1 |

trash_slots   = [ 'A1', ]
tiprack_slots = [ 'A3', ]

water_slots  = [ 'B3', 'C3', 'D3', ]
petri_slots  = [ 'B2', 'C2', 'D2', ]
tray_slots   = [ 'B1', 'C1', 'D1', ]


# Define Container(s) =================================

trashes     = [ containers.load ( trash_type   , slot ) for slot in trash_slots   ]
tipracks    = [ containers.load ( tiprack_type , slot ) for slot in tiprack_slots ]
waterbowls  = [ containers.load ( water_type   , slot ) for slot in water_slots   ]
petries     = [ containers.load ( petri_type   , slot ) for slot in petri_slots   ]
trays       = [ containers.load ( tray_type    , slot ) for slot in tray_slots    ]

petridish_diameter = 85


# Define Instruments(s) ===============================

pipette = instruments.Pipette(
    axis            = 'b',
    name            = 'p200_Single',
    channels        = 1,
    min_volume      = 0,
    max_volume      = 1000,
    tip_racks       = tipracks,
    aspirate_speed  = 1000,
    dispense_speed  = 1000,
    trash_container = trashes[0]
)


# Utils ===============================================

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


# Define Custom Protocol ==============================

def run_custom_protocol( petries, petridish_diameter, trays, tiprack, waterbowls, trash ):

    _a, _b = 5, 1
    step = (petridish_diameter / 2 - 2 - _a) / _b / len(trays[0].wells())

    for petri, tray, waterbowl, tip_well in zip( petries, trays, waterbowls, tiprack.wells() ):

        _theta = 1

        pipette.pick_up_tip( tip_well )

        for tray_well in tray.wells():

            # Aspirate a bit of air followed by a bit of water, twice
            pipette.move_to(( waterbowl, Vector( 0, 0, 20 ) ), 'arc' ).aspirate( 200 )
            pipette.aspirate( 100 , waterbowl )
            pipette.move_to(( waterbowl, Vector( 0, 0, 20 ) ), 'arc' ).aspirate( 100 )
            pipette.aspirate( 100 , waterbowl )

            # Compute new petri X, Y coordinates that we will aspirate specimen from
            dx, dy = polar_to_cartesian(archimdean_spiral(_a, _b, _theta), _theta)
            _theta += step

            # Apply suction to specimen and stay fixed on the ground
            pipette.move_to( ( petri, Vector( dx, dy, 0 ) ), 'arc' ).delay(1).aspirate( 500 )

            # Jiggle pipette in all directions so as to detach specimen from its surroundings
            pipette.move_to( ( petri, Vector( dx + 3 , dy     , 0 ) ), 'direct' )
            pipette.move_to( ( petri, Vector( dx - 3 , dy     , 0 ) ), 'direct' )
            pipette.move_to( ( petri, Vector( dx     , dy     , 0 ) ), 'direct' )
            pipette.move_to( ( petri, Vector( dx     , dy + 3 , 0 ) ), 'direct' )
            pipette.move_to( ( petri, Vector( dx     , dy - 3 , 0 ) ), 'direct' )

            # Place aspirated contents in tray well
            pipette.dispense( tray_well ).blow_out()

        pipette.drop_tip( trash )


# Run Protocol ==========================================

run_custom_protocol( petries, petridish_diameter, trays, tipracks[0], waterbowls, trashes[0] )
robot.home()
print('Process Complete.')
