from random import randrange, shuffle,randint

# __init
popSize = 50

fitness = []

nextPopulation = []

distance=[]

def generateRandomGenom():
    '''
    :return: Generated random gens for our chroms in population
    '''
    genom = []
    for i in range(0, genLength):
        genom.append(i)
    shuffle(genom)
    return genom

def getPopulation():
    '''
    :return: Population generated
    '''
    population = []
    for i in range(1, popSize):
        population.append(generateRandomGenom())
    return population

def generateDistance():
    '''

    :return: Generated distance ,depends on user input(towns)
    '''
    for i in range(0, genLength):
        for j in range (0, genLength):
         if (i != j):
             distance[i][j] = randint(1, 20)
             distance[j][i] = distance[i][j]
    return distance

def calculateTour(genes):
    '''

    :param genes: Takes the value of each gene so we can calculate gene[i] + gene[i+1]
    :return: The score which is the sum of a chromosome distance
    '''
    score = 0
    for i in range(genLength):
        if i != genLength-1:
            score = score + distance[genes[i]][genes[i + 1]]
        elif(i == genLength-1):
            score = score + distance[genes[i]][genes[0]] #A,..,D -> A (Get the distance from last gene to first gene
    return score

def getfitness():
    '''
    EVALUATE
    f(x) = 1/d Fitness Function
    :return:  Array of our popylation fitnesses
    '''

    for chrom in pop:
        fitness.append((1 / float(calculateTour(chrom))))
    return fitness

def TournamentSelection(currPop,genNum):
    '''
    :param currPop: Current population depends on the genNum
    :param genNum: Number of the generation

    TournamentSelection,randomly select three chroms from population
    and get the best ,depends on its fitness.Select three more and get
    the best from them.When matingArray contains nmod2 = 0 parents
    mate the last two to get the offspring that will be added in the next
    generation.
    '''
    matingArray=[]
    nextGenpop = 0
    while(nextGenpop !=49 ):

        #Two Competitors

        randd = randint(0,len(currPop)-1)
        randd1 = randint(0,len(currPop)-1)
        randd2 = randint(0,len(currPop)-1)

        maxx = max(fitness[randd],fitness[randd1],fitness[randd2])

        if(maxx == fitness[randd]):
            currentparent = randd
        elif(maxx == fitness[randd1]):
            currentparent = randd1
        else:
            currentparent = randd2

        matingArray.append(currentparent)

        #Check which method of crossover to use

        if(len(matingArray)%2 == 0):
            if(inpCrossoverMethod == 1):
                Mating(matingArray[-2:],genNum) #get the last two parents
                nextGenpop+=1
            else:
                PMX(matingArray[-2:],genNum)
                nextGenpop += 1

def getMutProb(gen):
    '''
    :param gen: Current generation
    :return: 1 <= x <= 100
    '''
    return -99.0 / 50.0 * gen + 100

def PMX(parents,genNum):
    '''
    1.Randomly select a swath of alleles from parent 1 and copy them directly to the child. Note the indexes of the segment.
    2.Looking in the same segment positions in parent 2, select each value that hasn't already been copied to the child.
        A.For each of these values:
        2i.Note the index of this value in Parent 2. Locate the value, V, from parent 1 in this same position.
        2ii.Locate this same value in parent 2.
        2iii.If the index of this value in Parent 2 is part of the original swath, go to step i. using this value.
        2iv.If the position isn't part of the original swath, insert Step A's value into the child in this position.
    3.Copy any remaining positions from parent 2 to the child.

    :param parents: An array of 2 numbers pointing at the index of population than shows which parents selected to mate
    :param genNum: Generation number
    '''
    print("Parents selected for mating", parents)
    gen1 = pop[parents[0]]
    gen2 = pop[parents[1]]

    #Pick 2 points for swath

    point1 = randint(0, genLength-1)
    point2 = randint(0, genLength - 2)

    if point2 >= point1:
        point2 += 1
    else:  # Swap the two cx points
        point1, point2 = point2, point1

    #_init offspring full of Nulls so we can check whether its value is empty

    offspring=[None]*genLength

    #Copy swath from parent1 to offspring

    for i in range(point1,point2+1):
        offspring[i]= gen1[i]

    #Swath of parent2

    swath2 = gen2[point1:point2+1]

    notCoppied = []

    #1. / 2.

    for i in range(len(swath2)):
        if(not(swath2[i] in offspring)):
            notCoppied.append(swath2[i])

    if(len(notCoppied)!=0):
        value = notCoppied[0]
    while(not len(notCoppied) == 0):

        if(len(notCoppied) == 1):
            if(offspring.count(None) == 1):
                id = offspring.index(None)
                offspring[id]=notCoppied[0]
                break

        # A.
        #2i.

        indexOfValue= gen2.index(value)

        #2ii.

        valueParent1 = gen1[indexOfValue]


        indexofvalueParent2 = gen2.index(valueParent1)

        valueInparent2 = gen2[indexofvalueParent2]

        #2iii./2iv.

        if(offspring[indexofvalueParent2] is None):
            offspring[indexofvalueParent2] = notCoppied[0]
            notCoppied.remove(notCoppied[0])
            if(len(notCoppied)!=0):
                value = notCoppied[0]
        else:
            value = valueInparent2

    #3.
    if(None in offspring):

        for i in range(len(offspring)):
            if (offspring[i] is None):
                offspring[i] = gen2[i]

    #Mutation

    swap1 = randrange(0, len(offspring))
    swap2 = randrange(0, len(offspring))
    isMutation = randrange(0, 1000)
    if (isMutation < getMutProb(genNum * 100)):
        print("Mutation")
        glass = offspring[swap1]
        offspring[swap1] = offspring[swap2]
        offspring[swap2] = glass

    nextPopulation.append(offspring)

    print("The offspring after crossover:", offspring)

