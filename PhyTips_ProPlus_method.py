# imports
from opentrons import robot, labware, instruments

# metadata
metadata = {
    'protocolName': '0.3 mL / 20 uL Phytip ProPlus purification',
    'author': 'Jeff Dantzler <dantzler@goodtherapeutics.com>',
    'description': 'Protocol to purify proteins with an Fc that will bind to protein A',
}

# labware

# plate layout by column:
# column 	1:	PBS for equilibration			volume:	1.0 mL
#			2:	sample containing Fc			volume:	? >200 uL
#			3:	PBS wash						volume: 1.0 mL
#			4:	acetate pH 6.0 wash				volume: 1.0 mL
#			5:	acetate pH 3.5 elution buffer	volume: 60 uL
#			6:	neutralization buffer			volume: as needed to aspirate 6 uL

# create custom plate
custom_plate_name = 'VWR_SBS_96_well_1.2mL_plate'

if custom_plate_name not in labware.list():
    labware.create(
        custom_plate_name,  	# name of you labware
        grid=(12, 8),       	# number of (columns, rows)
        spacing=(9, 9),         # distances (mm) between each (column, row)
        diameter=8.24,      	# x dimension of well ** crude hack to tell API that it is a round well since x-size throws error **
#       y-size=8.24,	      	# y dimension of well
        depth=24.63,            # depth (mm) of each well
        volume=1200)        	# volume (µL) of each well

plate = labware.load(custom_plate_name, slot='2')

tiprack = labware.load('opentrons_96_tiprack_300ul', '3')

# pipettes
pipette = instruments.P300_Multi(
    mount='right',
    aspirate_flow_rate=8,
    dispense_flow_rate=8,
    blow_out_flow_rate=16,
    tip_racks=[tiprack])	# *** DO NOT CALL (tiprack) in pipette.pick_up_tip() command *** !!!


# commands

# define variables
tip_air_gap = 40
cycle_delay_time = 2
equilibration_volume = 180
equilibration_final_dispense_addition = 2
capture_volume = 190
capture_final_dispense_addition = 5
wash_volume = 190
wash_final_dispense_addition = 5
elution_volume = 3 * 20 				# 3x 20 uL resin volume
elution_final_dispense_addition = 10

# define functions
def process_sample(location, sample_volume, backpressure_compensation_volume,
	cycle_count, final_dispense_addition, delay_time):
	pipette.move_to(plate.columns(location).bottom())
	for cycle in range(cycle_count - 1):
		pipette.aspirate(sample_volume + backpressure_compensation_volume)
		pipette.delay(seconds=delay_time)
		pipette.dispense(sample_volume + backpressure_compensation_volume)
		pipette.delay(seconds=delay_time)
	pipette.aspirate(sample_volume + backpressure_compensation_volume)
	pipette.delay(seconds=delay_time)
	pipette.dispense(sample_volume + backpressure_compensation_volume + final_dispense_addition)
	pipette.delay(seconds=delay_time)


# aspirate air gap prior to picking up the tips (apparently this is not allowed!)
# how can we hack this?
pipette.aspirate(tip_air_gap)

# pick up a column of 8 tips from the first column in the tiprack 
pipette.pick_up_tip()

# equilibration step
process_sample(
	location = '1',
	sample_volume = equilibration_volume,
	backpressure_compensation_volume = 0,
	cycle_count = 4,
	final_dispense_addition = equilibration_final_dispense_addition,
	delay_time = cycle_delay_time)

# capture step
process_sample(
	location = '2',
	sample_volume = capture_volume,
	backpressure_compensation_volume = 0,
	cycle_count = 4,
	final_dispense_addition = capture_final_dispense_addition,
	delay_time = cycle_delay_time)

# PBS wash step
process_sample(
	location = '3',
	sample_volume = wash_volume,
	backpressure_compensation_volume = 0,
	cycle_count = 4,
	final_dispense_addition = wash_final_dispense_addition,
	delay_time = cycle_delay_time)

# acetate pH 6.0 wash step
process_sample(
	location = '4',
	sample_volume = wash_volume,
	backpressure_compensation_volume = 0,
	cycle_count = 4,
	final_dispense_addition = wash_final_dispense_addition,
	delay_time = cycle_delay_time)

# elution step
process_sample(
	location = '5',
	sample_volume = elution_volume,
	backpressure_compensation_volume = 40,
	cycle_count = 4,
	final_dispense_addition = elution_final_dispense_addition,
	delay_time = cycle_delay_time)

pipette.return_tip()

