import sys

import cv2

from video_source import VideoSource


def main():

    if len(sys.argv) != 2:
        print("Usage: python main.py <video_path>")
        return

    video_path = sys.argv[1]

    source = VideoSource(
    source_id="video-01",
    source_path=video_path
)

    try:
        source.open()

        metadata = source.get_metadata()

        print("Video opened successfully")
        print(f"Source ID: {metadata.source_id}")
        print(f"FPS: {metadata.fps}")
        print(
            f"Resolution: "
            f"{metadata.width}x"
            f"{metadata.height}"
        )

        while True:

            frame = source.read_frame()

            if frame is None:
                break

            cv2.putText(
                frame.image,
                f"Frame: {frame.frame_number}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            cv2.imshow(
                "Nexa - Module 1",
                frame.image
            )

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

    finally:
        source.close()
        cv2.destroyAllWindows()

        print("Video source closed")


if __name__ == "__main__":
    main()