import sys

import cv2

# Module 1
sys.path.append("../video")

# Module 3
sys.path.append("../counting")

# Module 4
sys.path.append("../risk")

from video_source import VideoSource
from person_detector import PersonDetector
from person_counter import PersonCounter
from count_smoother import CountSmoother

from risk_config import RiskConfig
from risk_evaluator import RiskEvaluator
from risk_persistence import RiskPersistence


def main():

    if len(sys.argv) != 2:
        print(
            "Usage: python video_risk_test.py <video_path>"
        )
        return

    video_path = sys.argv[1]

    # -------------------------
    # Module 1
    # -------------------------

    source = VideoSource(
        source_id="video-01",
        source_path=video_path
    )

    # -------------------------
    # Module 2
    # -------------------------

    detector = PersonDetector(
        model_name="yolo26s.pt",
        confidence=0.25
    )

    # -------------------------
    # Module 3
    # -------------------------

    counter = PersonCounter()

    smoother = CountSmoother(
        window_size=5
    )

    # -------------------------
    # Module 4
    # -------------------------

    # These values are only for testing.
    config = RiskConfig(
        warning_threshold=20,
        critical_threshold=40
    )

    evaluator = RiskEvaluator(
        config
    )

    persistence = RiskPersistence(
        required_count=3
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

            # -------------------------
            # Module 1
            # -------------------------

            frame = source.read_frame()

            if frame is None:
                break

            # -------------------------
            # Module 2
            # -------------------------

            detections = detector.detect(
                frame.image
            )

            # -------------------------
            # Module 3
            # -------------------------

            raw_count = counter.count(
                detections
            )

            smoothed_count = smoother.update(
                raw_count
            )

            # -------------------------
            # Module 4
            # -------------------------

            raw_risk = evaluator.evaluate(
                smoothed_count
            )

            confirmed_risk, is_stable = (
                persistence.update(
                    raw_risk
                )
            )

            # -------------------------
            # Draw detections
            # -------------------------

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

            # -------------------------
            # Display information
            # -------------------------

            cv2.putText(
                frame.image,
                f"Raw count: {raw_count}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame.image,
                f"Smoothed count: {smoothed_count}",
                (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame.image,
                f"Risk: {confirmed_risk.value}",
                (20, 110),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 255, 255),
                2
            )

            if not is_stable:
                cv2.putText(
                    frame.image,
                    "Risk transition pending",
                    (20, 145),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 255),
                    2
                )

            cv2.putText(
                frame.image,
                f"Frame: {frame.frame_number}",
                (20, 180),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            # -------------------------
            # Resize for display
            # -------------------------

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
                "Nexa - Modules 1 to 4",
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