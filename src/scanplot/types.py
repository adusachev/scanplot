import os
from dataclasses import dataclass
from typing import Annotated, Literal, TypeAlias, TypeVar

import numpy as np
import numpy.typing as npt

PathLike: TypeAlias = str | os.PathLike[str]

DType = TypeVar("DType", bound=np.generic)

ArrayNxMx3 = Annotated[npt.NDArray[DType], Literal["N", "M", 3]]
ArrayNxM = Annotated[npt.NDArray[DType], Literal["N", "M"]]
ArrayNx2 = Annotated[npt.NDArray[DType], Literal["N", 2]]
ArrayNx3 = Annotated[npt.NDArray[DType], Literal["N", 3]]
ArrayN = Annotated[npt.NDArray[DType], Literal["N"]]

ImageLike: TypeAlias = ArrayNxMx3 | ArrayNxM


@dataclass
class ConverterParameters:
    x_min_px: int
    x_max_px: int
    y_min_px: int
    y_max_px: int
    x_min_factual: float
    x_max_factual: float
    y_min_factual: float
    y_max_factual: float
    x_axis_type: Literal["linear", "logscale"]
    y_axis_type: Literal["linear", "logscale"]
