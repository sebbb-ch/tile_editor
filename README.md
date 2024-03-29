NOTES

- Exports a dict with coordinates as keys (as strings) and tile "value" as values
    - This means that when reading in the json, you need to convert those string keys into actual int tuples (most likely using literal_eval)
- The tile palette is in a directory with the tiles named in the numerical order you want them to appear on the palette

BUGS
- When you export with the grid on, the screenshot will show both the mouse brush and the grid. No bueno.

TODOS
- move the grid around so you can edit something more than just the one screen
    - the top left and bottom right corners will delineate the size of the map in this case
- load in a map from json and be able to make edits
- click and drag to place multiple tiles of a certain brush
- custom brushes (i.e. more than just the one tile at a time)