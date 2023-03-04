This version has the following changes:

V9.1
----
1. Changed the font "arial" to "Arial". There was a compability issue using python 3.9
2. Replace the "protocol" with "data_entity". This will now store data entities being transferred in the interface
3. Updated the default_mapping.json with the above 
4. Changed the app.py file to include a random number for the images. This does not take the image from browser cache now.
5. Included a new file 'fileintegrity' to check if an existing image is there in the directory based on a sha256 check

V9.0
----
1. Introduced a new column - reverse_flow with values as 'Y' or 'N'. 'Y' indicates that the flow is also reversed.
2. Changed the logic for mapping.json to accept any columns not in the code. This will only map the columns that is found in mapping.json
3. Changes made to accept a system which is also part of the main flow and an input to the main flow.
4. Introduced a config file to set all colors and initialising parameters. This change is only to _class file
5. Introduced a new function - _reduce_gap_group() which reduces the gap between 2 functional groups
6. renamed _reduce_gap_new2() function to_reduce_gap_between_boxes()
7. IMG_HEIGHT adjusted due to reducing in gaps
8. Collapsed the dataflow group name to print just once.
9. Introduced the mapping.json document as a parameter to the file. this is only in _class file
10. Introduced font as "arial" for all. This is only for _class file
11. Corrected the signature of the function call in app.py. Included the mapping parameter