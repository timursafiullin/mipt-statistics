import numpy as np

from typing import Any, Callable


def get_boxplot_outliers(
    data: np.ndarray,
    key: Callable[[Any], Any]
) -> np.ndarray:
    if len(data) == 0:
        raise ValueError("Empty array given")

    values = np.array([key(x) for x in data])

    if values.size == 0:
        return np.array([], dtype=int)

    q1 = np.percentile(values, 25)
    q3 = np.percentile(values, 75)
    eps = (q3 - q1) * 1.5
    lower, upper = q1 - eps, q3 + eps

    mask_outliers = (values < lower) | (values > upper)
    return np.nonzero(mask_outliers)[0]
