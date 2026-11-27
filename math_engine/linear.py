import math

def linear_model(x, weight, bias):
    """Calculate z = wx + b."""
    return weight * x + bias

def sigmoid(z):
    """Stable sigmoid transform; returns a value strictly between 0 and 1."""
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    exp_z = math.exp(z)
    return exp_z / (1.0 + exp_z)

def calculate_score(x, weight, bias):
    z = linear_model(x, weight, bias)
    return {"raw_score": z, "output": sigmoid(z)}
