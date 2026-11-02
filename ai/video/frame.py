from dataclasses import dataclass
from datetime import datetime

import numpy as np


@dataclass
class Frame:
    """
    Represents one video frame produced by Module 1.
    """

    frame_number: int
    timestamp: datetime
    image: np.ndarray

    @property
    def width(self) -> int:
        return self.image.shape[1]

    @property
    def height(self) -> int:
        return self.image.shape[0]