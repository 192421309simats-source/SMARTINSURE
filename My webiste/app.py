import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash

from database import db
from ai_engine import calculate_risk_score, get_personalized_recommendations
from fraud_engine import analyze_claim_fraud, get_fraud_analytics_summary

app = Flask(__name__)
app.secret_key = "smartinsure_institutional_secret_key_2026"

# Helper context processor to pass current user and branding info
@app.context_processor
def inject_global_data():
    user = None
    if "user_id" in session:
        user = db.get_user_by_id(session["user_id"])
    return {
        "current_user": user,
        "brand_name": "SMARTINSURE",
        "tagline": "Secure Today. Confident Tomorrow.",
        "toll_free": "1800-209-8888",
        "support_email": "support@smartinsure.com",
        "current_year": 2026
    }

# ==================== PUBLIC ROUTES ====================

@app.route("/")
def index():
    catalog = db.get_catalog()
    stats = {
        "customers": "10,000+",
        "policies": "500+",
        "claims_processed": "2,400+",
        "csat": "95%"
    }
    return render_template("index.html", catalog=catalog, stats=stats)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/solutions")
def solutions():
    catalog = db.get_catalog()
    return render_template("solutions.html", catalog=catalog)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        identifier = request.form.get("identifier", "").strip()
        password = request.form.get("password", "").strip()
        
        user = db.get_user_by_email_or_username(identifier)
        if user and user.get("password") == password:
            session["user_id"] = user["id"]
            session["role"] = user.get("role", "customer")
            flash(f"Welcome back, {user['name']}.", "success")
            if user.get("role") == "admin":
                return redirect(url_for("admin_dashboard"))
            return redirect(url_for("customer_dashboard"))
        else:
            flash("Invalid credentials. Please verify your email/username and password.", "danger")
            
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        username = request.form.get("username", "").strip() or email.split("@")[0]
        password = request.form.get("password", "").strip()
        phone = request.form.get("phone", "").strip()
        age = int(request.form.get("age", 30))
        annual_income = float(request.form.get("annual_income", 1000000))
        occupation = request.form.get("occupation", "Professional").strip()
        dependents = int(request.form.get("dependents", 2))
        smoking = request.form.get("smoking", "Non-Smoker")
        health_status = request.form.get("health_status", "Good")
        pre_existing = request.form.get("pre_existing_conditions", "None").strip()

        # Check existing
        if db.get_user_by_email_or_username(email):
            flash("An account with this email already exists.", "warning")
            return redirect(url_for("login"))

        risk_analysis = calculate_risk_score({
            "age": age,
            "annual_income": annual_income,
            "dependents": dependents,
            "smoking": smoking,
            "health_status": health_status,
            "pre_existing_conditions": pre_existing
        })

        new_user = {
            "name": name,
            "email": email,
            "username": username,
            "password": password,
            "role": "customer",
            "phone": phone,
            "age": age,
            "annual_income": annual_income,
            "occupation": occupation,
            "dependents": dependents,
            "smoking": smoking,
            "health_status": health_status,
            "pre_existing_conditions": pre_existing,
            "risk_score": risk_analysis["risk_score"],
            "risk_level": risk_analysis["risk_level"]
        }

        created = db.add_user(new_user)
        session["user_id"] = created["id"]
        session["role"] = "customer"
        flash("Registration successful. Your policyholder account has been activated.", "success")
        return redirect(url_for("recommendations"))

    return render_template("register.html")

@app.route("/demo-login/<role>")
def demo_login(role):
    if role == "admin":
        user = db.get_user_by_email_or_username("admin")
        if user:
            session["user_id"] = user["id"]
            session["role"] = "admin"
            flash("Logged in as Senior Administrator S. K. Raman (Demo Mode)", "info")
            return redirect(url_for("admin_dashboard"))
    else:
        user = db.get_user_by_email_or_username("rajesh")
        if user:
            session["user_id"] = user["id"]
            session["role"] = "customer"
            flash("Logged in as Policyholder Rajesh Sharma (Demo Mode)", "info")
            return redirect(url_for("customer_dashboard"))
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been securely logged out from SmartInsure.", "info")
    return redirect(url_for("index"))

