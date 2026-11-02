from alert_engine import AlertEngine
from alert_status import AlertStatus


def main():

    engine = AlertEngine()

    # Test 1: No alert for NORMAL risk.
    assert engine.process("NORMAL") is None
    print("PASS: NORMAL creates no alert")

    # Test 2: WARNING creates an alert.
    result = engine.process("WARNING")
    assert result["event"] == "CREATED"

    alert = result["alert"]
    assert alert.alert_id == 1
    assert alert.status == AlertStatus.ACTIVE
    print("PASS: WARNING creates an active alert")

    # Test 3: Repeated WARNING creates no duplicate.
    assert engine.process("WARNING") is None
    print("PASS: Repeated WARNING creates no duplicate")

    # Test 4: CRITICAL escalates the same alert.
    result = engine.process("CRITICAL")
    assert result["event"] == "ESCALATED"
    assert result["alert"].alert_id == 1
    assert result["alert"].risk_level == "CRITICAL"
    print("PASS: CRITICAL escalates the existing alert")

    # Test 5: Repeated CRITICAL creates no duplicate.
    assert engine.process("CRITICAL") is None
    print("PASS: Repeated CRITICAL creates no duplicate")

    # Test 6: NORMAL resolves the active alert.
    result = engine.process("NORMAL")
    assert result["event"] == "RESOLVED"
    assert result["alert"].alert_id == 1
    assert result["alert"].status == AlertStatus.RESOLVED
    assert result["alert"].resolved_at is not None
    print("PASS: NORMAL resolves the active alert")

    # Test 7: Closing with no active alert does nothing.
    assert engine.close() is None
    print("PASS: Closing with no active alert is safe")

    # Test 8: Shutdown resolves an active alert.
    result = engine.process("WARNING")
    assert result["event"] == "CREATED"

    result = engine.close()
    assert result["event"] == "RESOLVED"
    assert result["alert"].alert_id == 2
    assert result["alert"].status == AlertStatus.RESOLVED
    print("PASS: Shutdown resolves an active alert")

    print("\nAll alert lifecycle tests passed.")


if __name__ == "__main__":
    main()