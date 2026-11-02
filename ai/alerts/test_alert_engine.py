from alert_engine import AlertEngine


def main():

    engine = AlertEngine()

    risk_sequence = [
        "NORMAL",

        # Create WARNING alert
        "WARNING",
        "WARNING",

        # Escalate the same alert
        "CRITICAL",
        "CRITICAL",
        "CRITICAL",

        # Still active
        "CRITICAL",

        # Resolve
        "NORMAL"
    ]

    for risk in risk_sequence:

        result = engine.process(risk)

        if result is None:

            print(
                f"Risk: {risk:<8} | "
                f"Result: None"
            )

        else:

            alert = result["alert"]

            print(
                f"Risk: {risk:<8} | "
                f"Event: {result['event']:<9} | "
                f"Alert ID: {alert.alert_id} | "
                f"Alert Risk: {alert.risk_level}"
            )


if __name__ == "__main__":
    main()