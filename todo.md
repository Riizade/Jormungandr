Done (needs testing)
------------------------------------------------------------------------------

In Progress
------------------------------------------------------------------------------
- Define data table spec
    - Figure out syntax/parser for weight parsing
    - Decide on a syntax for lists of values in an entity's attribute
    - Decide on a syntax for referencing attributes of the entity

To Do
------------------------------------------------------------------------------
- Build a command-line interface for generating things
- Autosort JSON alphabetically by "val"
- Figure out Doxygen/comments
- Write usage documentation for table spec
- Write/find JSON viewer to easily view data tables
- Write error handling that tests JSON tables for correctness
    - Invalid syntax/values for a field
    - Duplicate specifications for an attribute or resource
    - Determine if something can never be generated (requires an attribute that will not be present at the time of selection)

Feature Wishlist
------------------------------------------------------------------------------
- Generate relationships between objects
- Save a setting (all objects/relationships) to disk
- Allow for editing of a saved setting (individual regeneration of objects, values, etc)
- Build HTML wiki of all generated objects for a setting
- Host the generated HTML locally using Flask
- Enable or disable individual values for different fields using a GUI