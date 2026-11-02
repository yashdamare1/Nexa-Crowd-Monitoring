from datetime import datetime

import cv2

from frame import Frame
from video_metadata import VideoMetadata


class VideoSource:
    """
    Reads frames from a video file.

    Module 1 is responsible only for video acquisition.
    """

    def __init__(
        self,
        source_id: str,
        source_path: str
    ):
        self.source_id = source_id
        self.source_path = source_path

        self.capture = None
        self.frame_number = 0

    def open(self) -> None:

        self.capture = cv2.VideoCapture(
            self.source_path
        )

        if not self.capture.isOpened():
            raise RuntimeError(
                f"Unable to open video: {self.source_path}"
            )

        self.frame_number = 0

    def read_frame(self) -> Frame | None:

        if self.capture is None:
            raise RuntimeError(
                "Video source is not open"
            )

        success, image = self.capture.read()

        if not success:
            return None

        frame = Frame(
            frame_number=self.frame_number,
            timestamp=datetime.now(),
            image=image
        )

        self.frame_number += 1

        return frame

    def get_metadata(self) -> VideoMetadata:

        if self.capture is None:
            raise RuntimeError(
                "Video source is not open"
            )

        return VideoMetadata(
            source_id=self.source_id,
            source_path=self.source_path,
            fps=self.capture.get(
                cv2.CAP_PROP_FPS
            ),
            width=int(
                self.capture.get(
                    cv2.CAP_PROP_FRAME_WIDTH
                )
            ),
            height=int(
                self.capture.get(
                    cv2.CAP_PROP_FRAME_HEIGHT
                )
            )
        )

    def close(self) -> None:

        if self.capture is not None:
            self.capture.release()

        self.capture = None