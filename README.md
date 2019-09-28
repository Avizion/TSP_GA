Travel salesman problem solver with genetic algorithm.

Fitness Function :
                    f(x) = 1/d 
                    
User tournament selection.

TournamentSelection,randomly select three chroms from population
and get the best ,depends on its fitness.Select three more and get
the best from them.When matingArray contains nmod2 = 0 parents
mate the last two to get the offspring that will be added in the next
generation.


User PMX and two point crossover to generate offsprings.

PMX:
    1.Randomly select a swath of alleles from parent 1 and copy them directly to the child. Note the indexes of the segment.
    2.Looking in the same segment positions in parent 2, select each value that hasn't already been copied to the child.
        A.For each of these values:
        2i.Note the index of this value in Parent 2. Locate the value, V, from parent 1 in this same position.
        2ii.Locate this same value in parent 2.
        2iii.If the index of this value in Parent 2 is part of the original swath, go to step i. using this value.
        2iv.If the position isn't part of the original swath, insert Step A's value into the child in this position.
    3.Copy any remaining positions from parent 2 to the child.
    
Two-point crossover:
    Two-point crossover calls for two points to be selected on the parent organism strings.
    Everything between the two points is swapped between the parent organisms, rendering two child organisms.

