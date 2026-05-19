from sklearn.metrics import davies_bouldin_score, calinski_harabasz_score
import pandas as pd








def clustering_coverage_stats(tested_df: pd.DataFrame) -> None:
    print(
    f"""
    Nodes with Labels:\t\t\t\t{sum(sum(tested_df["label"] == lab_idx) for lab_idx in tested_df["label"].unique() if lab_idx != -1)}
    Nodes without Labels:\t\t\t{sum(tested_df["label"] == -1)}
    Nodes ratio [with label / all]:\t\t{sum(sum(tested_df["label"] == lab_idx) for lab_idx in tested_df["label"].unique() if lab_idx != -1)} / {len(tested_df)}
    Nodes ratio [with label / all][%]:\t\t{sum(sum(tested_df["label"] == lab_idx) for lab_idx in tested_df["label"].unique() if lab_idx != -1) / len(tested_df) * 100:.2f}%
    Noise [without label / all][%]:\t\t{sum(tested_df["label"] == -1) / len(tested_df) * 100:.2f}%
    """)



def run_scoring(df: pd.DataFrame) -> dict[str, float]:    
    scores_func_dict: dict = {
        f"Davies-Bouldin Score": davies_bouldin_score,
        f"Calinski-Harabasz Score": calinski_harabasz_score,
    }

    only_clustered_df: pd.DataFrame = df[df["label"] != -1]
    df_without_labels: pd.DataFrame = only_clustered_df.drop(columns=["label"])

    labels = only_clustered_df["label"]

    scores = {score_name: func(df_without_labels, labels) for score_name, func in scores_func_dict.items()}

    for scoring_func_name, score_value in scores.items():
        print(f"{f"{scoring_func_name}:":<40}{score_value:.3f}")

    return scores