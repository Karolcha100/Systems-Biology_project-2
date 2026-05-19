import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.axes import Axes
import numpy as np
import pandas as pd



def configure_selected_track_axis(ax: Axes, track_id: int, time_data: np.ndarray, y_data: np.ndarray, type: str = "") -> None:
    cmap = mpl.colormaps["coolwarm"]

    ax.set_title(f"{type} id: {track_id}")

    ax.plot(
        time_data, 
        y_data,
        ls = "--",
        color = f"C{0}",
        lw = 0.5,
        alpha = 0.75
    )


    ax.scatter(
        time_data, 
        y_data,
        c = cmap([erk_val for erk_val in y_data]),
        s = 10,
        alpha=1,
    )

    ax.grid(True)
    ax.set_xlabel(f"time")
    ax.set_ylabel(f"ERK")

    ax.set_xticks(np.arange(0, max(time_data) + 25, 25))



def plot_selected_tracks(df: pd.DataFrame, selected_track_ids: list[int], title: str, tracked_cols: tuple[str, str]) -> None:
    fig, axes = plt.subplots(2, len(selected_track_ids), figsize = (6*len(selected_track_ids), 5))

    fig.suptitle(title)

    time_data = df.index.get_level_values(0).unique().to_numpy()

    for ax_idx, track_idx in enumerate(selected_track_ids):
        configure_selected_track_axis(
            axes[0][ax_idx], 
            track_id=track_idx, 
            time_data=time_data,
            y_data=df.loc[(slice(None), track_idx), :][tracked_cols[0]].to_numpy(),
            type="Not Scaled"
        )
        configure_selected_track_axis(
            axes[1][ax_idx], 
            track_id=track_idx, 
            time_data=time_data,
            y_data=df.loc[(slice(None), track_idx), :][tracked_cols[1]].to_numpy(),
            type="Scaled"
        )

    fig.tight_layout()



def configure_frame_axis(
        ax: Axes, 
        x: np.ndarray, 
        y: np.ndarray, 
        sizes: np.ndarray, 
        colors,
        tracked_ratio: str, 
        alpha: float
    ) -> None:
    ax.scatter(
        x, 
        y, 
        s=sizes, 
        alpha = alpha,
        c = colors
    )

    ax.set_title(f"{tracked_ratio}")
    ax.set_xlabel(f"X")
    ax.set_ylabel(f"Y")

    ax.set_xlim(0-50, 1000+50)
    ax.set_ylim(0-50, 1000+50)


def plot_frame(
        frame_idx: int, 
        df: pd.DataFrame, 
        experiment_idx: int, 
        site_idx: int, 
        cols_names_XY: tuple[str, str],
        tracked_ratios: tuple[str, str],
        save_path: str|None = "../untracked/data/pics_for_gifs",
        cmap_name: str = "coolwarm",
    ) -> None:
    cmap = mpl.colormaps[cmap_name]

    fig, (ax_erk, ax_fox) = plt.subplots(1, 2, figsize = (22, 10))

    fig.suptitle(f"EXP: {experiment_idx}, SITE: {site_idx}, frame: {frame_idx}")

    X = df[cols_names_XY[0]].to_numpy()
    Y = df[cols_names_XY[1]].to_numpy()
    sizes = df.Nuclear_size.to_numpy()**1.5 / 750

    colors_ERK = [cmap(erk_val) for erk_val in df[tracked_ratios[0]]]
    colors_FOX = [cmap(fox_val) for fox_val in df[tracked_ratios[1]]]

    configure_frame_axis(
        ax_erk,
        X, 
        Y,
        sizes=sizes,
        tracked_ratio="ERK",
        alpha = 1,
        colors=colors_ERK,
    )

    configure_frame_axis(
        ax_fox,
        X, 
        Y,
        sizes=sizes,
        tracked_ratio="FOX",
        alpha = 1,
        colors=colors_FOX,
    )


    if save_path is not None:
        fig.savefig(f"{save_path}/frame_{frame_idx}")
        plt.close()

    
