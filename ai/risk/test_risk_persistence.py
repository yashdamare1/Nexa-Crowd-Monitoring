from risk_level import RiskLevel
from risk_persistence import RiskPersistence


def main():

    persistence = RiskPersistence(
        escalation_count=3,
        recovery_count=5
    )

    print("Test 1: Escalation")

    for frame in range(1, 4):
        confirmed, stable = persistence.update(
            RiskLevel.WARNING
        )

        print(
            f"Frame: {frame} | "
            f"Confirmed: {confirmed.value} | "
            f"Stable: {stable}"
        )

    assert persistence.confirmed_level == RiskLevel.WARNING

    print("\nTest 2: Recovery")

    for frame in range(1, 6):
        confirmed, stable = persistence.update(
            RiskLevel.NORMAL
        )

        print(
            f"Frame: {frame} | "
            f"Confirmed: {confirmed.value} | "
            f"Stable: {stable}"
        )

    assert persistence.confirmed_level == RiskLevel.NORMAL

    print("\nAll risk persistence tests passed.")


if __name__ == "__main__":
    main()