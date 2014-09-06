Jormungandr
===========

A world/campaign setting generator written in Python.

## Grammar ##
### Variables ###
Anything inside the $ signs is a variable. (e.g. $color$ is a variable)

In a data table used for generation, those variables are tables located in the "resources" attribute. The program will then randomly choose a value from that variable table according to the weights of its elements.
Jormungandr will only count them as valid values for generation if the object that called the variable table fulfills that values "req" section.