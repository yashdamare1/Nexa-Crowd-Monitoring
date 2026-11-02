from count_smoother import CountSmoother


def main():

    smoother = CountSmoother(
        window_size=5
    )

    counts = [
        18,
        21,
        19,
        23,
        17,
        25
    ]

    for count in counts:

        smoothed = smoother.update(count)

        print(
            f"Raw count: {count} | "
            f"Smoothed count: {smoothed}"
        )


if __name__ == "__main__":
    main()