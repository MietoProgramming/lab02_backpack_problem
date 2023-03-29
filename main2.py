import random
import matplotlib.pyplot as plt
import numpy as np

items = [
    {'weight': 3, "value": 5},
    {'weight': 12, "value": 9},
    {'weight': 8, "value": 1},
    {'weight': 11, "value": 14},
    {'weight': 10, "value": 8},
    {'weight': 7, "value": 12},
    {'weight': 6, "value": 5},
    {'weight': 2, "value": 6},
    {'weight': 14, "value": 3},
    {'weight': 2, "value": 7},
]

populationNb = 20
iterations = 2
crossingProbability = 0.8
mutationProbability = 0.1
maxBackpackCapacityWeight = 53


def generateGenom():
    return [random.randint(0, 1) for _ in range(len(items))]


def crossover(parentGenom1, parentGenom2):
    child = []
    for i in range(len(parentGenom1)):
        if random.random() < crossingProbability:
            child.append(parentGenom1[i])
        else:
            child.append(parentGenom2[i])
    return child


def getWeightAndValue(genom):
    total_weight = 0
    total_value = 0
    for i in range(len(genom)):
        if genom[i] == 1:
            total_weight += items[i]['weight']
            total_value += items[i]['value']
    if total_weight > maxBackpackCapacityWeight:
        return (0, total_weight)
    else:
        return (total_value, total_weight)


def mutation(genom):
    for i in range(len(genom)):
        if random.random() < mutationProbability:
            genom[i] = 1 - genom[i]
    return genom


def generateTable(items, genomstable):
    num_items = len(items)
    table1 = np.zeros((populationNb + 3, num_items), dtype=int)

    # First table
    # First row: Numbers of items
    table1[0] = np.arange(1, num_items+1)

    # Second row: Weight for item
    table1[1] = [item["weight"] for item in items]

    # Third row: Value for item
    table1[2] = [item["value"] for item in items]

    # Remaining rows: 0 or 1 depending on random generated list from genoms
    for i in range(3, populationNb+3):
        for j in range(num_items):
            table1[i][j] = genomstable[i-3][j]

    return table1


def main():
    genoms2 = []
    best_values = []
    avg_values = []
    iterationCopies = []
    plotGenomValues = []
    genoms = [generateGenom() for _ in range(populationNb)]
    genoms1 = genoms
    for iteration in range(iterations):
        genomsValues = []
        genomsWeights = []
        for (value, weight) in [getWeightAndValue(genom) for genom in genoms]:
            genomsValues.append(value)
            genomsWeights.append(weight)
        iterationCopies.append(
            {'genoms': genoms, 'values': genomsValues, 'weights': genomsWeights})
        parents = random.choices(genoms, weights=genomsValues, k=2)
        children = []
        for _ in range(populationNb):
            parents = random.choices(genoms, weights=genomsValues, k=2)
            children.append(mutation(crossover(parents[0], parents[1])))
        genoms = children
        genoms2 = children
        best_values.append(max(genomsValues))
        avg_values.append(sum(genomsValues) / len(genomsValues))
        plotGenomValues.append(genomsValues)
        print(genoms2)
        print("values")
        print(genomsValues)
        print('Weights')
        print(genomsWeights)
        
    iterationsArr = range(iterations)
    # Create a figure with a 3x2 grid of subplots
    fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(15, 10))
    plt.subplots_adjust(left=None, bottom=None, right=None,
                        top=0.9, wspace=0.3, hspace=0.5)

    table1 = generateTable(items, genoms1)
    table2 = generateTable(items, genoms2)
    
    rows = ['No', 'Weight', 'Value']
    numbers = [i for i in range(1, 21)]
    rows += numbers

    # TABLE 1
    axs[0, 0].axis('off')
    table = axs[0, 0].table(cellText=table1, cellLoc='center',
                            loc='center', rowLabels=rows)
    # Format the first column
    for i in range(0, 23):
        cell = table[i, -1].get_text()
        cell.set_fontweight('bold')
    # Format the first three rows
    for j in range(3):
        for i in range(10):
            cell = table[j, i].get_text()
            cell.set_fontweight('bold')

    # TABLE 2
    axs[0, 1].axis('off')
    table = axs[0, 1].table(cellText=table2, cellLoc='center',
                            loc='center', rowLabels=rows)
    # Format the first column
    for i in range(0, 23):
        cell = table[i, -1].get_text()
        cell.set_fontweight('bold')
    # Format the first three rows
    for j in range(3):
        for i in range(10):
            cell = table[j, i].get_text()
            cell.set_fontweight('bold')

    # Create the third subplot by merging the last column of the first row
    # with the entire second row
    axs[0, 2].axis('off')
    axs[0, 2].set_visible(False)

    axs[1, 2].axhline(y=max(best_values), xmin=0, xmax=0.95, color='gray', linestyle="dashed", linewidth=1, label=max(best_values))
    axs[1, 2].plot(iterationsArr, best_values, label='Best')
    axs[1, 2].plot(iterationsArr, avg_values, label='Average')
    axs[1, 2].set_position([0.7, 0.35, 0.228, 0.343])
    plt.xlabel('Generation')
    plt.ylabel('Values')
    plt.title('Evolution of genoms using Genetic Algorithm')
    plt.legend()

    #wartość z pierwszej i drugiej generacji
    plot1 = plotGenomValues[0]
    plot2 = plotGenomValues[1]

    # Create the fourth and fifth subplots in the second row
    axs[1, 0].set_title("1 st. generation roulette")
    axs[1, 0].pie(plot1, labels=[f"{(genom/sum(plot1))*100:.2f}%" for genom in plot1])
    axs[1, 1].set_title("2 nd. generation roulette")
    axs[1, 1].pie(plot2, labels=[f"{(genom/sum(plot2))*100:.2f}%" for genom in plot2])

    plt.show()


main()