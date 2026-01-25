import pytest
from datetime import date


class TestMortgageEndpoints:
    """Tests for mortgage CRUD endpoints."""

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_create_mortgage(self, client, sample_mortgage_data):
        """Test creating a new mortgage."""
        response = client.post("/api/v1/mortgages", json=sample_mortgage_data)
        assert response.status_code == 201
        data = response.json()
        assert data["loan_amount"] == sample_mortgage_data["loan_amount"]
        assert data["state"] == "CA"
        assert "id" in data
        assert "created_at" in data

    def test_list_mortgages_empty(self, client):
        """Test listing mortgages when none exist."""
        response = client.get("/api/v1/mortgages")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_mortgages(self, client, sample_mortgage_data):
        """Test listing mortgages."""
        # Create a mortgage first
        client.post("/api/v1/mortgages", json=sample_mortgage_data)

        response = client.get("/api/v1/mortgages")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1

    def test_get_mortgage(self, client, sample_mortgage_data):
        """Test getting a specific mortgage."""
        # Create first
        create_response = client.post("/api/v1/mortgages", json=sample_mortgage_data)
        mortgage_id = create_response.json()["id"]

        response = client.get(f"/api/v1/mortgages/{mortgage_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == mortgage_id
        assert data["loan_amount"] == sample_mortgage_data["loan_amount"]

    def test_get_mortgage_not_found(self, client):
        """Test getting a non-existent mortgage."""
        response = client.get("/api/v1/mortgages/9999")
        assert response.status_code == 404

    def test_update_mortgage(self, client, sample_mortgage_data):
        """Test updating a mortgage."""
        # Create first
        create_response = client.post("/api/v1/mortgages", json=sample_mortgage_data)
        mortgage_id = create_response.json()["id"]

        # Update
        response = client.put(
            f"/api/v1/mortgages/{mortgage_id}",
            json={"current_balance": 270000, "missed_payments": 3},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["current_balance"] == 270000
        assert data["missed_payments"] == 3

    def test_delete_mortgage(self, client, sample_mortgage_data):
        """Test deleting a mortgage."""
        # Create first
        create_response = client.post("/api/v1/mortgages", json=sample_mortgage_data)
        mortgage_id = create_response.json()["id"]

        # Delete
        response = client.delete(f"/api/v1/mortgages/{mortgage_id}")
        assert response.status_code == 204

        # Verify deleted
        response = client.get(f"/api/v1/mortgages/{mortgage_id}")
        assert response.status_code == 404

    def test_create_mortgage_validation_error(self, client):
        """Test validation error for invalid mortgage data."""
        response = client.post(
            "/api/v1/mortgages",
            json={
                "loan_amount": -1000,  # Invalid
                "current_balance": 275000,
                "interest_rate": 6.5,
                "loan_term_months": 360,
                "remaining_months": 324,
                "monthly_payment": 1896.20,
                "loan_start_date": str(date.today()),
                "state": "CA",
            },
        )
        assert response.status_code == 422


class TestDashboardEndpoint:
    """Tests for payment dashboard endpoint."""

    def test_get_dashboard(self, client, sample_mortgage_data):
        """Test getting payment dashboard."""
        # Create mortgage
        create_response = client.post("/api/v1/mortgages", json=sample_mortgage_data)
        mortgage_id = create_response.json()["id"]

        response = client.get(f"/api/v1/mortgages/{mortgage_id}/dashboard")
        assert response.status_code == 200
        data = response.json()

        assert data["mortgage_id"] == mortgage_id
        assert "current_monthly_payment" in data
        assert "days_past_due" in data
        assert "total_arrears" in data
        assert "risk_level" in data
        assert "dti_ratio" in data

    def test_dashboard_risk_levels(self, client, sample_mortgage_current, sample_mortgage_critical):
        """Test dashboard shows correct risk levels."""
        # Current mortgage - should be LOW
        response1 = client.post("/api/v1/mortgages", json=sample_mortgage_current)
        id1 = response1.json()["id"]
        dashboard1 = client.get(f"/api/v1/mortgages/{id1}/dashboard").json()
        assert dashboard1["risk_level"] == "LOW"

        # Critical mortgage - should be CRITICAL
        response2 = client.post("/api/v1/mortgages", json=sample_mortgage_critical)
        id2 = response2.json()["id"]
        dashboard2 = client.get(f"/api/v1/mortgages/{id2}/dashboard").json()
        assert dashboard2["risk_level"] == "CRITICAL"


class TestScenariosEndpoint:
    """Tests for modification scenarios endpoint."""

    def test_get_scenarios(self, client, sample_mortgage_data):
        """Test getting modification scenarios."""
        # Create mortgage
        create_response = client.post("/api/v1/mortgages", json=sample_mortgage_data)
        mortgage_id = create_response.json()["id"]

        response = client.get(f"/api/v1/mortgages/{mortgage_id}/scenarios")
        assert response.status_code == 200
        data = response.json()

        assert len(data) >= 5  # At least 5 scenarios
        scenario_types = [s["scenario_type"] for s in data]
        assert "RATE_REDUCTION_1" in scenario_types
        assert "RATE_REDUCTION_2" in scenario_types
        assert "TERM_EXTENSION_10" in scenario_types
        assert "PRINCIPAL_FORBEARANCE" in scenario_types


class TestDeadlinesEndpoint:
    """Tests for foreclosure deadlines endpoint."""

    def test_get_deadlines(self, client, sample_mortgage_data):
        """Test getting foreclosure deadlines."""
        create_response = client.post("/api/v1/mortgages", json=sample_mortgage_data)
        mortgage_id = create_response.json()["id"]

        response = client.get(f"/api/v1/mortgages/{mortgage_id}/deadlines")
        assert response.status_code == 200
        data = response.json()

        assert data["state"] == "CA"
        assert data["state_name"] == "California"
        assert "foreclosure_type" in data
        assert "milestones" in data
        assert len(data["milestones"]) > 0


class TestWarningsEndpoint:
    """Tests for warnings endpoint."""

    def test_get_warnings_delinquent(self, client, sample_mortgage_data):
        """Test getting warnings for delinquent mortgage."""
        create_response = client.post("/api/v1/mortgages", json=sample_mortgage_data)
        mortgage_id = create_response.json()["id"]

        response = client.get(f"/api/v1/mortgages/{mortgage_id}/warnings")
        assert response.status_code == 200
        data = response.json()

        # Should have warnings for 2 missed payments
        assert len(data) > 0
        warning_types = [w["type"] for w in data]
        # Should have some kind of late/default warning
        assert any(
            t in warning_types for t in ["LATE_NOTICE", "DEFAULT_WARNING", "PRE_FORECLOSURE"]
        )

    def test_get_warnings_current(self, client, sample_mortgage_current):
        """Test getting warnings for current mortgage."""
        create_response = client.post("/api/v1/mortgages", json=sample_mortgage_current)
        mortgage_id = create_response.json()["id"]

        response = client.get(f"/api/v1/mortgages/{mortgage_id}/warnings")
        assert response.status_code == 200
        data = response.json()

        # Should have no critical warnings
        critical_warnings = [w for w in data if w["severity"] == "CRITICAL"]
        assert len(critical_warnings) == 0


class TestGuidanceEndpoint:
    """Tests for guidance endpoint."""

    def test_get_guidance(self, client, sample_mortgage_data):
        """Test getting foreclosure prevention guidance."""
        create_response = client.post("/api/v1/mortgages", json=sample_mortgage_data)
        mortgage_id = create_response.json()["id"]

        response = client.get(f"/api/v1/mortgages/{mortgage_id}/guidance")
        assert response.status_code == 200
        data = response.json()

        assert "risk_level" in data
        assert "summary" in data
        assert "immediate_steps" in data
        assert "resources" in data
        assert len(data["immediate_steps"]) > 0
        assert len(data["resources"]) > 0

    def test_guidance_has_lender_script(self, client, sample_mortgage_data):
        """Test that guidance includes lender script."""
        create_response = client.post("/api/v1/mortgages", json=sample_mortgage_data)
        mortgage_id = create_response.json()["id"]

        response = client.get(f"/api/v1/mortgages/{mortgage_id}/guidance")
        data = response.json()

        assert "lender_script" in data
        assert data["lender_script"] is not None
        assert "loss mitigation" in data["lender_script"].lower()
