# powerplant-coding-challenge


## How does it work?

Below you can find the description of the code used for the powerplant-coding-challenge.

# Explanation of the whole process.

Wind plants are prioritized because their use cost is null.
When wind plants' loads are maximum, the rest of the plants are used.

The order of other plants are determined by their unit_price (price * efficiency) and the min and max load values.

# What can be improved

Because of the lack of time, there are many steps I didn't work on.
Here is a list of next steps to improve the model and scripts:

TODO: Generalize wind plants and other plants. The logic can be generalized in case wind plants use becomes not free
TODO: Improve structure of the scripts
TODO: Improve flexibility of types in functions ('int' -> ('float' | 'int') )
TODO: Do more tests on responses. Is the response the optimal solution?
TODO: Improve data structures for plants (avoid copy in function call)

