# imports
from opentrons import robot, labware, instruments
# robot.connect()
# robot.turn_on_rail_lights()
# robot.reset()
# robot.home()

# labware
sourcePlate1 = labware.load('NUNC_V96_PP_0.45mL_plate', slot='5')
#sourcePlate2 = labware.load('NUNC_V96_PP_0.45mL_plate', slot='6')
destinationPlate1 = labware.load('ProxiPlate-384HS', slot='4')
tip_rack_1 = labware.load('tiprack-10ul', slot='8')

# pipettes
pipette = instruments.P10_Single(
    mount='left',
    tip_racks=[tip_rack_1])

oddColumns = list(map(str, range(1, 25, 2)))
evenColumns = list(map(str, range(2, 25, 2)))
volume = 1.5
sourceRows=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
destinationRows=['A', 'E', 'I', 'M']

# create list of source wells, in order
sourceWells = []
for row in sourceRows:
    # generate list of all wells in this row
    currentRow = []
    for column in range(12):
        well = row + str(column+1)
        sourceWells.append(well)

# create list of destination wells, in order
destinationWells = []
for row in destinationRows:
    currentRow = []
    for column in oddColumns:
        well = row + str(column)
        destinationWells.append(well)
    for column in evenColumns:
        well = row + str(column)
        destinationWells.append(well)

for well in range(96):
    print("source: ", sourceWells[well])
    print("destination: ", destinationWells[well])
    pipette.transfer(volume,
                     sourcePlate1(sourceWells[well]),
                     destinationPlate1(destinationWells[well])
                     )

