from person_counter import PersonCounter


def main():

    counter = PersonCounter()

    detections = [
        {
            "class": "person",
            "confidence": 0.91
        },
        {
            "class": "person",
            "confidence": 0.84
        },
        {
            "class": "person",
            "confidence": 0.73
        }
    ]

    count = counter.count(detections)

    print(f"People count: {count}")


if __name__ == "__main__":
    main()