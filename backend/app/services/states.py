from typing import List, Optional
from app.schemas.mortgage import StateInfo, ForeclosureType


class StateService:
    """Service for state-specific foreclosure information."""

    # State foreclosure data
    # Sources: Various state statutes and legal resources
    STATES = {
        "AL": StateInfo(
            code="AL",
            name="Alabama",
            foreclosure_type=ForeclosureType.NON_JUDICIAL,
            timeline_days_min=49,
            timeline_days_max=74,
            notes="Power of sale state with 30-day notice requirement",
        ),
        "AK": StateInfo(
            code="AK",
            name="Alaska",
            foreclosure_type=ForeclosureType.NON_JUDICIAL,
            timeline_days_min=105,
            timeline_days_max=120,
            notes="Non-judicial with 90-day notice of default",
        ),
        "AZ": StateInfo(
            code="AZ",
            name="Arizona",
            foreclosure_type=ForeclosureType.NON_JUDICIAL,
            timeline_days_min=90,
            timeline_days_max=120,
            notes="Trustee sale state, 90-day minimum after recording",
        ),
        "AR": StateInfo(
            code="AR",
            name="Arkansas",
            foreclosure_type=ForeclosureType.NON_JUDICIAL,
            timeline_days_min=70,
            timeline_days_max=120,
            notes="Power of sale with statutory right of redemption",
        ),
        "CA": StateInfo(
            code="CA",
            name="California",
            foreclosure_type=ForeclosureType.NON_JUDICIAL,
            timeline_days_min=120,
            timeline_days_max=200,
            notes="Notice of default, 90-day reinstatement period, 21-day notice of sale",
        ),
        "CO": StateInfo(
            code="CO",
            name="Colorado",
            foreclosure_type=ForeclosureType.NON_JUDICIAL,
            timeline_days_min=110,
            timeline_days_max=125,
            notes="Public trustee foreclosure with 110-day minimum",
        ),
        "CT": StateInfo(
            code="CT",
            name="Connecticut",
            foreclosure_type=ForeclosureType.JUDICIAL,
            timeline_days_min=150,
            timeline_days_max=360,
            notes="Strict foreclosure state, court supervised",
        ),
        "DE": StateInfo(
            code="DE",
            name="Delaware",
            foreclosure_type=ForeclosureType.JUDICIAL,
            timeline_days_min=170,
            timeline_days_max=210,
            notes="Court action required, sheriff sale",
        ),
        "FL": StateInfo(
            code="FL",
            name="Florida",
            foreclosure_type=ForeclosureType.JUDICIAL,
            timeline_days_min=180,
            timeline_days_max=450,
            notes="Judicial foreclosure with potential delays",
        ),
        "GA": StateInfo(
            code="GA",
            name="Georgia",
            foreclosure_type=ForeclosureType.NON_JUDICIAL,
            timeline_days_min=37,
            timeline_days_max=60,
            notes="One of fastest foreclosure states, 30-day advertisement",
        ),
        "HI": StateInfo(
            code="HI",
            name="Hawaii",
            foreclosure_type=ForeclosureType.HYBRID,
            timeline_days_min=220,
            timeline_days_max=480,
            notes="Both judicial and non-judicial available",
        ),
        "ID": StateInfo(
            code="ID",
            name="Idaho",
            foreclosure_type=ForeclosureType.NON_JUDICIAL,
            timeline_days_min=120,
            timeline_days_max=150,
            notes="Deed of trust state with 120-day process",
        ),
        "IL": StateInfo(
            code="IL",
            name="Illinois",
            foreclosure_type=ForeclosureType.JUDICIAL,
            timeline_days_min=210,
            timeline_days_max=420,
            notes="Judicial only, 90-day redemption period",
        ),
        "IN": StateInfo(
            code="IN",
            name="Indiana",
            foreclosure_type=ForeclosureType.JUDICIAL,
            timeline_days_min=150,
            timeline_days_max=270,
            notes="Court supervised with 3-month redemption",
        ),
        "IA": StateInfo(
            code="IA",
            name="Iowa",
            foreclosure_type=ForeclosureType.JUDICIAL,
            timeline_days_min=160,
            timeline_days_max=300,
            notes="Judicial with mediation requirements",
        ),
        "KS": StateInfo(
            code="KS",
            name="Kansas",
            foreclosure_type=ForeclosureType.JUDICIAL,
            timeline_days_min=120,
            timeline_days_max=200,
            notes="Court process with redemption rights",
        ),
        "KY": StateInfo(
            code="KY",
            name="Kentucky",
            foreclosure_type=ForeclosureType.JUDICIAL,
            timeline_days_min=147,
            timeline_days_max=210,
            notes="Commissioner sale after court judgment",
        ),
        "LA": StateInfo(
            code="LA",
            name="Louisiana",
            foreclosure_type=ForeclosureType.JUDICIAL,
            timeline_days_min=60,
            timeline_days_max=180,
            notes="Executory process (faster) or ordinary process",
        ),
        "ME": StateInfo(
            code="ME",
            name="Maine",
            foreclosure_type=ForeclosureType.JUDICIAL,
            timeline_days_min=240,
            timeline_days_max=360,
            notes="Judicial with 90-day redemption",
        ),
        "MD": StateInfo(
            code="MD",
            name="Maryland",
            foreclosure_type=ForeclosureType.HYBRID,
            timeline_days_min=90,
            timeline_days_max=150,
            notes="Assent to decree allows faster process",
        ),
        "MA": StateInfo(
            code="MA",
            name="Massachusetts",
            foreclosure_type=ForeclosureType.NON_JUDICIAL,
            timeline_days_min=75,
            timeline_days_max=150,
            notes="Statutory power of sale, 150-day right to cure",
        ),
        "MI": StateInfo(
            code="MI",
            name="Michigan",
            foreclosure_type=ForeclosureType.NON_JUDICIAL,
            timeline_days_min=60,
            timeline_days_max=90,
            notes="Advertisement for 4 consecutive weeks",
        ),
        "MN": StateInfo(
            code="MN",
            name="Minnesota",
            foreclosure_type=ForeclosureType.NON_JUDICIAL,
            timeline_days_min=90,
            timeline_days_max=150,
            notes="Advertisement by publication, 6-month redemption",
        ),
        "MS": StateInfo(
            code="MS",
            name="Mississippi",
            foreclosure_type=ForeclosureType.NON_JUDICIAL,
            timeline_days_min=60,
            timeline_days_max=90,
            notes="Power of sale with 30-day notice",
        ),
        "MO": StateInfo(
            code="MO",
            name="Missouri",
            foreclosure_type=ForeclosureType.NON_JUDICIAL,
            timeline_days_min=60,
            timeline_days_max=90,
            notes="Deed of trust state, 20-day newspaper notice",
        ),
        "MT": StateInfo(
            code="MT",
            name="Montana",
            foreclosure_type=ForeclosureType.NON_JUDICIAL,
            timeline_days_min=120,
            timeline_days_max=150,
            notes="Small tract act or trust indenture act",
        ),
        "NE": StateInfo(
            code="NE",
            name="Nebraska",
            foreclosure_type=ForeclosureType.JUDICIAL,
            timeline_days_min=142,
            timeline_days_max=180,
            notes="Court process with notice requirements",
        ),
        "NV": StateInfo(
            code="NV",
            name="Nevada",
            foreclosure_type=ForeclosureType.NON_JUDICIAL,
            timeline_days_min=120,
            timeline_days_max=180,
            notes="Mediation required before foreclosure",
        ),
        "NH": StateInfo(
            code="NH",
            name="New Hampshire",
            foreclosure_type=ForeclosureType.NON_JUDICIAL,
            timeline_days_min=59,
            timeline_days_max=90,
            notes="Power of sale with 25-day notice",
        ),
        "NJ": StateInfo(
            code="NJ",
            name="New Jersey",
            foreclosure_type=ForeclosureType.JUDICIAL,
            timeline_days_min=270,
            timeline_days_max=450,
            notes="Fair Foreclosure Act protections, court supervised",
        ),
        "NM": StateInfo(
            code="NM",
            name="New Mexico",
            foreclosure_type=ForeclosureType.JUDICIAL,
            timeline_days_min=120,
            timeline_days_max=180,
            notes="Court supervised foreclosure",
        ),
        "NY": StateInfo(
            code="NY",
            name="New York",
            foreclosure_type=ForeclosureType.JUDICIAL,
            timeline_days_min=300,
            timeline_days_max=720,
            notes="Lengthy judicial process, settlement conferences required",
        ),
        "NC": StateInfo(
            code="NC",
            name="North Carolina",
            foreclosure_type=ForeclosureType.NON_JUDICIAL,
            timeline_days_min=90,
            timeline_days_max=120,
            notes="Power of sale with clerk hearing",
        ),
        "ND": StateInfo(
            code="ND",
            name="North Dakota",
            foreclosure_type=ForeclosureType.JUDICIAL,
            timeline_days_min=90,
            timeline_days_max=150,
            notes="Court process with notice of default",
        ),
        "OH": StateInfo(
            code="OH",
            name="Ohio",
            foreclosure_type=ForeclosureType.JUDICIAL,
            timeline_days_min=150,
            timeline_days_max=270,
            notes="Court supervised, sheriff sale",
        ),
        "OK": StateInfo(
            code="OK",
            name="Oklahoma",
            foreclosure_type=ForeclosureType.HYBRID,
            timeline_days_min=90,
            timeline_days_max=180,
            notes="Power of sale or judicial available",
        ),
        "OR": StateInfo(
            code="OR",
            name="Oregon",
            foreclosure_type=ForeclosureType.NON_JUDICIAL,
            timeline_days_min=150,
            timeline_days_max=180,
            notes="Trust deed foreclosure with 120-day notice",
        ),
        "PA": StateInfo(
            code="PA",
            name="Pennsylvania",
            foreclosure_type=ForeclosureType.JUDICIAL,
            timeline_days_min=180,
            timeline_days_max=300,
            notes="Act 91 notice required, court process",
        ),
        "RI": StateInfo(
            code="RI",
            name="Rhode Island",
            foreclosure_type=ForeclosureType.HYBRID,
            timeline_days_min=60,
            timeline_days_max=120,
            notes="Power of sale or judicial available",
        ),
        "SC": StateInfo(
            code="SC",
            name="South Carolina",
            foreclosure_type=ForeclosureType.JUDICIAL,
            timeline_days_min=150,
            timeline_days_max=240,
            notes="Court process, right of redemption",
        ),
        "SD": StateInfo(
            code="SD",
            name="South Dakota",
            foreclosure_type=ForeclosureType.HYBRID,
            timeline_days_min=90,
            timeline_days_max=150,
            notes="Power of sale or judicial available",
        ),
        "TN": StateInfo(
            code="TN",
            name="Tennessee",
            foreclosure_type=ForeclosureType.NON_JUDICIAL,
            timeline_days_min=40,
            timeline_days_max=60,
            notes="Fast power of sale, 20-day notice",
        ),
        "TX": StateInfo(
            code="TX",
            name="Texas",
            foreclosure_type=ForeclosureType.NON_JUDICIAL,
            timeline_days_min=41,
            timeline_days_max=60,
            notes="Fast foreclosure, first Tuesday of month sales",
        ),
        "UT": StateInfo(
            code="UT",
            name="Utah",
            foreclosure_type=ForeclosureType.NON_JUDICIAL,
            timeline_days_min=112,
            timeline_days_max=142,
            notes="Trust deed foreclosure with 3-month notice",
        ),
        "VT": StateInfo(
            code="VT",
            name="Vermont",
            foreclosure_type=ForeclosureType.JUDICIAL,
            timeline_days_min=210,
            timeline_days_max=300,
            notes="Strict foreclosure or judicial sale",
        ),
        "VA": StateInfo(
            code="VA",
            name="Virginia",
            foreclosure_type=ForeclosureType.NON_JUDICIAL,
            timeline_days_min=45,
            timeline_days_max=60,
            notes="Fast power of sale, 14-day newspaper notice",
        ),
        "WA": StateInfo(
            code="WA",
            name="Washington",
            foreclosure_type=ForeclosureType.NON_JUDICIAL,
            timeline_days_min=120,
            timeline_days_max=180,
            notes="Deed of trust with 90-day notice",
        ),
        "WV": StateInfo(
            code="WV",
            name="West Virginia",
            foreclosure_type=ForeclosureType.NON_JUDICIAL,
            timeline_days_min=60,
            timeline_days_max=90,
            notes="Deed of trust foreclosure",
        ),
        "WI": StateInfo(
            code="WI",
            name="Wisconsin",
            foreclosure_type=ForeclosureType.JUDICIAL,
            timeline_days_min=180,
            timeline_days_max=300,
            notes="Court supervised with redemption rights",
        ),
        "WY": StateInfo(
            code="WY",
            name="Wyoming",
            foreclosure_type=ForeclosureType.NON_JUDICIAL,
            timeline_days_min=60,
            timeline_days_max=90,
            notes="Power of sale advertising",
        ),
        "DC": StateInfo(
            code="DC",
            name="District of Columbia",
            foreclosure_type=ForeclosureType.NON_JUDICIAL,
            timeline_days_min=47,
            timeline_days_max=75,
            notes="Power of sale with mediation",
        ),
    }

    @classmethod
    def get_state(cls, code: str) -> Optional[StateInfo]:
        """Get state information by code."""
        return cls.STATES.get(code.upper())

    @classmethod
    def get_all_states(cls) -> List[StateInfo]:
        """Get all states with foreclosure information."""
        return sorted(cls.STATES.values(), key=lambda s: s.name)

    @classmethod
    def get_foreclosure_type_description(cls, ftype: ForeclosureType) -> str:
        """Get description of foreclosure type."""
        descriptions = {
            ForeclosureType.JUDICIAL: (
                "Judicial foreclosure requires court action. The lender must file "
                "a lawsuit and obtain a court judgment before selling the property. "
                "This process typically takes longer but offers more protections."
            ),
            ForeclosureType.NON_JUDICIAL: (
                "Non-judicial foreclosure does not require court involvement. The "
                "lender can foreclose using a power of sale clause in the deed of "
                "trust. This process is typically faster."
            ),
            ForeclosureType.HYBRID: (
                "Hybrid states allow both judicial and non-judicial foreclosure. "
                "The lender may choose which process to use based on the loan "
                "documents and circumstances."
            ),
        }
        return descriptions.get(ftype, "")
