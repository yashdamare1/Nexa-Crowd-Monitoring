import sys

import cv2

# Allow Python to find Module 1 files
sys.path.append("../video")

from video_source import VideoSource
from person_detector import PersonDetector


def main():

    if len(sys.argv) != 2:
        print("Usage: python video_detection_test.py <video_path>")
        return

    video_path = sys.argv[1]

    source = VideoSource(
        source_id="video-01",
        source_path=video_path
    )

    detector = PersonDetector(
        model_name="yolo26s.pt",
        confidence=0.25
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

            detections = detector.detect(
                frame.image
            )

            for detection in detections:

                x1 = detection["x1"]
                y1 = detection["y1"]
                x2 = detection["x2"]
                y2 = detection["y2"]

                confidence = detection["confidence"]

                cv2.rectangle(
                    frame.image,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame.image,
                    f"person {confidence:.2f}",
                    (x1, y1 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

            # Display the current detection count.
            cv2.putText(
                frame.image,
                f"People detected: {len(detections)}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            # Display frame number.
            cv2.putText(
                frame.image,
                f"Frame: {frame.frame_number}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            # Resize only for display.
            display_width = 1200

            height, width = frame.image.shape[:2]

            scale = display_width / width

            display_height = int(
                height * scale
            )

            display_image = cv2.resize(
                frame.image,
                (display_width, display_height)
            )

            cv2.imshow(
                "Nexa - Module 1 + Module 2",
                display_image
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