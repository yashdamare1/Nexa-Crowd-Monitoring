class PersonCounter:
    """
    Counts valid person detections produced by Module 2.
    """

    def count(self, detections) -> int:
        """
        Return the number of detected people.
        """

        if detections is None:
            return 0

        return len(detections)