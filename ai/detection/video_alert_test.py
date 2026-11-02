
import sys
import os
import time
import cv2

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(BASE_DIR, "..", "video"))
sys.path.append(os.path.join(BASE_DIR, "..", "counting"))
sys.path.append(os.path.join(BASE_DIR, "..", "risk"))
sys.path.append(os.path.join(BASE_DIR, "..", "alerts"))

from backend_client import NexaBackendClient
from video_source import VideoSource
from person_detector import PersonDetector
from person_counter import PersonCounter
from count_smoother import CountSmoother
from risk_config import RiskConfig
from risk_evaluator import RiskEvaluator
from risk_persistence import RiskPersistence
from alert_engine import AlertEngine


def main():
    if len(sys.argv) != 2:
        print("Usage: python video_alert_test.py <video_path>")
        return

    video_path = sys.argv[1]

    backend = NexaBackendClient()
    backend.login()

    last_backend_update = 0.0
    latest_count = 0
    latest_risk = "NORMAL"
    source_id = "video-01"

    source = VideoSource(
        source_id=source_id,
        source_path=video_path
    )

    detector = PersonDetector(
        model_name="yolo26s.pt",
        confidence=0.25
    )

    counter = PersonCounter()
    smoother = CountSmoother(window_size=5)

    config = RiskConfig(
        warning_threshold=20,
        critical_threshold=40
    )

    evaluator = RiskEvaluator(config)

    persistence = RiskPersistence(
        escalation_count=15,
        recovery_count=90
    )

    alert_engine = AlertEngine()

    try:
        source.open()
        metadata = source.get_metadata()
        source_id = metadata.source_id

        print("Video opened successfully")
        print(f"Source ID: {source_id}")
        print(f"FPS: {metadata.fps}")
        print(f"Resolution: {metadata.width}x{metadata.height}")

        while True:
            frame = source.read_frame()

            if frame is None:
                break

            detections = detector.detect(frame.image)

            raw_count = counter.count(detections)
            smoothed_count = smoother.update(raw_count)

            raw_risk = evaluator.evaluate(smoothed_count)
            confirmed_risk, is_stable = persistence.update(raw_risk)

            
            alert_result = alert_engine.process(confirmed_risk.value)

            if alert_result is not None:
                print(f"ALERT EVENT: {alert_result['event']}")

                alert = alert_result["alert"]
                print(f"Alert ID: {alert.alert_id}")
                print(f"Risk: {alert.risk_level}")

                try:
                    backend.send_alert_event(
                        source_id=source_id,
                        alert=alert,
                        event_type=alert_result["event"]
                    )
                    print("Alert event sent to Nexa backend.")
                except Exception as exc:
                    print(f"Failed to send alert event: {exc}")


            # Send monitoring state at most once per second.
            latest_count = smoothed_count
            latest_risk = confirmed_risk.value
            now = time.monotonic()

            if now - last_backend_update >= 1.0:
                try:
                    backend.send_monitoring_update(
                        source_id=source_id,
                        person_count=latest_count,
                        risk_level=latest_risk,
                        source_online=True
                    )

                    last_backend_update = now
                    print(
                        f"BACKEND UPDATE: source={source_id}, "
                        f"count={latest_count}, risk={latest_risk}"
                    )
                except Exception as exc:
                    print(f"Backend update failed: {exc}")

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

            display_width = 1200
            height, width = frame.image.shape[:2]
            scale = display_width / width
            display_height = int(height * scale)

            display_image = cv2.resize(
                frame.image,
                (display_width, display_height)
            )

            cv2.imshow("Nexa - Modules 1 to 5", display_image)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

    finally:
        try:
            final_alert = alert_engine.close()

           
            if final_alert is not None:
                print(f"ALERT EVENT: {final_alert['event']}")
                alert = final_alert["alert"]
                print(f"Alert ID: {alert.alert_id}")
                print(f"Risk: {alert.risk_level}")

                try:
                    backend.send_alert_event(
                        source_id=source_id,
                        alert=alert,
                        event_type=final_alert["event"]
                    )
                    print("Final alert event sent to Nexa backend.")
                except Exception as exc:
                    print(f"Failed to send final alert event: {exc}")

        finally:
            try:
                if backend.token:
                    backend.send_monitoring_update(
                        source_id=source_id,
                        person_count=latest_count,
                        risk_level=latest_risk,
                        source_online=False
                    )
                    print("Backend source marked offline.")
            except Exception as exc:
                print(f"Could not report source offline: {exc}")
            finally:
                source.close()
                cv2.destroyAllWindows()
                print("Video source closed")


if __name__ == "__main__":
    main()
