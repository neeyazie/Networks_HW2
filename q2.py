import networkx as nx
import matplotlib.pyplot as plt
import math

n_p = [(1*(10**2), 0.67), (5*(10**2), 0.5), (1*(10**3), 0.2)]
# n_p = [(5, 0.5)]


for n, p in n_p:
    degree = 0
    cluster = 0
    path = 0
    divide = 0

    distribution = [0 for _ in range(n)]

    repeat = 30
    for _ in range(repeat):
        G = nx.erdos_renyi_graph(n, p)

        degree += (sum([i[1] for i in G.degree]) / n)

        cluster += (sum((nx.clustering(G, [i for i in range(n)])).values()) / n)

        paths = 0
        divide = 0

        for C in (G.subgraph(c).copy() for c in nx.connected_components(G)):
            paths += nx.average_shortest_path_length(C)
            divide += 1

        # for i in range(n-1):
        #     for j in range(i, n):
        #         if nx.has_path(G, i, j):
        #             paths += nx.shortest_path_length(G, i, j)
        
        # paths /= (((n)*(n-1))//2)

        paths /= divide
        path += paths
        
        histogram = nx.degree_histogram(G)

        for i in range(len(histogram)):
            distribution[i] += histogram[i]

    degree /= repeat
    cluster /= repeat
    path /= repeat

    plt.figure(figsize=(10, 6))
    
    x = [i for i in range(n)]
    for i in range(n):
        distribution[i] /= repeat
    y = distribution

    plt.plot(x, y)

    plt.xlabel("Degree Value")
    plt.ylabel("Average Number Of Nodes with Degree")
    plt.title(f"Degree Distribution Of Graph Size {n} And Probability {p}")

    print(degree)
    print(cluster)
    print(path)

    k = (n - 1) * p
    cc = p
    d = (math.log10(n)/math.log10(k))

    text_str = f"Average Degree: {degree:.2f}\nExpected Average Degree: {k:.2f}\n\nClustering Coefficient: {cluster:.4f}\nExpected Clustering Coefficient: {cc:.4f}\n\nAverage Path Length: {path:.2f}\nExpected Average Path Length: {d:.2f}"
    plt.text(0.8 * n, max(y) * 0.7, text_str, fontsize=12, bbox=dict(facecolor='white', alpha=1))

    # Save the plot as a file
    output_file = f"{n}_{p}_graph.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')  # Save as high-quality image
    print(f"Plot saved as '{output_file}'")