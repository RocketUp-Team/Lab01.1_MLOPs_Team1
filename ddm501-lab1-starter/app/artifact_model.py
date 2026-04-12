"""
Serializable collaborative filtering model artifact.

This module defines the classes that get pickled into models/svd_model.pkl.
Keep these classes stable: changing their names or module path will break
loading existing model files.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

import numpy as np


@dataclass(frozen=True)
class PredictionResult:
    """Mimics Surprise's Prediction object shape (only .est is needed)."""
    est: float


class MovieLensSVDModel:
    """
    Simple SVD-based collaborative filtering model.

    - Learns a low-rank approximation of the (user x item) rating matrix.
    - Uses global mean centering.
    - Handles unknown users/movies by returning the global mean.
    """

    def __init__(
        self,
        global_mean: float,
        user_factors: np.ndarray,
        item_factors: np.ndarray,
        user_id_to_index: Dict[str, int],
        movie_id_to_index: Dict[str, int],
        min_rating: float = 1.0,
        max_rating: float = 5.0,
    ) -> None:
        self.global_mean = float(global_mean)
        self.user_factors = np.asarray(user_factors, dtype=np.float32)
        self.item_factors = np.asarray(item_factors, dtype=np.float32)
        self.user_id_to_index = dict(user_id_to_index)
        self.movie_id_to_index = dict(movie_id_to_index)
        self.min_rating = float(min_rating)
        self.max_rating = float(max_rating)

    def _lookup(self, uid: str, iid: str) -> tuple[Optional[int], Optional[int]]:
        return self.user_id_to_index.get(uid), self.movie_id_to_index.get(iid)

    def predict(self, uid: str, iid: str) -> PredictionResult:
        uidx, iidx = self._lookup(uid, iid)
        if uidx is None or iidx is None:
            est = self.global_mean
        else:
            # Dot product in latent space + global mean.
            est = self.global_mean + float(np.dot(self.user_factors[uidx], self.item_factors[iidx]))

        # Clamp defensively.
        if est < self.min_rating:
            est = self.min_rating
        elif est > self.max_rating:
            est = self.max_rating

        return PredictionResult(est=est)