@app.route("/track", methods=["GET"])
def track_claim_public():
    claim_id = request.args.get("claim_id", "").strip()
    claim = None
    searched = False
    if claim_id:
        searched = True
        claim = db.get_claim_by_id(claim_id)
    return render_template("track_claim.html", claim=claim, claim_id=claim_id, searched=searched)


# ==================== CUSTOMER PORTAL ROUTES ====================

def require_customer():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user = db.get_user_by_id(session["user_id"])
    if not user:
        session.clear()
        return redirect(url_for("login"))
    return None

@app.route("/dashboard")
def customer_dashboard():
    auth_check = require_customer()
    if auth_check:
        return auth_check
        
    user = db.get_user_by_id(session["user_id"])
    user_policies = db.get_user_policies(user["id"])
    user_claims = db.get_claims(user["id"])
    notifications = db.get_notifications(user["id"])
    
    total_premium = sum(p.get("premium", 0) for p in user_policies)
    pending_claims = sum(1 for c in user_claims if c.get("status") not in ["Settled", "Rejected"])
    
    # Calculate fresh risk profile
    risk_info = calculate_risk_score(user)

    return render_template(
        "dashboard.html",
        user=user,
        policies=user_policies,
        claims=user_claims,
        notifications=notifications,
        total_premium=total_premium,
        pending_claims=pending_claims,
        risk_info=risk_info
    )

@app.route("/my-policies")
def my_policies():
    auth_check = require_customer()
    if auth_check:
        return auth_check
    user = db.get_user_by_id(session["user_id"])
    policies = db.get_user_policies(user["id"])
    return render_template("my_policies.html", policies=policies, user=user)

@app.route("/recommendations")
def recommendations():
    auth_check = require_customer()
    if auth_check:
        return auth_check
        
    user = db.get_user_by_id(session["user_id"])
    catalog = db.get_catalog()
    
    rec_data = get_personalized_recommendations(user, catalog)
    return render_template(
        "recommendations.html",
        user=user,
        risk_profile=rec_data["risk_profile"],
        recommendations=rec_data["recommendations"]
    )

@app.route("/compare")
def compare_policies():
    auth_check = require_customer()
    if auth_check:
        return auth_check
    
    catalog = db.get_catalog()
    user = db.get_user_by_id(session["user_id"])
    rec_data = get_personalized_recommendations(user, catalog)
    
    # Select 3 core policies for side-by-side comparison
    compare_list = catalog[:3]
    return render_template("compare.html", policies=compare_list, user=user, rec_data=rec_data)

@app.route("/submit-claim", methods=["GET", "POST"])
def submit_claim():
    auth_check = require_customer()
    if auth_check:
        return auth_check
        
    user = db.get_user_by_id(session["user_id"])
    user_policies = db.get_user_policies(user["id"])

    if request.method == "POST":
        policy_num = request.form.get("policy_number", "").strip()
        claim_type = request.form.get("claim_type", "").strip()
        incident_date = request.form.get("incident_date", "").strip()
        incident_location = request.form.get("incident_location", "").strip()
        claim_amount = float(request.form.get("claim_amount", 0))
        description = request.form.get("description", "").strip()
        doc_names = request.form.get("doc_names", "Hospital_Invoice.pdf, Medical_Discharge_Summary.pdf")

        # Find policy details
        policy = db.get_policy_by_number(policy_num)
        policy_name = policy["policy_name"] if policy else "Smart Insurance Plan"

        # Run AI Fraud & Risk Analysis Engine
        user_history = db.get_claims(user["id"])
        fraud_analysis = analyze_claim_fraud({
            "claim_amount": claim_amount,
            "claim_type": claim_type,
            "description": description,
            "incident_location": incident_location
        }, user_history, policy)

        new_claim = {
            "user_id": user["id"],
            "customer_name": user["name"],
            "customer_email": user["email"],
            "policy_number": policy_num,
            "policy_name": policy_name,
            "claim_type": claim_type,
            "claim_amount": claim_amount,
            "claim_amount_display": f"₹{claim_amount:,.0f}",
            "incident_date": incident_date,
            "incident_location": incident_location,
            "description": description,
            "documents": [d.strip() for d in doc_names.split(",") if d.strip()],
            "risk_score": fraud_analysis["risk_score"],
            "fraud_score": fraud_analysis["fraud_score"],
            "priority": fraud_analysis["priority"],
            "priority_badge": fraud_analysis["priority"],
            "fraud_reasons": fraud_analysis["fraud_reasons"],
            "status": "Submitted"
        }

        created = db.add_claim(new_claim)
        flash(f"Claim successfully registered with Reference Number {created['claim_id']}.", "success")
        return redirect(url_for("track_claim_public", claim_id=created["claim_id"]))

    return render_template("submit_claim.html", user=user, policies=user_policies)

