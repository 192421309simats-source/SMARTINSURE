"""
SmartInsure AI Fraud Detection & Anomaly Risk Analysis Engine
Evaluates claims against underwriting fraud heuristics, frequency spikes, quantum ratios,
and pattern discrepancy indices.
"""

def analyze_claim_fraud(claim_data, user_claims_history=[], policy=None):
    """
    Analyzes a claim using rule-based and statistical heuristics.
    Returns fraud_score, risk_score, priority, and reason checklist.
    """
    fraud_score = 10
    risk_score = 20
    reasons = []

    amount = float(claim_data.get("claim_amount", 0))
    claim_type = str(claim_data.get("claim_type", ""))
    desc = str(claim_data.get("description", "")).lower()
    location = str(claim_data.get("incident_location", "")).lower()
    
    # 1. Coverage quantum check
    if policy:
        coverage = float(policy.get("coverage", 1000000))
        ratio = (amount / coverage) if coverage > 0 else 0
        if ratio > 0.8:
            fraud_score += 30
            risk_score += 25
            reasons.append(f"Claim quantum (₹{amount:,.0f}) is exceptionally high (>80% of total policy coverage)")
        elif ratio > 0.5:
            fraud_score += 15
            risk_score += 15
            reasons.append(f"Substantial claim quantum (₹{amount:,.0f}) relative to policy sum assured")

    # 2. Historical frequency check
    recent_claims = len(user_claims_history)
    if recent_claims >= 2:
        fraud_score += 25
        risk_score += 20
        reasons.append(f"Multiple recent claims detected ({recent_claims} prior claims in active history)")

    # 3. Night / Unverified location / Discrepancy keywords
    if "night" in location or "expressway" in location or "highway" in location:
        if "total loss" in claim_type.lower() or "collision" in desc:
            fraud_score += 18
            reasons.append("High-velocity night highway incident pattern detected")

    if "mismatch" in desc or "discrepancy" in desc or "duplicate" in desc:
        fraud_score += 30
        risk_score += 30
        reasons.append("Discrepancy identified between submitted documentation and provider registry")

    # 4. Critical illness / high value claims
    if "critical" in claim_type.lower() and amount > 500000:
        risk_score += 25
        if not reasons:
            reasons.append("High-value critical illness benefit requiring waiting period & pre-existing validation")

    # Cap scores
    fraud_score = min(96, max(8, fraud_score))
    risk_score = min(96, max(12, risk_score))

    # Priority determination
    if fraud_score >= 70:
        priority = "FRAUD ALERT"
    elif fraud_score >= 45 or risk_score >= 60:
        priority = "HIGH"
    elif fraud_score >= 25 or risk_score >= 35:
        priority = "MEDIUM"
    else:
        priority = "LOW"

    return {
        "fraud_score": fraud_score,
        "risk_score": risk_score,
        "priority": priority,
        "fraud_reasons": reasons
    }


def get_fraud_analytics_summary(all_claims):
    """
    Computes real-time fraud metrics across the entire claims registry.
    """
    total = len(all_claims)
    if total == 0:
        return {
            "total_claims": 0,
            "suspicious_claims": 0,
            "high_risk_claims": 0,
            "fraud_detection_rate": "0.0%"
        }

    suspicious = sum(1 for c in all_claims if c.get("fraud_score", 0) >= 40)
    high_risk = sum(1 for c in all_claims if c.get("priority") in ["HIGH", "FRAUD ALERT"])
    fraud_alerts = sum(1 for c in all_claims if c.get("priority") == "FRAUD ALERT")
    
    rate = (suspicious / total) * 100

    return {
        "total_claims": total,
        "suspicious_claims": suspicious,
        "high_risk_claims": high_risk,
        "fraud_alerts": fraud_alerts,
        "fraud_detection_rate": f"{rate:.1f}%"
    }
