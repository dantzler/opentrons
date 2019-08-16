# imports
from opentrons import robot, labware, instruments

# metadata
metadata = {
    'protocolName': '0.3 mL / 20 uL Phytip ProPlus purification',
    'author': 'Jeff Dantzler <dantzler@goodtherapeutics.com>',
    'description': 'Protocol to purify proteins with an Fc that will bind to protein A',
}

# labware
custom_plate_name = 'VWR_SBS_96_well_1.2mL_plate'

if plate_name not in labware.list():
    labware.create(
        custom_plate_name,  	# name of you labware
        grid=(12, 8),       	# number of (columns, rows)
        spacing=(9, 9),         # distances (mm) between each (column, row)
        x-size=8.24,         	# x dimension of well
        y-size=8.24,			# y dimension of well
        depth=24.63,            # depth (mm) of each well
        volume=1200)        	# volume (µL) of each well

plate = labware.load(custom_plate_name, slot='3')

tiprack = labware.load('opentrons_96_tiprack_300ul', '3')

# pipettes
pipette = instruments.P300_Mutli(
    mount='right',
    aspirate_flow_rate=8,
    dispense_flow_rate=8,
    blow_out_flow_rate=16,
    tip_racks=[tiprack])

