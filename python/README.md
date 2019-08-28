# script.py
Creates a GUI for the user to input a value that will show bigger and smaller roads than the value on E18 between Drammen and Oslo. GUI will also open the browser to give a visual representation of what the road looks like on the map. The roads will be colored to give a rough estimate of where roads are smaller and bigger than the given value. There will be a second tab to open in the GUI, this will display more detailed information about the search.

Interesting values that we have included are:
- Smallest road object's "dekkebredde"
- Biggest road object's "dekkebredde"
- The average "dekkebredde" across all road objects
- The percentage of the road that fits the "requirement" input by the user
- The percentage of the road that does not fit the "requirement" input by the user

# file_sorter.py
Creates multiple .json files from the Nasjonal Vegdatabank API, from the different road objects in the area between Drammen and Oslo on E18 to use in script.py. Also merges the files to make one "superfile" that aims to contain all information about every "dekkebredde" road object.
