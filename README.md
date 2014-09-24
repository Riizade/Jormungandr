Jormungandr
===========

A world/campaign setting generator written in Python.

## JSON Generation File Structure ##
Each JSON generation file has two main objects. These are the "profile" and the "resources" section.
The values stored in each sections are lists of objects called "options".

### Profile ###
This specifies what attributes a particular entity has, and how to generate them.
Each key in this object is an attribute that the generated entity will have.
The list of options that make up the value of each key is a list of values that can fill that attribute.

### Resources ###
The resources object contains a list of keys that can be referenced in the values of options.

### Options ###
Each option has 3 components, val, wt, and req.

#### val ####
This is the value of the option that can be stored in the resulting entity of a generation file. 
This field supports the following command grammar: 
 - Selection Command
 - Numeric Generation Command

#### wt ####
This is the weight of the option, relative to the weights of the options listed alongside it. A higher weight means that this option is more likely to be chosen. The weights are arbitrary integers, and don't need to add to a particular value.

#### req ####
This object is a list of requirements that must be satisfied for this option to be chosen for a particular entity. 
Each key in this object is an attribute that the entity must have. The value of each key is a list of valid values for that attribute. An option will only be chosen for a particular entity if for each key in req, the value of that same key in the entity is appears in the list of values for that key in req.
This field supports the following command grammar:
 - Selection Command
 - Numeric Comparison Command
 
When a selection command is used in a req field, it doesn't randomly choose one value to replace that command. Instead, it acts as if it is every value for that command.
This way if you want to say that for instance, an option is valid if a person's occupation is any kind of metalworker, you can specify in req "occupation": "[$smith$, $miner$]".

## Command Grammar ##

### Selection Command ###
Anything inside $ signs is a selection command. (e.g. $color$ is a selection command)  
During generation, a selection command will be replaced with an option value that is valid for the particular entity it is being generated for.  
Selection commands are recursive in a sense. If a selection command generates a value that has another selection command in it, the process will be repeated until a complete value with no commands left is reached.  
If the same selection command is specified multiple times in the value of an option (for example "$name$ $name$ $name$"), each instance of the command will have a unique value.  

These specifications mean there are two things to watch for when using the selection command:
 - Circular selections:
 
    If a selection command comes up with a value that then uses a selection command to select a parent, the command can be caught in an infinite loop.
    For example, "$name$" appears in a value. The value selected from the resource "name" is "John of $place$". The value selected for "$place$" is "$name$'s Rock", generating "John of $name$'s Rock" This can cause a loop where it continuously selects "$name$'s Rock" and replaces it with "John of John of $place$'s Rock", starting the process over.
 - Exhausting a resource:
 
    If you specify that you need n of a resource, for example "$pdesc$, $pdesc$, $pdesc$", and that resource has <n options, it will not be able to fill each of those fields, and Jormungandr will probably crash.
        
### Numeric Generation Command ###
A numeric generation command looks like this [#-#], where # are numbers.
On entity generation, this command will be replaced with an integer that falls in the range of the two numbers specified, inclusive.

### Numeric Comparison Command ###
A numeric comparison command looks like [>#], [<#] or [=#].
This command will be used to check if a certain field has a number respectively greater than, less than, or equal to the number specified in the command.
This command type only appears in the "req" field of options.