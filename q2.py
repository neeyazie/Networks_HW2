import networkx as nx
import matplotlib.pyplot as plt
import math

# Setting set of values of graph size and probabilities, as well as how often do we want to repeat graph creations for each set

n_p = [(1*(10**2), 0.67), (5*(10**2), 0.5), (1*(10**3), 0.2)]
# n_p = [(5, 0.5)]
repeat = 30

for n, p in n_p:
    # Setting up base values

    degree = 0
    cluster = 0
    path = 0
    divide = 0
    distribution = [0 for _ in range(n)]

    
    for _ in range(repeat):
        # Creating graph via networkx

        G = nx.erdos_renyi_graph(n, p)

        # Adding average degree of graph
        degree += (sum([i[1] for i in G.degree]) / n)

        # Adding cluster coefficient of graph
        cluster += (sum((nx.clustering(G, [i for i in range(n)])).values()) / n)

        # Adding average path length of graph
        paths = 0
        divide = 0

        for C in (G.subgraph(c).copy() for c in nx.connected_components(G)):
            paths += nx.average_shortest_path_length(C)
            divide += 1

        paths /= divide
        path += paths
        
        # Adding degree histogram of graph to distribution
        histogram = nx.degree_histogram(G)

        for i in range(len(histogram)):
            distribution[i] += histogram[i]

    # Finding out averages of each type of value
    degree /= repeat
    cluster /= repeat
    path /= repeat

    # Setting up axes of our graph
    x = [i for i in range(n)]
    for i in range(n):
        distribution[i] /= repeat
    y = distribution

    # Creating plot
    plt.figure(figsize=(10, 6))

    plt.plot(x, y)

    plt.xlabel("Degree Value")
    plt.ylabel("Average Number Of Nodes with Degree")
    plt.title(f"Degree Distribution Of Graph Size {n} And Probability {p}")

    # Calculating expected values of average degree, clustering coefficients and average path length
    k = (n - 1) * p
    cc = p
    d = (math.log10(n)/math.log10(k))

    # Printing values calculated on top right of graph
    text_str = f"Average Degree: {degree:.2f}\nExpected Average Degree: {k:.2f}\n\nClustering Coefficient: {cluster:.4f}\nExpected Clustering Coefficient: {cc:.4f}\n\nAverage Path Length: {path:.2f}\nExpected Average Path Length: {d:.2f}"
    plt.text(0.8 * n, max(y) * 0.7, text_str, fontsize=12, bbox=dict(facecolor='white', alpha=1))

    # Outputting plot into a separate png file
    output_file = f"{n}_{p}_graph.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Plot saved as '{output_file}'")