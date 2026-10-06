from services.policy_checker import check_policy

def test_policy_fail_short():
    r = check_policy("short")
    assert not r["policy_pass"]

def test_policy_fail_common():
    r = check_policy("password123")
    assert not r["policy_pass"]

def test_policy_pass_long_demo():
    r = check_policy("T9#vL2!qR8@xM4$p")
    assert r["policy_pass"]
