import matplotlib.pyplot as plt
import numpy as np

from typing import Union
from strenum import StrEnum

# Set style for matplotlib
plt.style.use("ggplot")

# Default parameters
block_height = 4
block_width = 6
plot_color = "forestgreen"
darker_color = "green"
hist_bins = 30
hist_range = (0, 5)


# Classes and Enums
class ShapeMismatchError(Exception):
    pass


class AxisNames(StrEnum):
    X = "X"
    Y = "Y"


class DiagramTypes(StrEnum):
    Violin = "v"
    Hist = "h"
    Boxplot = "b"


# Functions
def visualize_distribution(
    points: np.ndarray,
    diagram_type: Union[DiagramTypes, list[DiagramTypes]],
    diagram_axis: Union[AxisNames, list[AxisNames]],
    path_to_save: str = "",
) -> None:
    validate_distribution(points, diagram_type, diagram_axis)

    abscissa, ordinates = points.T
    diagrams = diagram_type if isinstance(diagram_type, list) else [diagram_type]
    axes = diagram_axis if isinstance(diagram_axis, list) else [diagram_axis]

    ncols = len(axes)
    nrows = len(diagrams)

    figure = plt.figure(figsize=(ncols * block_width, nrows * block_height))
    gridspec = plt.GridSpec(nrows, ncols, figure=figure)

    for i, diagram in enumerate(diagrams):
        for j, axisName in enumerate(axes):
            data = abscissa if axisName == AxisNames.X else ordinates
            axis = figure.add_subplot(gridspec[i, j])
            match diagram:
                case DiagramTypes.Violin:
                    violin = axis.violinplot(
                        data,
                        vert=False,
                        showmedians=True,
                    )
                    for body in violin["bodies"]:
                        body.set_facecolor(plot_color)
                        body.set_edgecolor(darker_color)
                    for part in ("cmins", "cmaxes", "cmedians", "cbars"):
                        plt.setp(violin[part], color=darker_color, linewidth=1)
                case DiagramTypes.Hist:
                    axis.hist(
                        data,
                        bins=hist_bins,
                        color=plot_color,
                        density=True,
                        alpha=0.5,
                        range=None if not hist_range else hist_range
                    )
                case DiagramTypes.Boxplot:
                    axis.boxplot(
                        data,
                        vert=False,
                        patch_artist=True,
                        boxprops=dict(facecolor="#83B783"),
                        medianprops=dict(color="forestgreen"),
                    )
                    data_min, data_max = axis.get_xlim()
                    xticks = np.round(np.arange(data_min, data_max + 1e-6, 0.5), 1)
                    axis.set_xticks(xticks)
                    axis.set_yticks([])
                case _:
                    raise ValueError("Invalid diagram type")
            if i == 0:
                axis.set_title(axisName.value)

    plt.tight_layout()
    if path_to_save:
        figure.savefig(path_to_save)

    plt.show()


# Function which validate 'visualize_distribution' parameters
def validate_distribution(
    points: np.ndarray,
    diagram_type: Union[DiagramTypes, list[DiagramTypes]],
    diagram_axis: Union[AxisNames, list[AxisNames]],
) -> None:
    validate_types = (
        isinstance(diagram_type, DiagramTypes)
        or (
            isinstance(diagram_type, list) and
            all(isinstance(diagtype, DiagramTypes) for diagtype in diagram_type)
        )
    )
    validate_axes = (
        isinstance(diagram_axis, AxisNames)
        or (
            isinstance(diagram_axis, list) and
            all(isinstance(axis, AxisNames) for axis in diagram_axis)
        )
    )

    if not validate_types:
        raise TypeError("Diagram type should be DiagramTypes enum member or list of DiagramTypes")
    if not validate_axes:
        raise TypeError("Diagram axis should be AxisNames enum member or list of AxisNames")
    if not isinstance(points, np.ndarray):
        raise TypeError("Invalid type of points")

    abscissa, ordinates = points.T
    if abscissa.size != ordinates.size:
        raise ShapeMismatchError("The abscissa and ordinates must have the same size")
    if (abscissa.ndim != 1) and (abscissa.ndim != ordinates.ndim):
        raise ValueError("The abscissa and ordinates must be one-dimensional arrays")


# Setters for parameters
def set_blockheight(height: int) -> None:
    global block_height
    if isinstance(height, int):
        block_height = height
    else:
        raise ValueError("Figure block height must be integer")


def set_blockwidth(width: int) -> None:
    global block_width
    if isinstance(width, int):
        block_width = width
    else:
        raise ValueError("Figure block width must be integer")


def set_plotcolor(color: str) -> None:
    global plot_color
    if isinstance(color, str):
        plot_color = color
    else:
        raise ValueError("Color should be string")


def set_histbins(bins: int) -> None:
    global hist_bins
    if isinstance(bins, int):
        hist_bins = bins
    else:
        raise ValueError("Bins count must be integer")
    
def set_range(range: tuple) -> None:
    global hist_range
    if isinstance(range, tuple):
        hist_range = range
    else:
        raise ValueError("Range count must be tuple")
