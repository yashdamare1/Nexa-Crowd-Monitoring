from ultralytics import YOLO


class PersonDetector:
    """
    Detects people using a pretrained YOLO model.
    """

    PERSON_CLASS_ID = 0

    def __init__(
        self,
        model_name: str = "yolo26s.pt",
        confidence: float = 0.25
    ):
        self.model = YOLO(model_name)
        self.confidence = confidence

    def detect(self, image):

        results = self.model(
            image,
            conf=self.confidence,
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

                # Only keep person detections
                if class_id != self.PERSON_CLASS_ID:
                    continue

                confidence = float(
                    box.conf[0].item()
                )

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0].tolist()
                )

                detections.append({
                    "class": "person",
                    "confidence": confidence,
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2
                })

        return detections