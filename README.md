# Orienteering_Archieve_Automation

Some usefull script to automate the processing in setting up a new map, update old symbols set or export in different format. Currently support only OCAD file.

## To-Do

## Change of persepective

-   [ ] Using a local temp folder to store exportXML file
-   [ ] Use python to launch ocad and export pdf/gif files
-   [ ] Use a sqlite3 local / online database to store info about map (easier to retrive info and to checks)
-   [ ] Finally delete the API folder and move the PDF exported file into root folder for each map

### GUI

-   [ ] Fixing InfoView
    -   [ ] Name of app
    -   [ ] Small description
    -   [ ] Brief _How to use_
    -   [ ] Tommaso Bocchietti
-   [ ] Fixing MapsManagementView
    -   [ ] Make TreeView 60% width (right) and 100% height
    -   [ ] Attach ScrollBar to TreeView
    -   [ ] Add filters (Name_Map, Map_Status (omologata?), Folder_Status)
    -   [ ] Set color for Folder_Status not ok
-   [ ] Fixing MapDetailsView (**should be just a viewer**)
    -   [ ] Display all info from map_data[mapID] variable
-   [ ] MapActionsView

### Functions

-   [ ] Implement login system on startup
-   [ ] Deal with Module integration in global app
