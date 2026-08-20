import json
import os
from datetime import datetime, date

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(DATA_DIR, exist_ok=True)
DB_FILE = os.path.join(DATA_DIR, 'smartinsure_db.json')

DEFAULT_DATA = {
    "users": [
        {
            "id": "USR-001",
            "name": "Rajesh Sharma",
            "email": "rajesh.sharma@example.com",
            "username": "rajesh",
            "password": "password123",
            "role": "customer",
            "phone": "+91 98765 43210",
            "age": 38,
            "annual_income": 1400000,
            "occupation": "Senior IT Consultant",
            "dependents": 3,
            "smoking": "Non-Smoker",
            "health_status": "Good",
            "pre_existing_conditions": "None",
            "risk_score": 28,
            "risk_level": "LOW",
            "status": "Active",
            "created_at": "2025-01-15"
        },
        {
            "id": "USR-002",
            "name": "Priya Patel",
            "email": "priya.patel@example.com",
            "username": "priya",
            "password": "password123",
            "role": "customer",
            "phone": "+91 98234 56789",
            "age": 46,
            "annual_income": 950000,
            "occupation": "School Principal",
            "dependents": 2,
            "smoking": "Non-Smoker",
            "health_status": "Moderate",
            "pre_existing_conditions": "Mild Hypertension",
            "risk_score": 42,
            "risk_level": "MEDIUM",
            "status": "Active",
            "created_at": "2025-03-20"
        },
        {
            "id": "USR-003",
            "name": "Vikram Malhotra",
            "email": "vikram.m@example.com",
            "username": "vikram",
            "password": "password123",
            "role": "customer",
            "phone": "+91 97112 34567",
            "age": 52,
            "annual_income": 2200000,
            "occupation": "Business Director",
            "dependents": 4,
            "smoking": "Smoker",
            "health_status": "Critical Monitor",
            "pre_existing_conditions": "Type-2 Diabetes",
            "risk_score": 68,
            "risk_level": "HIGH",
            "status": "Active",
            "created_at": "2025-02-10"
        },
        {
            "id": "USR-004",
            "name": "Ananya Sen",
            "email": "ananya.sen@example.com",
            "username": "ananya",
            "password": "password123",
            "role": "customer",
            "phone": "+91 94331 88990",
            "age": 29,
            "annual_income": 850000,
            "occupation": "UX Designer",
            "dependents": 1,
            "smoking": "Non-Smoker",
            "health_status": "Excellent",
            "pre_existing_conditions": "None",
            "risk_score": 18,
            "risk_level": "LOW",
            "status": "Active",
            "created_at": "2025-05-18"
        },
        {
            "id": "ADM-001",
            "name": "S. K. Raman (Chief Underwriter)",
            "email": "admin@smartinsure.com",
            "username": "admin",
            "password": "adminpassword",
            "role": "admin",
            "phone": "+91 1800 209 8888",
            "designation": "Senior Claims Officer & Risk Administrator",
            "status": "Active",
            "created_at": "2024-01-01"
        }
    ],
    "policies_catalog": [
        {
            "id": "POL-CAT-01",
            "name": "Smart Jeevan Raksha Term Plan",
            "type": "Life Insurance",
            "category": "Life",
            "tagline": "Pure term protection with terminal illness accelerator",
            "coverage": 10000000,
            "coverage_display": "₹1.00 Crore",
            "premium": 14500,
            "premium_frequency": "Annual",
            "duration": "35 Years",
            "min_age": 18,
            "max_age": 65,
            "claim_support_ratio": "99.2%",
            "waiting_period": "None (Instant Cover)",
            "tax_benefit": "Section 80C & 10(10D)",
            "benefits": [
                "100% Tax-free lump sum payout on demise",
                "Built-in Terminal Illness Cover up to ₹50 Lakhs",
                "Waiver of premium on accidental total disability",
                "Optional accidental death rider"
            ],
            "recommended_for": ["Low Risk", "Salaried", "High Dependents"],
            "status": "Active",
            "badge": "Highest Demanded"
        },
        {
            "id": "POL-CAT-02",
            "name": "Smart Arogya Sanjeevani Health Shield",
            "type": "Health Insurance",
            "category": "Health",
            "tagline": "Comprehensive cashless family hospitalization cover across 9,500+ network hospitals",
            "coverage": 1500000,
            "coverage_display": "₹15 Lakhs",
            "premium": 18200,
            "premium_frequency": "Annual",
            "duration": "1 Year (Renewable)",
            "min_age": 18,
            "max_age": 70,
            "claim_support_ratio": "98.6%",
            "waiting_period": "30 Days (Accident Day 1)",
            "tax_benefit": "Section 80D up to ₹75,000",
            "benefits": [
                "Cashless treatment in 9,500+ empanelled hospitals",
                "Zero co-payment on room rent & ICU charges",
                "Daycare procedures & AYUSH treatment included",
                "Annual complimentary preventive health checkup"
            ],
            "recommended_for": ["Family", "Medium Risk", "Low Risk"],
            "status": "Active",
            "badge": "Top Recommended"
        },
        {
            "id": "POL-CAT-03",
            "name": "Smart Suraksha Motor Package",
            "type": "Vehicle Insurance",
            "category": "Vehicle",
            "tagline": "Comprehensive zero-depreciation 4-wheeler and 2-wheeler motor protection",
            "coverage": 850000,
            "coverage_display": "₹8.5 Lakhs (IDV)",
            "premium": 9400,
            "premium_frequency": "Annual",
            "duration": "1 Year",
            "min_age": 18,
            "max_age": 80,
            "claim_support_ratio": "97.8%",
            "waiting_period": "Immediate",
            "tax_benefit": "Business Expense deductible",
            "benefits": [
                "Zero Depreciation on plastic & metal parts",
                "24x7 Roadside Assistance & towing pan-India",
                "Engine & Gearbox hydrostatic lock protection",
                "Personal Accident Cover for owner-driver (₹15 Lakhs)"
            ],
            "recommended_for": ["Vehicle Owners", "Commuters"],
            "status": "Active",
            "badge": "Quick Settlement"
        },
        {
            "id": "POL-CAT-04",
            "name": "Smart Parivar Sampurna Shield",
            "type": "Family Protection",
            "category": "Family",
            "tagline": "Holistic umbrella shield securing parents, spouse, children & critical illnesses",
            "coverage": 2500000,
            "coverage_display": "₹25 Lakhs",
            "premium": 27500,
            "premium_frequency": "Annual",
            "duration": "Multi-Year (3 Years)",
            "min_age": 21,
            "max_age": 65,
            "claim_support_ratio": "99.1%",
            "waiting_period": "60 Days for Critical Illness",
            "tax_benefit": "Section 80C & 80D",
            "benefits": [
                "Combines Term Life + 32 Critical Illness + Child Education fund",
                "Guaranteed renewal regardless of claims history",
                "Global emergency medical assistance & air ambulance",
                "Maternity & newborn hospitalization covered"
            ],
            "recommended_for": ["Married with Kids", "Single Breadwinners"],
            "status": "Active",
            "badge": "Best Family Value"
        },
        {
            "id": "POL-CAT-05",
            "name": "Smart Pension Vriddhi Retirement Fund",
            "type": "Retirement Planning",
            "category": "Retirement",
            "tagline": "Guaranteed annuity pension with wealth growth & inflation cushion",
            "coverage": 5000000,
            "coverage_display": "₹50 Lakhs Annuity Pool",
            "premium": 60000,
            "premium_frequency": "Annual",
            "duration": "20 Years Accumulation",
            "min_age": 25,
            "max_age": 60,
            "claim_support_ratio": "99.8%",
            "waiting_period": "N/A",
            "tax_benefit": "Section 80CCC & 10(10A)",
            "benefits": [
                "Guaranteed monthly annuity for lifetime post-retirement",
                "Return of total purchase price to nominee upon demise",
                "Joint life annuity option with spouse continuation",
                "Systematic loyalty additions every 5 years"
            ],
            "recommended_for": ["Ages 30+", "Retirement Focused"],
            "status": "Active",
            "badge": "Guaranteed Annuity"
        }
    ],
    "user_policies": [
        {
            "policy_number": "POL-2026-LI-10492",
            "user_id": "USR-001",
            "user_name": "Rajesh Sharma",
            "policy_name": "Smart Jeevan Raksha Term Plan",
            "policy_type": "Life Insurance",
            "category": "Life",
            "premium": 14500,
            "coverage": 10000000,
            "coverage_display": "₹1,00,00,000",
            "start_date": "2024-04-01",
            "expiry_date": "2059-03-31",
            "next_due_date": "2027-04-01",
            "status": "Active",
            "payment_frequency": "Annual",
            "nominee": "Sunita Sharma (Wife) - 100%",
            "branch": "SmartInsure Connaught Place Branch, New Delhi"
        },
        {
            "policy_number": "POL-2026-HL-28491",
            "user_id": "USR-001",
            "user_name": "Rajesh Sharma",
            "policy_name": "Smart Arogya Sanjeevani Health Shield",
            "policy_type": "Health Insurance",
            "category": "Health",
            "premium": 18200,
            "coverage": 1500000,
            "coverage_display": "₹15,00,000",
            "start_date": "2024-06-15",
            "expiry_date": "2027-06-14",
            "next_due_date": "2027-06-15",
            "status": "Active",
            "payment_frequency": "Annual",
            "nominee": "Sunita Sharma (Wife)",
            "branch": "SmartInsure Noida Sector 18 Branch"
        },
        {
            "policy_number": "POL-2026-VH-49201",
            "user_id": "USR-001",
            "user_name": "Rajesh Sharma",
            "policy_name": "Smart Suraksha Motor Package",
            "policy_type": "Vehicle Insurance",
            "category": "Vehicle",
            "premium": 9400,
            "coverage": 850000,
            "coverage_display": "₹8,50,000",
            "start_date": "2025-08-10",
            "expiry_date": "2026-08-09",
            "next_due_date": "2026-08-10",
            "status": "Grace Period",
            "payment_frequency": "Annual",
            "nominee": "Rajesh Sharma (Self)",
            "branch": "SmartInsure Indirapuram Branch"
        },
        {
            "policy_number": "POL-2026-FM-50291",
            "user_id": "USR-002",
            "user_name": "Priya Patel",
            "policy_name": "Smart Parivar Sampurna Shield",
            "policy_type": "Family Protection",
            "category": "Family",
            "premium": 27500,
            "coverage": 2500000,
            "coverage_display": "₹25,00,000",
            "start_date": "2025-01-10",
            "expiry_date": "2028-01-09",
            "next_due_date": "2027-01-10",
            "status": "Active",
            "payment_frequency": "Annual",
            "nominee": "Ramesh Patel (Husband)",
            "branch": "SmartInsure Ahmedabad Main Branch"
        },
        {
            "policy_number": "POL-2026-RT-39401",
            "user_id": "USR-003",
            "user_name": "Vikram Malhotra",
            "policy_name": "Smart Pension Vriddhi Retirement Fund",
            "policy_type": "Retirement Planning",
            "category": "Retirement",
            "premium": 60000,
            "coverage": 5000000,
            "coverage_display": "₹50,00,000",
            "start_date": "2023-11-01",
            "expiry_date": "2043-10-31",
            "next_due_date": "2026-11-01",
            "status": "Active",
            "payment_frequency": "Annual",
            "nominee": "Meenakshi Malhotra (Wife)",
            "branch": "SmartInsure Mumbai Nariman Point Branch"
        }
    ],
    "claims": [
        {
            "claim_id": "CLM-2026-000145",
            "user_id": "USR-001",
            "customer_name": "Rajesh Sharma",
            "customer_email": "rajesh.sharma@example.com",
            "policy_number": "POL-2026-HL-28491",
            "policy_name": "Smart Arogya Sanjeevani Health Shield",
            "claim_type": "Cashless Hospitalization",
            "claim_amount": 145000,
            "claim_amount_display": "₹1,45,000",
            "incident_date": "2026-07-22",
            "incident_location": "Fortis Escorts Hospital, New Delhi",
            "description": "Emergency acute laparoscopic appendectomy performed due to severe abdominal pain and infection.",
            "documents": [
                "Hospital_Admission_Note.pdf",
                "Discharge_Summary_Signed.pdf",
                "Itemized_Pharmacy_Bills.pdf",
                "Diagnostic_CT_Scan_Report.pdf"
            ],
            "risk_score": 24,
            "fraud_score": 12,
            "priority": "LOW",
            "priority_badge": "LOW",
            "status": "Under Review",
            "current_step": 3,
            "status_timeline": [
                {
                    "step": 1,
                    "name": "Submitted",
                    "date": "2026-07-23 10:15 AM",
                    "completed": True,
                    "note": "Claim registered online by policyholder. Digital acknowledgment issued."
                },
                {
                    "step": 2,
                    "name": "Documents Verified",
                    "date": "2026-07-24 02:40 PM",
                    "completed": True,
                    "note": "Hospital discharge summary and itemized bills verified against hospital portal."
                },
                {
                    "step": 3,
                    "name": "Under Review",
                    "date": "2026-07-25 11:30 AM",
                    "completed": False,
                    "active": True,
                    "note": "Medical underwriter evaluating surgical room rent and pharmacy breakdown."
                },
                {
                    "step": 4,
                    "name": "Decision",
                    "date": "Expected by 2026-08-22",
                    "completed": False,
                    "active": False,
                    "note": "Final adjudication approval pending Chief Medical Officer signoff."
                },
                {
                    "step": 5,
                    "name": "Settlement",
                    "date": "Pending Decision",
                    "completed": False,
                    "active": False,
                    "note": "Direct NEFT transfer to empanelled hospital account."
                }
            ],
            "fraud_reasons": [],
            "created_at": "2026-07-23"
        },
        {
            "claim_id": "CLM-2026-000146",
            "user_id": "USR-002",
            "customer_name": "Priya Patel",
            "customer_email": "priya.patel@example.com",
            "policy_number": "POL-2026-FM-50291",
            "policy_name": "Smart Parivar Sampurna Shield",
            "claim_type": "Reimbursement - Outpatient Therapy",
            "claim_amount": 38000,
            "claim_amount_display": "₹38,000",
            "incident_date": "2026-06-12",
            "incident_location": "Sterling Hospital, Ahmedabad",
            "description": "Post-accidental physical rehabilitation and physiotherapy follow-up sessions.",
            "documents": [
                "Physiotherapist_Certification.pdf",
                "Receipts_Batch_June.pdf"
            ],
            "risk_score": 35,
            "fraud_score": 18,
            "priority": "LOW",
            "priority_badge": "LOW",
            "status": "Settled",
            "current_step": 5,
            "status_timeline": [
                {"step": 1, "name": "Submitted", "date": "2026-06-14 09:30 AM", "completed": True, "note": "Claim submitted online."},
                {"step": 2, "name": "Documents Verified", "date": "2026-06-15 04:10 PM", "completed": True, "note": "Prescriptions and payment receipts verified."},
                {"step": 3, "name": "Under Review", "date": "2026-06-16 11:20 AM", "completed": True, "note": "Adjudicated by claims desk."},
                {"step": 4, "name": "Decision", "date": "2026-06-17 03:45 PM", "completed": True, "note": "Approved in full for ₹38,000."},
                {"step": 5, "name": "Settlement", "date": "2026-06-18 10:00 AM", "completed": True, "note": "NEFT Ref #TXN9842109 transferred to customer account."}
            ],
            "fraud_reasons": [],
            "created_at": "2026-06-14"
        },
        {
            "claim_id": "CLM-2026-000147",
            "user_id": "USR-003",
            "customer_name": "Vikram Malhotra",
            "customer_email": "vikram.m@example.com",
            "policy_number": "POL-2026-RT-39401",
            "policy_name": "Smart Pension Vriddhi Retirement Fund",
            "claim_type": "Critical Illness Rider Claim",
            "claim_amount": 920000,
            "claim_amount_display": "₹9,20,000",
            "incident_date": "2026-07-28",
            "incident_location": "Hinduja Healthcare, Mumbai",
            "description": "Coronary angioplasty stent placement following acute myocardial infarction episode.",
            "documents": [
                "Cath_Lab_Angiography_Report.pdf",
                "Discharge_Summary.pdf",
                "Stent_Invoices_Barcode.pdf"
            ],
            "risk_score": 62,
            "fraud_score": 48,
            "priority": "MEDIUM",
            "priority_badge": "MEDIUM",
            "status": "Under Review",
            "current_step": 3,
            "status_timeline": [
                {"step": 1, "name": "Submitted", "date": "2026-07-29 02:20 PM", "completed": True, "note": "Claim submitted with cardiac medical records."},
                {"step": 2, "name": "Documents Verified", "date": "2026-07-30 05:00 PM", "completed": True, "note": "Cardiac specialist documentation under verification."},
                {"step": 3, "name": "Under Review", "date": "2026-08-01 10:30 AM", "completed": False, "active": True, "note": "Cross-checking pre-existing diabetes timeline vs waiting period clause."},
                {"step": 4, "name": "Decision", "date": "Pending Review", "completed": False, "active": False, "note": "Under investigation."},
                {"step": 5, "name": "Settlement", "date": "Pending Decision", "completed": False, "active": False, "note": "Awaiting approval."}
            ],
            "fraud_reasons": ["Pre-existing condition timeline verification required", "High claim quantum vs tenure"],
            "created_at": "2026-07-29"
        },
        {
            "claim_id": "CLM-2026-000148",
            "user_id": "USR-004",
            "customer_name": "Ananya Sen",
            "customer_email": "ananya.sen@example.com",
            "policy_number": "POL-2026-HL-28491",
            "policy_name": "Smart Arogya Sanjeevani Health Shield",
            "claim_type": "Cashless Hospitalization",
            "claim_amount": 62000,
            "claim_amount_display": "₹62,000",
            "incident_date": "2026-08-02",
            "incident_location": "Apollo Hospital, Kolkata",
            "description": "Daycare nasal endoscopic sinus surgery (FESS) under local anesthesia.",
            "documents": [
                "Apollo_Daycare_Discharge.pdf",
                "Sinus_CT_Scan.pdf"
            ],
            "risk_score": 18,
            "fraud_score": 8,
            "priority": "LOW",
            "priority_badge": "LOW",
            "status": "Approved",
            "current_step": 4,
            "status_timeline": [
                {"step": 1, "name": "Submitted", "date": "2026-08-03 11:00 AM", "completed": True, "note": "Claim uploaded by Apollo Hospital TPA desk."},
                {"step": 2, "name": "Documents Verified", "date": "2026-08-03 03:15 PM", "completed": True, "note": "Pre-auth and surgical invoice validated."},
                {"step": 3, "name": "Under Review", "date": "2026-08-04 10:00 AM", "completed": True, "note": "Daycare procedure verified under policy schedule."},
                {"step": 4, "name": "Decision", "date": "2026-08-05 02:30 PM", "completed": True, "active": True, "note": "Approved cashless authorization for ₹62,000."},
                {"step": 5, "name": "Settlement", "date": "Scheduled 2026-08-21", "completed": False, "active": False, "note": "Final settlement disbursement queued."}
            ],
            "fraud_reasons": [],
            "created_at": "2026-08-03"
        },
        {
            "claim_id": "CLM-2026-000149",
            "user_id": "USR-003",
            "customer_name": "Vikram Malhotra",
            "customer_email": "vikram.m@example.com",
            "policy_number": "POL-2026-VH-49201",
            "policy_name": "Smart Suraksha Motor Package",
            "claim_type": "Accidental Vehicle Total Loss",
            "claim_amount": 780000,
            "claim_amount_display": "₹7,80,000",
            "incident_date": "2026-08-08",
            "incident_location": "Mumbai-Pune Expressway (Night Incident)",
            "description": "Claim filed for severe night collision with roadblock. Discrepancy detected in surveyor spot photos vs garage repair estimate.",
            "documents": [
                "FIR_Copy_Expressway_Police.pdf",
                "Garage_Estimate_Sheet.pdf",
                "Surveyor_Spot_Report.pdf"
            ],
            "risk_score": 88,
            "fraud_score": 87,
            "priority": "FRAUD ALERT",
            "priority_badge": "FRAUD ALERT",
            "status": "Investigating",
            "current_step": 3,
            "status_timeline": [
                {"step": 1, "name": "Submitted", "date": "2026-08-09 09:10 AM", "completed": True, "note": "Accidental damage claim submitted online."},
                {"step": 2, "name": "Documents Verified", "date": "2026-08-10 12:45 PM", "completed": True, "note": "Surveyor assigned to inspect vehicle at workshop."},
                {"step": 3, "name": "Under Review", "date": "2026-08-11 04:30 PM", "completed": False, "active": True, "note": "AI Fraud Engine triggered: Duplicate claim pattern and suspicious garage estimate mismatch."},
                {"step": 4, "name": "Decision", "date": "Pending Forensic Inspection", "completed": False, "active": False, "note": "Referred to Special Investigation Unit (SIU)."},
                {"step": 5, "name": "Settlement", "date": "Frozen", "completed": False, "active": False, "note": "Hold placed pending SIU clearance."}
            ],
            "fraud_reasons": [
                "Duplicate claim pattern detected across insurer database",
                "Unusually high claim amount (92% of IDV) within 15 days of policy renewal",
                "Multiple recent claims across motor & health segments (2 claims in 30 days)",
                "Discrepancy between police report timestamp and telemetry data"
            ],
            "created_at": "2026-08-09"
        }
    ],
    "payments": [
        {
            "transaction_id": "TXN-2026-98124",
            "policy_number": "POL-2026-LI-10492",
            "user_id": "USR-001",
            "user_name": "Rajesh Sharma",
            "policy_name": "Smart Jeevan Raksha Term Plan",
            "amount": 14500,
            "payment_mode": "Net Banking (SBI)",
            "date": "2025-04-01",
            "status": "Successful",
            "receipt_no": "REC-884210"
        },
        {
            "transaction_id": "TXN-2026-98125",
            "policy_number": "POL-2026-HL-28491",
            "user_id": "USR-001",
            "user_name": "Rajesh Sharma",
            "policy_name": "Smart Arogya Sanjeevani Health Shield",
            "amount": 18200,
            "payment_mode": "UPI (HDFC Bank)",
            "date": "2025-06-15",
            "status": "Successful",
            "receipt_no": "REC-884211"
        },
        {
            "transaction_id": "TXN-2026-98126",
            "policy_number": "POL-2026-FM-50291",
            "user_id": "USR-002",
            "user_name": "Priya Patel",
            "policy_name": "Smart Parivar Sampurna Shield",
            "amount": 27500,
            "payment_mode": "Credit Card (ICICI)",
            "date": "2025-01-10",
            "status": "Successful",
            "receipt_no": "REC-884212"
        },
        {
            "transaction_id": "TXN-2026-98127",
            "policy_number": "POL-2026-RT-39401",
            "user_id": "USR-003",
            "user_name": "Vikram Malhotra",
            "policy_name": "Smart Pension Vriddhi Retirement Fund",
            "amount": 60000,
            "payment_mode": "NEFT Corporate",
            "date": "2025-11-01",
            "status": "Successful",
            "receipt_no": "REC-884213"
        }
    ],
    "notifications": [
        {
            "id": "NOTIF-01",
            "user_id": "USR-001",
            "title": "Claim CLM-2026-000145 Update",
            "message": "Your hospitalization claim is currently in Under Review stage. Our medical officer is examining the pharmacy bills.",
            "timestamp": "2026-07-25 11:30 AM",
            "type": "claim",
            "read": False
        },
        {
            "id": "NOTIF-02",
            "user_id": "USR-001",
            "title": "Premium Renewal Reminder",
            "message": "Policy POL-2026-VH-49201 is in Grace Period. Pay before 09-Sep-2026 to avoid policy lapse.",
            "timestamp": "2026-08-10 09:00 AM",
            "type": "policy",
            "read": False
        },
        {
            "id": "NOTIF-03",
            "user_id": "USR-001",
            "title": "Tax Certificate Available",
            "message": "Your Section 80C & 80D tax exemption certificates for FY 2025-26 are ready for download.",
            "timestamp": "2026-05-01 10:00 AM",
            "type": "system",
            "read": True
        }
    ]
}

