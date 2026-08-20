"""
Automated Test Suite for SmartInsure Platform
Tests all public pages, authentication flows, policy recommendations,
claim registration & tracking, and admin adjudication APIs.
"""
import unittest
from app import app
from database import db
from ai_engine import calculate_risk_score, get_personalized_recommendations
from fraud_engine import analyze_claim_fraud, get_fraud_analytics_summary

class TestSmartInsure(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

    def test_01_public_pages(self):
        """Verify all public facing pages render with 200 OK and proper branding."""
        routes = ['/', '/about', '/solutions', '/login', '/register', '/track']
        for route in routes:
            res = self.client.get(route)
            self.assertEqual(res.status_code, 200, f"Route {route} failed")
            self.assertTrue(b"SmartInsure" in res.data or b"SMART" in res.data)
            self.assertIn(b"Secure Today. Confident Tomorrow.", res.data)

    def test_02_customer_login_and_dashboard(self):
        """Test customer login and policyholder dashboard access."""
        res = self.client.post('/login', data={
            'identifier': 'rajesh',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Rajesh Sharma", res.data)
        self.assertIn(b"Active Policies", res.data)

    def test_03_admin_login_and_dashboard(self):
        """Test administrative login, admin sidebar, and analytics dashboard."""
        res = self.client.post('/login', data={
            'identifier': 'admin',
            'password': 'adminpassword'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"ADMINISTRATION", res.data)
        self.assertIn(b"Total Customers", res.data)

    def test_04_ai_recommendations(self):
        """Verify AI recommendation match scoring and rationale."""
        catalog = db.get_catalog()
        profile = {
            "age": 35,
            "annual_income": 1200000,
            "dependents": 2,
            "smoking": "Non-Smoker",
            "health_status": "Good"
        }
        rec = get_personalized_recommendations(profile, catalog)
        self.assertIn("risk_profile", rec)
        self.assertIn("recommendations", rec)
        self.assertTrue(len(rec["recommendations"]) > 0)
        self.assertTrue(rec["recommendations"][0]["match_score"] >= 80)

    def test_05_claim_submission_and_tracking(self):
        """Verify claim submission workflow and live tracking lookup."""
        with self.client.session_transaction() as sess:
            sess['user_id'] = 'USR-001'
            sess['role'] = 'customer'

        res = self.client.post('/submit-claim', data={
            'policy_number': 'POL-2026-HL-28491',
            'claim_type': 'Cashless Hospitalization',
            'incident_date': '2026-08-14',
            'incident_location': 'Medanta Medicity, Gurugram',
            'claim_amount': '85000',
            'description': 'Laparoscopic procedure for gall bladder treatment',
            'doc_names': 'Discharge_Note.pdf, Bills.pdf'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Track Your Claim", res.data)
        self.assertIn(b"Medanta Medicity", res.data)

    def test_06_admin_claim_adjudication_api(self):
        """Verify admin can adjudicate claim and transition status."""
        with self.client.session_transaction() as sess:
            sess['user_id'] = 'ADM-001'
            sess['role'] = 'admin'

        res = self.client.post('/api/admin/claims/CLM-2026-000145/adjudicate',
                               json={'action': 'approve', 'note': 'Approved by Senior Underwriter.'})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['claim']['status'], 'Approved')

    def test_07_admin_create_policy_api(self):
        """Verify admin can dynamically launch and register new insurance policy products."""
        with self.client.session_transaction() as sess:
            sess['user_id'] = 'ADM-001'
            sess['role'] = 'admin'

        res = self.client.post('/api/admin/policies/create', json={
            'name': 'Smart Cancer Suraksha Special Plan',
            'type': 'Health Insurance',
            'premium': 11500,
            'coverage': 3000000,
            'duration': '15 Years',
            'tagline': 'Dedicated stage 1 to 4 oncological critical protection',
            'benefits': ['100% lump sum payout on diagnosis', 'Second medical opinion included']
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['policy']['name'], 'Smart Cancer Suraksha Special Plan')

if __name__ == '__main__':
    unittest.main()
