# vegdatabase-sort
Sorts and analyzes Nasjonal vegdatabank with the vegdatabase api (https://api.vegdata.no/).

To use this program, you will firstly need to run ```file_sorter.py``` in order to update data to be as new as possible. After that you can run ```script.py``` and input your desired value.

# objectwiki.txt
Contains a list of all RoadObjects as well as each RoadObjects' attributeType and their id. This is the easiest way to understand what id belongs to what name. It makes it easier to create queries, simply search for the id or the name of the object or feature you are looking for.

# queries.txt
Contains a list of query examples, with short explanations of each id and value used. The NVDB documentation site gives a general understanding of how to write queries: https://api.vegdata.no/.

# python
- **script.py**
  - Contains a script which will allow the user to easily enter a width and then be redirected to https://www.vegvesen.no/nvdb/vegkart/v2 to look at a map with details of the road with the given width filter. The second tab of this program also allows the user to view statistics about their search. Currently the most important file used by this script is ```files/query_vegref_med_felt.json```

- **file_sorter.py**
  - Contains a script that sorts through information and saves it for easy use. This information is used in script.py to display statistics about the given input.

- **other**
  - files: contains .json files for script.py and file_sorter.py to use.
  - unused: contains old .json files and old methods previously used in file_sorter.py

# java
- **InfoCollectorNVDB.java** and **Main.java**
  - Contains a couple methods to collect important information about RoadObject types and  their Attribute types. This method prints the information to objectwiki.txt.

# Getting started

- **Step 1: Download Python 3.7**
  - If you have brew, run ```brew install python3``` followed by ```python3 --version```. The version should be 3.7.4 or newer. If you don't have brew, search Google for ```install brew <operating system>``` and follow the first guide. When writing ```brew doctor```, the command line should say ```Your system is ready to brew```
- **Step 2: Install python requirements**
  ```
  pip3 install PyQt5==5.13.0
  ```
- **Step 3: Run** ```script.py``` **from python folder**
  ```
  python3 script.py
  ```
