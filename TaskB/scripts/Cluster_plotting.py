import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import pandas as pd
import numpy as np



def plot_hist(ax: Axes, col_name: str, data: np.ndarray) -> None:
    ax.hist(data, rwidth = 0.8, bins = 1000, alpha = 1)
    ax.set_title(col_name)
    ax.set_xlabel(f"Value")
    ax.set_ylabel(f"Count")


def plot_two_columns(ax: Axes, col1_name: str, col2_name: str, col1_data: np.ndarray, col2_data: np.ndarray, alpha: float = 0.01) -> None:
    ax.scatter(col2_data, col1_data, marker = ".", alpha=alpha)
    ax.set_ylabel(col1_name)
    ax.set_xlabel(col2_name)
    ax.set_title(f"{col1_name[-1]} vs {col2_name[-1]}")


def plot_all_columns(df: pd.DataFrame, all_labels: pd.Series|None = None, sel_labels: list[int]|None = None, save_path: str|None = None) -> None:

    if all_labels is None and sel_labels is not None:
        raise ValueError(f"[plot_all_columns] {"all_labels"} should be provided when {"sel_labels"} are present!")

    fig, axs = plt.subplots(len(df.columns), len(df.columns), 
                            figsize=(6*len(df.columns), 6*len(df.columns)))

    for i, col1 in enumerate(df.columns):
        for j, col2 in enumerate(df.columns):
            if i == j:
                if sel_labels is not None and all_labels is not None:
                    for sel_lab in sel_labels:
                        plot_hist(axs[i][j], col1, df.loc[all_labels == sel_lab][col1].to_numpy())                  
                else:
                    plot_hist(axs[i][j], col1, df[col1].to_numpy())
            else:
                if sel_labels is not None and all_labels is not None:
                    for sel_lab in sel_labels:
                        plot_two_columns(
                            ax = axs[i][j],
                            col1_name=col1,
                            col2_name=col2,
                            col1_data=df.loc[all_labels == sel_lab][col1].to_numpy(),
                            col2_data=df.loc[all_labels == sel_lab][col2].to_numpy(),
                            alpha=0.005
                        )
                else:
                    plot_two_columns(
                    ax = axs[i][j],
                    col1_name=col1,
                    col2_name=col2,
                    col1_data=df[col1].to_numpy(),
                    col2_data=df[col2].to_numpy(),
                    alpha=0.005
                )


    fig.tight_layout()

    if save_path is not None:
        fig.savefig(save_path)