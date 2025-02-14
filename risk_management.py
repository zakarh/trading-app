# risk_management.py

def check_stop_loss(entry_price, current_price, stop_loss_pct=0.05):
    """
    Check whether the current price has fallen below the stop loss threshold.
    Returns True if the stop loss condition is met.
    """
    if current_price <= entry_price * (1 - stop_loss_pct):
        return True
    return False

# Additional risk management functions can be added here.

if __name__ == '__main__':
    # Simple test
    entry = 100
    current = 94
    if check_stop_loss(entry, current, 0.05):
        print("Stop loss triggered.")
    else:
        print("Stop loss not triggered.")
