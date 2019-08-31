
# Map ================================================

#   | A2 | B2 | C2 | D2 | E2 |
#   | A1 | B1 | C1 | D1 | E1 |

tiprack_slots = [ 'A2', ]
trash_slots   = [ 'B2', ]
water_slots   = [ 'C2', ]

tray_slots    = [ 'A1', 'E1', 'E2', ]
petri_slots   = [ 'B1', 'D1', 'D2', ]


# Variable(s) ========================================

tiprack_type  = 'tiprack-200ul'
water_type    = 'point'
trash_type    = 'point'

tray_type     = '96-PCR-flat'
petri_type    = 'point'


# Container(s) ========================================

tipracks = [ containers.load ( tiprack_type , slot ) for slot in tiprack_slots ]
trashes  = [ containers.load ( trash_type   , slot ) for slot in trash_slots   ]
waters   = [ containers.load ( water_type   , slot ) for slot in water_slots   ]
petries  = [ containers.load ( petri_type   , slot ) for slot in petri_slots   ]
trays    = [ containers.load ( tray_type    , slot ) for slot in tray_slots    ]

tiprack = tipracks[0]
trash   = trashes[0]
water   = waters[0]
petri   = petries[0]
tray    = trays[0]

# Pipette(s) ===========================================

pipette = instruments.Pipette(
	axis            = 'b',
	name            = 'p200_Single',
	channels        = 1,
	min_volume      = 0,
	max_volume      = 200,
	aspirate_speed  = 300,
	dispense_speed  = 500,
	tip_racks       = [tiprack],
	trash_container = trash
)
