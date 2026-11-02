from risk_config import RiskConfig
from risk_evaluator import RiskEvaluator


def main():

    config = RiskConfig(
        warning_threshold=50,
        critical_threshold=100
    )

    evaluator = RiskEvaluator(config)

    test_counts = [
        20,
        50,
        75,
        100,
        150
    ]

    for count in test_counts:

        risk = evaluator.evaluate(count)

        print(
            f"People: {count} | "
            f"Risk: {risk.value}"
        )


if __name__ == "__main__":
    main()