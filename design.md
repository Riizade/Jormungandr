Arbitrary Attribute Generation Ordering
------------------------------------------------------------------------------------------------------------------------
If an option for an attribute has requirements, and that requirement's attribute has already been generated on that entity:
    The requirement is considered met if and only if the entity's attribute fulfills the option's requirement on that attribute.
    If the requirement is not met, that option cannot be generated for that entity.
If an option for an attribute has requirements, and that requirement's attribute has not yet been generated for that entity:
    If the requirement is on a numeric attribute:
        Tighten the upper and lower bounds on the values that can be generated for that attribute
        If the lower bound would be greater than the upper bound, this option cannot be generated for that entity
    If the requirement is on a text attribute:
        If there are currently no requirements on that attribute, add the required text to the list of valid options on that attribute
        If there are currently requirements on that attribute, replace those requirements with the set-intersection of the two lists. 
        If the set-intersection of these lists is empty, this option cannot be generated for that entity.
        
        
If this feature is to be implemented, using selection commands as requirements for an attribute will require a ton of time during generation.
This is because for a given selection command, the valid values are vast, and you have to check if a particular requirement can be generated from a selection command, which means navigating the parse tree.

Additionally, weighting will be dominated heavily by which field is generated first. For instance, consider the situation that it's likely for an old person to have grey hair, but it's not likely that a person is old
If age is generated first, the distribution is correct.
If hair color is generated first, getting grey hair is now unconditionally more likely than having non-grey hair. In this case, age will be generated second in a range conforming to the requirements of having grey hair.
This means that lots of grey hair will be generated, and consequently, lots of older people.
This means that enabling this feature disallows conditionality of probability on other fields.

The major benefit of arbitrary generation order is the ability to specify attributes unconditionally before generation, allowing for towns to generate say, a certain number of people with the guard occupation, rather than relying on randomness.
However, this feature messes with probability distributions for certain required occupations (which may be desired).

The lookup time can be minimized by maintaining a graph of the probability information. The tree would be constructed from the JSON, then we could traverse it backward to calculate the probabilities of having selected a particular attribute from the value that would have been its parent, had it been generated in the specified order in the file. We can use these probabilities to reverse the tree and select attributes based on the attributes we were given at generation time.


Alternative implementation 1:
Instead of having this feature, attributes could have a definite generation order. With this implementation, if I want to specify a particular attribute before generation, I would have to generate an entity up to that attribute, then check if the entity meets all requirements. If not, then I have to regenerate. This gives no guarantees that a valid entity will or can ever be generated.
The advantage of this implementation is that I can use selection commands as requirements, but anything requiring text or selection commands must be generated before the required attribute.
This is confusing because it then causes numeric attribute requirements to have been generated beforehand, while text and selection attribute requirements must be generated afterward.

Alternative implementation 2:
Remove requirements.
This has lots of downsides, like not being able to split names by male/female.