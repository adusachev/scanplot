import os
from typing import Annotated, Literal, TypeAlias, TypeVar

import numpy as np
import numpy.typing as npt

PathLike: TypeAlias = str | os.PathLike[str]

DType = TypeVar("DType", bound=np.generic)

ArrayNxMx3 = Annotated[npt.NDArray[DType], Literal["N", "M", 3]]
ArrayNxM = Annotated[npt.NDArray[DType], Literal["N", "M"]]
ArrayNx2 = Annotated[npt.NDArray[DType], Literal["N", 2]]
ArrayN = Annotated[npt.NDArray[DType], Literal["N"]]

ImageLike: TypeAlias = ArrayNxMx3 | ArrayNxM
