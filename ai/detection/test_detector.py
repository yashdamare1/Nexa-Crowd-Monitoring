import cv2

from person_detector import PersonDetector


def main():

    detector = PersonDetector(
        model_name="yolo26s.pt",
        confidence=0.25
    )

    image = cv2.imread("test.jpg")

    if image is None:
        raise RuntimeError(
            "Unable to load test.jpg"
        )

    detections = detector.detect(image)

    print(
        f"People detected: {len(detections)}"
    )

    for detection in detections:

        print(detection)

        x1 = detection["x1"]
        y1 = detection["y1"]
        x2 = detection["x2"]
        y2 = detection["y2"]

        confidence = detection["confidence"]

        cv2.rectangle(
            image,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            5
        )

        cv2.putText(
            image,
            f"person {confidence:.2f}",
            (x1, y1 - 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (0, 255, 0),
            4
        )

    # Resize image only for display
    display_width = 1200

    original_height, original_width = image.shape[:2]

    scale = display_width / original_width

    display_height = int(
        original_height * scale
    )

    display_image = cv2.resize(
        image,
        (display_width, display_height)
    )

    cv2.imshow(
        "Nexa - Person Detection",
        display_image
    )

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()