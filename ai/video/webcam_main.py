import cv2

from webcam_source import WebcamSource


def main():

    source = WebcamSource(
        source_id="webcam-01",
        camera_index=0
    )

    try:
        source.open()

        metadata = source.get_metadata()

        print("Webcam opened successfully")
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
                "Nexa - Webcam",
                frame.image
            )

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

    finally:
        source.close()
        cv2.destroyAllWindows()

        print("Webcam source closed")


if __name__ == "__main__":
    main()