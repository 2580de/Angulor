from math_engine.linear import linear_model, sigmoid

def test_linear_model():
    assert abs(linear_model(0.8, 2.0, -0.3) - 1.3) < 1e-9

def test_sigmoid_zero():
    assert abs(sigmoid(0) - 0.5) < 1e-9

def test_sigmoid_range():
    assert 0 < sigmoid(2) < 1
    assert 0 < sigmoid(-2) < 1

def run_tests():
    test_linear_model()
    test_sigmoid_zero()
    test_sigmoid_range()
    print("All mathematical tests passed.")

if __name__ == "__main__":
    run_tests()
