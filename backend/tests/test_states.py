import pytest
from app.services.states import StateService
from app.schemas.mortgage import ForeclosureType


class TestStateService:
    """Tests for StateService."""

    def test_get_state_california(self):
        """Test getting California state info."""
        state = StateService.get_state("CA")
        assert state is not None
        assert state.code == "CA"
        assert state.name == "California"
        assert state.foreclosure_type == ForeclosureType.NON_JUDICIAL

    def test_get_state_new_york(self):
        """Test getting New York state info."""
        state = StateService.get_state("NY")
        assert state is not None
        assert state.code == "NY"
        assert state.name == "New York"
        assert state.foreclosure_type == ForeclosureType.JUDICIAL

    def test_get_state_texas(self):
        """Test getting Texas state info."""
        state = StateService.get_state("TX")
        assert state is not None
        assert state.foreclosure_type == ForeclosureType.NON_JUDICIAL
        # Texas is one of the fastest foreclosure states
        assert state.timeline_days_min < 60

    def test_get_state_lowercase(self):
        """Test case-insensitive state lookup."""
        state = StateService.get_state("ca")
        assert state is not None
        assert state.code == "CA"

    def test_get_state_invalid(self):
        """Test invalid state code returns None."""
        state = StateService.get_state("XX")
        assert state is None

    def test_get_all_states(self):
        """Test getting all states."""
        states = StateService.get_all_states()
        assert len(states) == 51  # 50 states + DC
        # Should be sorted by name
        assert states[0].name == "Alabama"
        assert states[-1].name == "Wyoming"

    def test_state_has_timeline(self):
        """Test that all states have valid timelines."""
        states = StateService.get_all_states()
        for state in states:
            assert state.timeline_days_min > 0
            assert state.timeline_days_max >= state.timeline_days_min

    def test_foreclosure_types_represented(self):
        """Test all foreclosure types are represented."""
        states = StateService.get_all_states()
        types = set(s.foreclosure_type for s in states)
        assert ForeclosureType.JUDICIAL in types
        assert ForeclosureType.NON_JUDICIAL in types
        assert ForeclosureType.HYBRID in types


class TestStatesEndpoint:
    """Tests for states API endpoint."""

    def test_list_states(self, client):
        """Test listing all states."""
        response = client.get("/api/v1/states")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 51
        # Check structure
        first_state = data[0]
        assert "code" in first_state
        assert "name" in first_state
        assert "foreclosure_type" in first_state
        assert "timeline_days_min" in first_state
        assert "timeline_days_max" in first_state
