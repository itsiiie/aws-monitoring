def check_threshold(total_cost, threshold):
    if total_cost >= threshold:
        return f"⚠️ ALERT: Cost has reached ${total_cost:.2f} — exceeds threshold ${threshold:.2f}"
    else:
        return f"✅ All good! Current cost is ${total_cost:.2f}, under threshold ${threshold:.2f}"
