import pandas as pd








def find_chains_top_std(
    df: pd.DataFrame,
    chains_depth: int = 5,
    top_n: int = 5,
    output_path: str = "erk_chains_top_std.parquet"
) -> None:
    
    erk_diff_cols = [f"ERK_diff_t{d}" for d in range(chains_depth)]

    base = (
        df[["ERK_neigh_diff"]]
        .reset_index()
        .rename(columns={
            df.index.names[0]: "image_T",
            df.index.names[1]: "track_id",
            df.index.names[2]: "neighbour_id",
        })
    )

    timepoints = sorted(base["image_T"].unique())
    first_chunk = True

    for t in timepoints[:-chains_depth]:
        t_window = timepoints[timepoints.index(t) : timepoints.index(t) + chains_depth + 1]
        window_df = base[base["image_T"].isin(t_window)].copy()
        edges = window_df.copy()

        # Buduj łańcuchy dla wszystkich tracków w t0
        chains = (
            window_df[window_df["image_T"] == t]
            .rename(columns={
                "track_id":       "track_id_t0",
                "neighbour_id":   "track_id_t1",
                "ERK_neigh_diff": "ERK_diff_t0",
            })
            .drop(columns="image_T")
            .assign(image_T=t)
        )

        for depth in range(1, chains_depth):
            next_edges = (
                edges[edges["image_T"] == timepoints[timepoints.index(t) + depth]]
                .rename(columns={
                    "track_id":       f"track_id_t{depth}",
                    "neighbour_id":   f"track_id_t{depth+1}",
                    "ERK_neigh_diff": f"ERK_diff_t{depth}",
                })
            )
            chains = chains.merge(
                next_edges[[f"track_id_t{depth}", f"track_id_t{depth+1}", f"ERK_diff_t{depth}"]],
                on=f"track_id_t{depth}",
                how="inner",
            )

        # Policz std wzdłuż łańcucha i wybierz top_n dla każdego track_id_t0
        chains["erk_std"] = chains[erk_diff_cols].std(axis=1)
        chains = (
            chains
            .sort_values("erk_std", ascending=False)
            .groupby("track_id_t0")
            .head(top_n)                        # top 5 per track_id
            .drop(columns="erk_std")
            .reset_index(drop=True)
        )

        # Posortuj kolumny
        col_order = ["image_T"]
        for d in range(chains_depth):
            col_order.append(f"track_id_t{d}")
            col_order.append(f"ERK_diff_t{d}")
        col_order.append(f"track_id_t{chains_depth}")
        chains = chains[col_order]

        # Zapis przyrostowy
        if first_chunk:
            chains.to_parquet(output_path, engine="fastparquet")
            first_chunk = False
        else:
            chains.to_parquet(output_path, engine="fastparquet", append=True)

        print(f"image_T={t}: {len(chains)} łańcuchów")

    print(f"Zapisano do {output_path}")