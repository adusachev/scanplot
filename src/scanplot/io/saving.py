import numpy as np


def dump_coords_csv(x: np.ndarray, y: np.ndarray, savepath: str) -> None:
    points = np.stack((x, y)).T
    np.savetxt(savepath, points, header="x, y")