def Mating(parents,genNum):
    '''
    Two-point crossover calls for two points to be selected on the parent organism strings.
    Everything between the two points is swapped between the parent organisms, rendering two child organisms

    :param parents: An array of 2 numbers pointing at the index of population than shows which parents selected to mate
    :param genNum: Generation number
    '''
    print("Parents selected for mating",parents)
    gen1 = pop[parents[0]]
    gen2 = pop[parents[1]]

    temp1 = gen1[:]
    temp2 = gen2[:]

    point = randrange(0, genLength-1)

    #Copy start-> point from parent1 to offspring
    offspring = temp1[0:point]
        #remove values already coppied to offspiring from parent2
    for i in offspring:
        temp2.remove(i)

    point = randrange(0, genLength-1)

    #Copy start-> point from parent2 to offspring
    for i in temp2[0:point]:
        offspring.append(i)
        # remove values already coppied to offspiring from parent1
    for i in offspring:
        temp1.remove(i)

    #Copy last values from parent1 to offspring
    for i in temp1:
        offspring.append(i)

    #Mutation
    swap1 = randrange(0, len(offspring))
    swap2 = randrange(0, len(offspring))
    isMutation = randrange(0, 1000)
    if (isMutation < getMutProb(genNum * 100)):
        print("Mutation")
        glass = offspring[swap1]
        offspring[swap1] = offspring[swap2]
        offspring[swap2] = glass

    nextPopulation.append(offspring)
    print("The offspring after crossover:", offspring)

def modifyValues(fit):
    '''
    Modify array values.isdigit to str
    :param fit: Array of fittest chrom
    :return: Array of fittest chrom contains letters instead of numbers
    '''
    for i, x in enumerate(fit):
        if x == 0:
            fit[i] = 'A'
        elif x == 1:
            fit[i] = 'B'
        elif x == 2:
            fit[i] = 'C'
        elif x == 3:
            fit[i] = 'D'
        elif x == 4:
            fit[i] = 'E'
        elif x == 5:
            fit[i] = 'F'
        elif x == 6:
            fit[i] = 'G'
        elif x == 7:
            fit[i] = 'H'
        elif x == 8:
            fit[i] = 'I'
        elif x == 9:
            fit[i] = 'G'
    return fit

def bestSoFar(pop,genNum):
    '''
    After each generation ,save fittest chrom so far
    :param pop: Current population
    :param genNum: Current generation
    '''
    global bestChromFitness
    global  bestChrom
    global bestGen

    for i in range(len(pop)):
        if (fitness[i] > bestChromFitness):
            bestChrom = pop[i]
            bestChromFitness = fitness[i]
            bestGen = genNum

#Genetic Algorithm

bestChromFitness =0
bestChrom = []
bestGen = 0

inp = "no digit"

inpCrossoverMethod = "no digit"

while(not inp.isdigit()):
    inp = input('Press 1 for project pattern,or random number for random pattern:')
inp =int(inp)

if(inp == 1):
    distance = [[0, 4, 4, 7, 3], [4, 0, 2, 3, 5], [4, 2, 0, 2, 3], [7, 3, 2, 0, 6], [3, 5, 3, 6, 0]]
    genLength = 5
else:
    while(True):
        try:
            genLength = int(input('Enter the number of cities: '))
            break
        except ValueError:
            print("Pick a number.")

    distance = [[0 for x in range(genLength)] for y in range(genLength)]
    generateDistance()

while(not inpCrossoverMethod.isdigit()):
    inpCrossoverMethod = input('Press 1 for TwoPoint Crossover Method or 2 for PMX Method:')
inpCrossoverMethod = int(inpCrossoverMethod)

#:Generate population:
print("Creating inital population...")

pop = getPopulation()

generations = 0

while (generations < 50): #:Terminal criteria:

    print("Current generation", generations , "with a population of" , len(pop)+1 , "chromosomes")

    getfitness()  # Get fitness for each chromosome in Population

    TournamentSelection(pop,generations)  # Selecting parents

    bestSoFar(pop, generations)

    pop = nextPopulation

    print("Current Population", pop)

    generations+=1

    fitness = []

    getfitness()

    nextPopulation = []

tour = calculateTour(bestChrom)

print("Distance between towns:")
for d in distance:
    print(d)

print("The fittest chromosome found in the Generation:",bestGen,"Best Chromosome", modifyValues(bestChrom), "with distance of", tour,".")