@app.route("/my-claims")
def my_claims():
    auth_check = require_customer()
    if auth_check:
        return auth_check
    user = db.get_user_by_id(session["user_id"])
    claims = db.get_claims(user["id"])
    return render_template("my_claims.html", claims=claims, user=user)

@app.route("/payments")
def customer_payments():
    auth_check = require_customer()
    if auth_check:
        return auth_check
    user = db.get_user_by_id(session["user_id"])
    payments = db.get_payments(user["id"])
    policies = db.get_user_policies(user["id"])
    return render_template("payments.html", payments=payments, policies=policies, user=user)

@app.route("/profile", methods=["GET", "POST"])
def user_profile():
    auth_check = require_customer()
    if auth_check:
        return auth_check
    user = db.get_user_by_id(session["user_id"])
    
    if request.method == "POST":
        updates = {
            "name": request.form.get("name", user["name"]),
            "phone": request.form.get("phone", user["phone"]),
            "annual_income": float(request.form.get("annual_income", user["annual_income"])),
            "occupation": request.form.get("occupation", user.get("occupation", "")),
            "dependents": int(request.form.get("dependents", user["dependents"])),
            "smoking": request.form.get("smoking", user["smoking"]),
            "health_status": request.form.get("health_status", user["health_status"]),
            "pre_existing_conditions": request.form.get("pre_existing_conditions", user["pre_existing_conditions"])
        }
        
        # Recalculate risk score
        risk_data = calculate_risk_score({**user, **updates})
        updates["risk_score"] = risk_data["risk_score"]
        updates["risk_level"] = risk_data["risk_level"]
        
        db.update_user(user["id"], updates)
        flash("Profile and underwriting risk parameters successfully updated.", "success")
        return redirect(url_for("user_profile"))
        
    risk_info = calculate_risk_score(user)
    return render_template("profile.html", user=user, risk_info=risk_info)


# ==================== ADMIN PORTAL ROUTES ====================

def require_admin():
    if "user_id" not in session or session.get("role") != "admin":
        flash("Unauthorized access. Administrator privileges required.", "danger")
        return redirect(url_for("login"))
    return None

@app.route("/admin")
@app.route("/admin/dashboard")
def admin_dashboard():
    auth_check = require_admin()
    if auth_check:
        return auth_check
        
    admin_user = db.get_user_by_id(session["user_id"])
    all_users = [u for u in db.get_all_users() if u.get("role") != "admin"]
    all_policies = db.get_user_policies()
    all_claims = db.get_claims()
    all_payments = db.get_payments()
    
    total_customers = len(all_users)
    active_policies_count = len(all_policies)
    pending_claims_count = sum(1 for c in all_claims if c.get("status") in ["Submitted", "Under Review", "Investigating"])
    high_risk_claims_count = sum(1 for c in all_claims if c.get("priority") in ["HIGH", "FRAUD ALERT"])
    fraud_alerts_count = sum(1 for c in all_claims if c.get("priority") == "FRAUD ALERT")
    total_premium_revenue = sum(p.get("amount", 0) for p in all_payments) + 12450000 # Institutional total volume
    
    fraud_summary = get_fraud_analytics_summary(all_claims)

    return render_template(
        "admin/dashboard.html",
        admin=admin_user,
        total_customers=total_customers,
        active_policies=active_policies_count,
        pending_claims=pending_claims_count,
        high_risk_claims=high_risk_claims_count,
        fraud_alerts=fraud_alerts_count,
        total_premium_revenue=f"₹{total_premium_revenue:,.0f}",
        fraud_summary=fraud_summary,
        recent_claims=all_claims[:5]
    )

