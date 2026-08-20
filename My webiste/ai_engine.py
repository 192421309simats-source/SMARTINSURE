"""
SmartInsure AI Recommendation & Risk Assessment Engine
Provides mathematical underwriting risk scoring and personalized policy matching.
"""

def calculate_risk_score(profile):
    """
    Calculates a comprehensive actuarial risk score between 1 and 100.
    Factors: Age, Smoking, Pre-existing conditions, Dependents/Income ratio, Health status.
    """
    score = 15  # Base baseline
    
    age = int(profile.get("age", 35))
    if age < 30:
        score += 5
    elif age < 40:
        score += 12
    elif age < 50:
        score += 24
    elif age < 60:
        score += 38
    else:
        score += 52

    # Smoking / Lifestyle
    smoking = str(profile.get("smoking", "Non-Smoker")).lower()
    if "smoker" in smoking and "non" not in smoking:
        score += 22
    
    # Health status & pre-existing conditions
    health = str(profile.get("health_status", "Good")).lower()
    if "critical" in health or "poor" in health:
        score += 25
    elif "moderate" in health or "fair" in health:
        score += 12
    elif "excellent" in health:
        score -= 5

    conditions = str(profile.get("pre_existing_conditions", "None")).lower()
    if conditions and conditions != "none":
        if "diabetes" in conditions or "hypertension" in conditions or "cardiac" in conditions:
            score += 15
        else:
            score += 8

    # Dependents & Income stability
    income = float(profile.get("annual_income", 1000000))
    dependents = int(profile.get("dependents", 2))
    
    if income > 1500000:
        score -= 5
    elif income < 500000:
        score += 8
        
    score = max(5, min(95, score))
    
    if score <= 35:
        level = "LOW"
        desc = "Eligible for premium discounts, accelerated issuance, and standard underwriting."
    elif score <= 65:
        level = "MEDIUM"
        desc = "Standard actuarial classification. Moderate medical disclosure recommended."
    else:
        level = "HIGH"
        desc = "Enhanced risk tier. Comprehensive medical review and rider coverage advised."

    return {
        "risk_score": score,
        "risk_level": level,
        "description": desc,
        "factors": {
            "age_factor": f"{age} years",
            "lifestyle": "Smoker" if "smoker" in smoking and "non" not in smoking else "Non-Smoker",
            "medical_history": "Pre-existing reported" if conditions != "none" else "Clean medical profile",
            "financial_stability": "High Income" if income >= 1200000 else "Standard Income"
        }
    }


def get_personalized_recommendations(user_profile, catalog_policies):
    """
    Evaluates catalog policies against user profile and generates match scores
    along with contextual 'Why this policy?' justification checklists.
    """
    risk_info = calculate_risk_score(user_profile)
    risk_score = risk_info["risk_score"]
    risk_level = risk_info["risk_level"]
    age = int(user_profile.get("age", 35))
    income = float(user_profile.get("annual_income", 1000000))
    dependents = int(user_profile.get("dependents", 2))

    recommendations = []

    for policy in catalog_policies:
        match_score = 70  # Baseline
        reasons = []
        
        cat = policy.get("category", "")
        
        if cat == "Life":
            if dependents >= 2:
                match_score += 18
                reasons.append(f"High family dependency protection for {dependents} dependents")
            if income >= 800000:
                match_score += 8
                reasons.append(f"Ideal income replacement ratio (₹{income:,.0f}/yr)")
            if risk_level == "LOW":
                match_score += 4
                reasons.append("Eligible for preferred non-smoker / low-risk discounted rates")
            reasons.append("Provides Section 80C & 10(10D) tax exemption certificates")
            
        elif cat == "Health":
            match_score += 15
            reasons.append("Covers cashless treatments across 9,500+ empanelled Indian hospitals")
            if risk_level in ["LOW", "MEDIUM"]:
                match_score += 10
                reasons.append("Compatible with your health risk profile without co-pay loading")
            if dependents >= 1:
                reasons.append(f"Comprehensive family float option covering spouse and {dependents} children")
            reasons.append("Deductible under Section 80D up to ₹75,000")

        elif cat == "Family":
            if dependents >= 2:
                match_score += 20
                reasons.append(f"Specially engineered umbrella shield for families with {dependents}+ dependents")
            if age >= 30 and age <= 55:
                match_score += 6
                reasons.append("Covers critical illness & children's future education security")
            reasons.append("Dual Section 80C & 80D tax deductions available")

        elif cat == "Retirement":
            if age >= 35:
                match_score += 16
                reasons.append(f"Optimal retirement accumulation horizon for current age ({age} yrs)")
            if income >= 1000000:
                match_score += 10
                reasons.append("Allows substantial tax-exempt pension pool creation under 80CCC")
            reasons.append("Guaranteed lifetime annuity with 100% purchase price return to nominee")

        elif cat == "Vehicle":
            match_score += 10
            reasons.append("Zero-depreciation protection and 24x7 roadside towing assistance")
            reasons.append("Owner-driver personal accident cover included up to ₹15 Lakhs")

        # Normalize score
        match_score = min(98, max(60, match_score))

        recommendations.append({
            "policy": policy,
            "match_score": match_score,
            "reasons": reasons,
            "is_top_match": False
        })

    # Sort descending by match score
    recommendations.sort(key=lambda x: x["match_score"], reverse=True)
    if recommendations:
        recommendations[0]["is_top_match"] = True

    return {
        "risk_profile": risk_info,
        "recommendations": recommendations
    }