class Database:
    def __init__(self):
        self.file_path = DB_FILE
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        self._save(DEFAULT_DATA)
        return json.loads(json.dumps(DEFAULT_DATA))

    def _save(self, data=None):
        if data is None:
            data = self.data
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_user_by_id(self, user_id):
        for u in self.data["users"]:
            if u["id"] == user_id:
                return u
        return None

    def get_user_by_email_or_username(self, identifier):
        for u in self.data["users"]:
            if u["email"].lower() == identifier.lower() or u.get("username", "").lower() == identifier.lower():
                return u
        return None

    def get_all_users(self):
        return self.data["users"]

    def add_user(self, user_dict):
        user_dict["id"] = f"USR-{len(self.data['users']) + 1:03d}"
        user_dict["status"] = "Active"
        user_dict["created_at"] = datetime.now().strftime("%Y-%m-%d")
        self.data["users"].append(user_dict)
        self._save()
        return user_dict

    def update_user(self, user_id, updates):
        for u in self.data["users"]:
            if u["id"] == user_id:
                u.update(updates)
                self._save()
                return u
        return None

    def get_catalog(self):
        return self.data["policies_catalog"]

    def get_catalog_item(self, policy_id):
        for p in self.data["policies_catalog"]:
            if p["id"] == policy_id:
                return p
        return None

    def add_catalog_policy(self, policy_data):
        policy_data["id"] = f"POL-CAT-{len(self.data['policies_catalog']) + 1:02d}"
        if "status" not in policy_data:
            policy_data["status"] = "Active"
        self.data["policies_catalog"].append(policy_data)
        self._save()
        return policy_data

    def get_user_policies(self, user_id=None):
        if user_id:
            return [p for p in self.data["user_policies"] if p["user_id"] == user_id]
        return self.data["user_policies"]

    def get_policy_by_number(self, pol_no):
        for p in self.data["user_policies"]:
            if p["policy_number"] == pol_no:
                return p
        return None

    def add_user_policy(self, policy_record):
        self.data["user_policies"].append(policy_record)
        self._save()
        return policy_record

    def get_claims(self, user_id=None):
        if user_id:
            return [c for c in self.data["claims"] if c["user_id"] == user_id]
        return self.data["claims"]

    def get_claim_by_id(self, claim_id):
        for c in self.data["claims"]:
            if c["claim_id"].upper() == claim_id.upper().strip():
                return c
        return None

    def add_claim(self, claim_data):
        next_num = len(self.data["claims"]) + 145
        claim_data["claim_id"] = f"CLM-2026-{next_num:06d}"
        claim_data["created_at"] = datetime.now().strftime("%Y-%m-%d")
        claim_data["current_step"] = 1
        
        now_str = datetime.now().strftime("%Y-%m-%d %I:%M %p")
        claim_data["status_timeline"] = [
            {"step": 1, "name": "Submitted", "date": now_str, "completed": True, "note": "Claim registered online by policyholder."},
            {"step": 2, "name": "Documents Verified", "date": "In Progress", "completed": False, "active": True, "note": "Verification of medical records and invoices in queue."},
            {"step": 3, "name": "Under Review", "date": "Upcoming", "completed": False, "active": False, "note": "Underwriting assessment."},
            {"step": 4, "name": "Decision", "date": "Upcoming", "completed": False, "active": False, "note": "Adjudication decision."},
            {"step": 5, "name": "Settlement", "date": "Upcoming", "completed": False, "active": False, "note": "Disbursement."}
        ]
        
        self.data["claims"].insert(0, claim_data)
        self._save()
        return claim_data

    def update_claim_status(self, claim_id, new_status, step=None, note=None):
        claim = self.get_claim_by_id(claim_id)
        if claim:
            claim["status"] = new_status
            if step is not None:
                claim["current_step"] = step
                now_str = datetime.now().strftime("%Y-%m-%d %I:%M %p")
                for item in claim.get("status_timeline", []):
                    if item["step"] < step:
                        item["completed"] = True
                        item["active"] = False
                    elif item["step"] == step:
                        item["completed"] = False
                        item["active"] = True
                        item["date"] = now_str
                        if note:
                            item["note"] = note
                    else:
                        item["completed"] = False
                        item["active"] = False
            self._save()
            return claim
        return None

    def get_payments(self, user_id=None):
        if user_id:
            return [p for p in self.data["payments"] if p["user_id"] == user_id]
        return self.data["payments"]

    def add_payment(self, payment_data):
        payment_data["transaction_id"] = f"TXN-2026-{len(self.data['payments']) + 98128}"
        payment_data["date"] = datetime.now().strftime("%Y-%m-%d")
        payment_data["status"] = "Successful"
        payment_data["receipt_no"] = f"REC-{len(self.data['payments']) + 884214}"
        self.data["payments"].append(payment_data)
        self._save()
        return payment_data

    def get_notifications(self, user_id):
        return [n for n in self.data.get("notifications", []) if n["user_id"] == user_id]

db = Database()
