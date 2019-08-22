# vegdatabase-sort
Sorts and analyzes the vegdatabase with the vegdatabase api

# objectwiki.txt
Contains a list of all RoadObjects as well as each RoadObjects' attributeType and their id. This is the easiest way to understand what id belongs to what name. It makes it easier to create queries, simply search for the id or the name of the object or feature you are looking for.

# queries.txt
Contains a list of query examples, with short explanations of each id and value used. The NVDB documentation site gives a general understanding of how to write queries: https://api.vegdata.no/.

# python --> script.py
Contains a script which will allow the user to easily enter a width and then be redirected to https://www.vegvesen.no/nvdb/vegkart/v2 to look at a map with details of the road with the given width filter.

# java --> InfoCollectorNVDB.java
Contains a couple methods to collect important information about RoadObject types and  their Attribute types. This method prints the information to objectwiki.txt.
