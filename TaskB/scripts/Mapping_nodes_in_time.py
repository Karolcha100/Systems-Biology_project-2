import networkx as nx
import pickle








def calculate_self_node_stats(
        nodeA: dict[str, float], 
        nodeB: dict[str, float], 
        ERK_ratio_name: str|None = "ERKKTR_ratio_scaled",
        FOX_ratio_name: str|None = None,
    ) -> dict[str, float]:

    stats: dict[str, float] = {}
    
    if ERK_ratio_name is not None:
        stats.update(
            {
                "ERK_t0": nodeA[ERK_ratio_name],
                "ERK_t1": nodeB[ERK_ratio_name],
                "ERK_diff": nodeB[ERK_ratio_name] - nodeA[ERK_ratio_name]
            }
        )

    if FOX_ratio_name is not None:
        stats.update(
            {
                "FOX_t0": nodeA[FOX_ratio_name],
                "FOX_t1": nodeB[FOX_ratio_name],
                "FOX_diff": nodeB[FOX_ratio_name] - nodeA[FOX_ratio_name]
            }
        )

    return stats



def calculate_stats_between_nodes(
        statsA: dict[str, float], 
        statsB: dict[str, float], 
        used_ratios: list[str],
        stats_types: list[str]) -> dict[str, float]:
    stats_dict: dict[str, float] = {}

    for ratio in used_ratios:
        for stat_type in stats_types:
            stats_dict[f"{ratio}_me_{stat_type}"] = statsA[f"{ratio}_{stat_type}"]
            stats_dict[f"{ratio}_neigh_{stat_type}"] = statsB[f"{ratio}_{stat_type}"]

    return stats_dict



def calculate_tracks_on_graphs(
        image_T: int, 
        path_to_graphs: str,
        used_ratios: list[str] = ["ERK"],
        stats_types: list[str] = ["diff"]
        ) -> dict[int, dict[int, dict[str, float]]]:
    """
    # TODO: Add selecting ratios names in input
    """
    graphA: nx.Graph
    graphB: nx.Graph

    with open(f"{path_to_graphs}/{image_T}.pickle", "rb") as file:
        graphA = pickle.load(file)

    with open(f"{path_to_graphs}/{image_T+1}.pickle", "rb") as file:
        graphB = pickle.load(file)

    nodes_in_both_graphs: set[int] = set(graphA.nodes) & set(graphB.nodes)


    self_nodes_stats: dict[int, dict[str, float]] = {}

    for node in nodes_in_both_graphs:
        self_nodes_stats[node] = calculate_self_node_stats(graphA.nodes[node], graphB.nodes[node])

    
    nodeA_to_nodeB_to_stats: dict[int, dict[int, dict[str, float]]] = {}

    for nodeA in graphA.nodes:
        if nodeA in nodes_in_both_graphs:
            nodeA_to_nodeB_to_stats[nodeA] = {}
            for nodeB in graphA.neighbors(nodeA):
                if nodeB in nodes_in_both_graphs:
                    nodeA_to_nodeB_to_stats[nodeA][nodeB] = calculate_stats_between_nodes(
                        self_nodes_stats[nodeA],
                        self_nodes_stats[nodeB],
                        stats_types=stats_types,
                        used_ratios=used_ratios
                    )

    return nodeA_to_nodeB_to_stats