@app.route("/admin/customers")
def admin_customers():
    auth_check = require_admin()
    if auth_check:
        return auth_check
    customers = [u for u in db.get_all_users() if u.get("role") != "admin"]
    return render_template("admin/customers.html", customers=customers)

@app.route("/admin/claims")
def admin_claims():
    auth_check = require_admin()
    if auth_check:
        return auth_check
    claims = db.get_claims()
    return render_template("admin/claims.html", claims=claims)

@app.route("/admin/fraud")
def admin_fraud():
    auth_check = require_admin()
    if auth_check:
        return auth_check
    claims = db.get_claims()
    fraud_summary = get_fraud_analytics_summary(claims)
    return render_template("admin/fraud.html", claims=claims, summary=fraud_summary)

@app.route("/admin/policies")
def admin_policies():
    auth_check = require_admin()
    if auth_check:
        return auth_check
    catalog = db.get_catalog()
    return render_template("admin/policies.html", catalog=catalog)


# ==================== REST APIs ====================

@app.route("/api/admin/claims/<claim_id>/adjudicate", methods=["POST"])
def api_adjudicate_claim(claim_id):
    if "user_id" not in session or session.get("role") != "admin":
        return jsonify({"success": False, "error": "Unauthorized"}), 403
        
    data = request.get_json() or {}
    action = data.get("action")  # approve, reject, investigate, settle, verify
    note = data.get("note", "Adjudication decision updated by Senior Claims Desk.")

    status_map = {
        "verify": ("Documents Verified", 2),
        "review": ("Under Review", 3),
        "investigate": ("Investigating", 3),
        "approve": ("Approved", 4),
        "reject": ("Rejected", 4),
        "settle": ("Settled", 5)
    }

    if action not in status_map:
        return jsonify({"success": False, "error": "Invalid adjudication action"}), 400

    new_status, step = status_map[action]
    updated = db.update_claim_status(claim_id, new_status, step=step, note=note)
    
    if updated:
        return jsonify({"success": True, "claim": updated})
    return jsonify({"success": False, "error": "Claim not found"}), 404

@app.route("/api/admin/policies/create", methods=["POST"])
def api_create_policy():
    if "user_id" not in session or session.get("role") != "admin":
        return jsonify({"success": False, "error": "Unauthorized"}), 403
    
    data = request.get_json() or {}
    policy_name = data.get("name")
    pol_type = data.get("type", "Life Insurance")
    premium = float(data.get("premium", 15000))
    coverage = float(data.get("coverage", 1000000))
    duration = data.get("duration", "20 Years")
    benefits = data.get("benefits", ["Comprehensive institutional coverage"])

    new_policy = {
        "name": policy_name,
        "type": pol_type,
        "category": pol_type.split()[0],
        "tagline": data.get("tagline", "Institutional insurance plan"),
        "coverage": coverage,
        "coverage_display": f"₹{coverage:,.0f}",
        "premium": premium,
        "premium_frequency": "Annual",
        "duration": duration,
        "min_age": 18,
        "max_age": 65,
        "claim_support_ratio": "99.0%",
        "waiting_period": "30 Days",
        "tax_benefit": "Section 80C/80D",
        "benefits": benefits,
        "recommended_for": ["All Citizens"],
        "status": "Active",
        "badge": "Newly Launched"
    }

    created = db.add_catalog_policy(new_policy)
    return jsonify({"success": True, "policy": created})

@app.route("/api/calculate-risk", methods=["POST"])
def api_calculate_risk():
    data = request.get_json() or {}
    res = calculate_risk_score(data)
    return jsonify(res)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
