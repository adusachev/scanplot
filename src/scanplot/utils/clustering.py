import logging
from collections import defaultdict
from typing import List, Tuple

import cv2 as cv
import numpy as np
from scipy.ndimage import sobel
from sklearn.cluster import DBSCAN, AgglomerativeClustering, MeanShift

logger = logging.getLogger(__name__)


def agglomerative_clustering(points: np.ndarray, eps: float = 5.5) -> np.ndarray:
    """
    Run Agglomerative Clustering with distance treshold.
    Return array of cluster labels.
    """
    if len(points) == 1:
        labels_pred = np.zeros(1, dtype=np.int64)
        return labels_pred

    try:
        agglomerat = AgglomerativeClustering(n_clusters=None, distance_threshold=eps)
        labels_pred = agglomerat.fit_predict(points)
    except MemoryError as ex:
        logger.error(f"Number of points: {len(points)} too lot for clustering")
        raise Exception(f"Number of points: {len(points)} too lot for clustering")

    return labels_pred


def meanshift_clustering(points: np.ndarray, bandwidth: float = 4) -> np.ndarray:
    """
    Run Mean-Shift clustering with a given bandwidth.
    Return array of cluster labels.
    """
    mean_shift = MeanShift(bandwidth=bandwidth)
    labels_pred = mean_shift.fit_predict(points)
    return labels_pred


def dbscan_clustering(points: np.ndarray, eps: float, min_samples: int) -> np.ndarray:
    """
    Run DBSCAN clustering.
    Return array of cluster labels.
    """
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels_pred = dbscan.fit_predict(points)
    return labels_pred


def simplify_points(points: np.ndarray, labels_pred: np.ndarray) -> np.ndarray:
    """
    Take clustering result (labeled data) and return array with cluster centers.
    """
    unique_labels = np.unique(labels_pred)
    n = len(unique_labels)
    cluster_centers = np.zeros((n, 2))

    for i in range(len(unique_labels)):
        label = unique_labels[i]
        cluster_indexes = np.where(labels_pred == label)[0]
        cluster_points = points[cluster_indexes]
        cluster_centers[i] = np.mean(cluster_points, axis=0)

    return cluster_centers
