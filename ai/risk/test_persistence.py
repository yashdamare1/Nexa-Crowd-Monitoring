from risk_level import RiskLevel
from risk_persistence import RiskPersistence


def main():

    persistence = RiskPersistence(
        required_count=3
    )

    test_sequence = [
        RiskLevel.NORMAL,

        RiskLevel.WARNING,
        RiskLevel.WARNING,
        RiskLevel.WARNING,

        RiskLevel.CRITICAL,
        RiskLevel.CRITICAL,
        RiskLevel.CRITICAL,

        RiskLevel.WARNING,
        RiskLevel.WARNING,
        RiskLevel.WARNING,

        RiskLevel.NORMAL,
        RiskLevel.NORMAL,
        RiskLevel.NORMAL
    ]

    for risk in test_sequence:

        confirmed, is_confirmed = persistence.update(
            risk
        )

        print(
            f"Input: {risk.value:<8} | "
            f"Confirmed: {confirmed.value:<8} | "
            f"Stable: {is_confirmed}"
        )


if __name__ == "__main__":
    main()