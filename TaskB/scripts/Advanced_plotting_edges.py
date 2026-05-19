import pandas as pd
import networkx as nx
import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl





def save_frame(
        frame_idx: int, 
        df_with_edges: pd.DataFrame,
        df_with_stats: pd.DataFrame,
        path: str|None = None,
        experiment_idx = 1,
        site_idx = 1,
        tracked_ratio = "ERK",
    ) -> None:
    edges = df_with_edges.index.to_numpy()
    labels = df_with_edges.to_numpy()

    graph = nx.DiGraph()
    graph.add_edges_from(edges)
    edge_to_label: dict[tuple[int, int], int] = {}

    for edge, label in zip(edges, labels):
        edge_to_label[tuple(edge)] = label


    track_ids_from_stats = df_with_stats.index.to_numpy()
    points = df_with_stats[["objNuclei_Location_Center_X", "objNuclei_Location_Center_Y"]].to_numpy()

    cmap_for_edges = mpl.colormaps["Set1"]
    cmap_for_nodes = mpl.colormaps["coolwarm"]

    nodes_sizes = [50 for track_id, node_size in zip(track_ids_from_stats, df_with_stats["Nuclear_size"]) if track_id in set(graph.nodes)]
    nodes_colors = [cmap_for_nodes(node_color) for track_id, node_color in zip(track_ids_from_stats, df_with_stats["ERKKTR_ratio_scaled"]) if track_id in set(graph.nodes)]
    edges_colors = [cmap_for_edges(label) for label in labels]

    positions: dict[int, np.ndarray] = {
        track_id: position for track_id, position in zip(track_ids_from_stats, points) if track_id in set(graph.nodes)
    }

    fig, ax = plt.subplots(1, figsize = (12, 12))

    fig.suptitle(f"EXP: {experiment_idx}, SITE: {site_idx}\n{tracked_ratio} SCALED\n\n frame: {frame_idx}")

    nx.draw(
        graph,
        ax = ax,
        pos=positions,
        node_size=nodes_sizes,
        node_color=nodes_colors,
        connectionstyle="arc3,rad=0.15",
        arrowsize=5,
        edge_color=edges_colors,
        edgecolors='black'
    )

    fig.tight_layout()

    if path is not None:
        fig.savefig(path)
        plt.close()
    else:
        fig.show()

    del graph