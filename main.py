from functools import reduce
from random import randint


items = [
    {'weight': 3, "value" : 5},
    {'weight': 12, "value" : 9},
    {'weight': 8, "value" : 1},
    {'weight': 11, "value" : 14},
    {'weight': 10, "value" : 8},
    {'weight': 7, "value" : 12},
    {'weight': 6, "value" : 5},
    {'weight': 2, "value" : 6},
    {'weight': 14, "value" : 3},
    {'weight': 2, "value" : 7},
]

populationNb = 20
iterations = 2
currentIteration = 0
crossingProbability = 0.8
muattionProbability = 0.1
maxBackpackCapacityWeight = 53

def generateGenom():
    return [randint(0, 2, 1).tolist() for _ in range(len(items))]
    
def crossover():
    pass    

def mutation(genom):
    pass

def getValueAndWeight(genom):
    indexesList = []
    
    def filterIndexes(element, index):
        if element == 1:
            indexesList.append(index)
            
    def getWeight(element):
        return element['weight']

    def getValue(element):
        return element['value']
            
    genom.forEach(lambda el, index: filterIndexes(el, index))
    generalValue = reduce(lambda sumArr, element: [sumArr[0] + getWeight(items[element]), sumArr[1] + getValue(items[element])], indexesList, [])
    print(f"Value: {generalValue[1]}, weight: {generalValue[0]}")
    return generalValue
    
def evaluateGenom(genom):
    [weight, value] = getValueAndWeight(genom)
    return value//maxBackpackCapacityWeight if weight >= 0 and weight <= maxBackpackCapacityWeight else 0
        
def main():
    genoms = generateGenom()
    while currentIteration <= iterations:
        genoms.forEach(lambda genom: getValueAndWeight(genom))
        currentIteration += 1






