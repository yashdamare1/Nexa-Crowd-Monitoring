import cv2

from person_detector import PersonDetector


def main():

    image = cv2.imread("test.jpg")

    if image is None:
        raise RuntimeError(
            "Unable to load test.jpg"
        )

    detector = PersonDetector(
        model_name="yolo26s.pt",
        confidence=0.25
    )

    results = detector.model(
        image,
        conf=0.25,
        imgsz=1920,
        verbose=False
    )

    detections = []

    for result in results:

        if result.boxes is None:
            continue

        for box in result.boxes:

            class_id = int(
                box.cls[0].item()
            )

            if class_id != 0:
                continue

            confidence = float(
                box.conf[0].item()
            )

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0].tolist()
            )

            detections.append(
                (x1, y1, x2, y2, confidence)
            )

    print(
        f"People detected at 1920: "
        f"{len(detections)}"
    )

    for x1, y1, x2, y2, confidence in detections:

        cv2.rectangle(
            image,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            4
        )

        cv2.putText(
            image,
            f"person {confidence:.2f}",
            (x1, max(30, y1 - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (0, 255, 0),
            3
        )

    display_width = 1200

    height, width = image.shape[:2]

    scale = display_width / width

    display_height = int(
        height * scale
    )

    display_image = cv2.resize(
        image,
        (display_width, display_height)
    )

    cv2.imshow(
        "Nexa - High Resolution Detection",
        display_image
    )

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()