TELECOM_CATEGORY_KEYWORDS = {
    "slow_internet": [
        "slow internet",
        "internet slow",
        "data slow",
        "buffering",
        "loading",
        "speed",
        "network slow",
        "connection slow",
        "සිග්නල් slow",
        "ඉන්ටර්නෙට් slow",
        "internet eka slow"
    ],
    "no_signal": [
        "no signal",
        "signal lost",
        "no coverage",
        "coverage problem",
        "network unavailable",
        "signal නැහැ",
        "සිග්නල් නැහැ",
        "network නැහැ"
    ],
    "call_drop": [
        "call drop",
        "call disconnected",
        "call failed",
        "voice breaking",
        "cannot call",
        "ඇමතුම කඩෙනවා",
        "call eka drop"
    ],
    "router_issue": [
        "router",
        "wifi",
        "wi-fi",
        "modem",
        "red light",
        "router not working",
        "wifi not working"
    ],
    "billing_issue": [
        "bill",
        "billing",
        "payment",
        "charged",
        "balance",
        "package activated",
        "wrong charge",
        "බිල්",
        "payment issue"
    ],
    "sim_issue": [
        "sim",
        "sim not working",
        "sim blocked",
        "sim registration",
        "new sim",
        "සිම්"
    ]
}


CATEGORY_PROMPTS = {
    "slow_internet": (
        "A simple realistic image of a mobile phone showing slow internet "
        "loading symbol with a telecom network tower in the background."
    ),
    "no_signal": (
        "A simple realistic image of a smartphone showing no signal bars "
        "near a telecom tower."
    ),
    "call_drop": (
        "A simple realistic image of a person experiencing a dropped phone call "
        "with a weak telecom signal icon."
    ),
    "router_issue": (
        "A simple realistic image of a Wi-Fi router with warning light and "
        "connection problem."
    ),
    "billing_issue": (
        "A simple realistic image of a mobile billing issue with invoice, "
        "payment alert, and telecom service symbols."
    ),
    "sim_issue": (
        "A simple realistic image of a SIM card problem with a smartphone "
        "and telecom support symbol."
    ),
    "general_telecom": (
        "A simple realistic image showing a telecom customer support scenario "
        "with network infrastructure."
    )
}


# New backend feature: category-based troubleshooting recommendations
CATEGORY_SOLUTIONS = {
    "slow_internet": [
        "Check mobile signal strength or Wi-Fi signal level.",
        "Restart the router or turn mobile data off and on again.",
        "Verify whether the customer has an active data package.",
        "Check for network congestion in the customer area.",
        "Escalate to the network operations team if the issue continues."
    ],
    "no_signal": [
        "Ask the customer to restart the device.",
        "Check whether the SIM is inserted correctly.",
        "Verify coverage availability in the customer location.",
        "Ask the customer to test the SIM in another device.",
        "Escalate as a possible tower or coverage issue."
    ],
    "call_drop": [
        "Check whether the issue happens in one location or everywhere.",
        "Ask the customer to restart the phone.",
        "Check signal strength during calls.",
        "Verify whether VoLTE or network mode settings are correct.",
        "Escalate if multiple users report call drops in the same area."
    ],
    "router_issue": [
        "Ask the customer to restart the router.",
        "Check router indicator lights.",
        "Verify cable and power connections.",
        "Reset router configuration only if required.",
        "Escalate for device replacement if hardware failure is suspected."
    ],
    "billing_issue": [
        "Verify the customer account balance and recent deductions.",
        "Check active packages and subscription history.",
        "Review recent payments or recharge records.",
        "Explain valid charges clearly to the customer.",
        "Escalate to billing support if incorrect charging is found."
    ],
    "sim_issue": [
        "Check whether the SIM is active.",
        "Ask the customer to reinsert the SIM.",
        "Test the SIM in another device.",
        "Verify SIM registration details.",
        "Escalate for SIM replacement if the SIM is damaged."
    ],
    "general_telecom": [
        "Collect more details about the customer issue.",
        "Check whether the issue is related to internet, signal, calls, billing, SIM, or router.",
        "Verify customer account and service status.",
        "Perform basic troubleshooting steps.",
        "Escalate to the relevant technical team if the issue is unclear."
    ]
}


def classify_telecom_category(transcript: str) -> str:
    """
    Classifies the transcript into a telecom issue category.
    """
    if not transcript:
        return "general_telecom"

    normalized_text = transcript.lower()

    for category, keywords in TELECOM_CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in normalized_text:
                return category

    return "general_telecom"


def build_prompt_from_category(category: str, transcript: str) -> str:
    """
    Builds an image generation prompt based on the telecom category.
    """
    base_prompt = CATEGORY_PROMPTS.get(category, CATEGORY_PROMPTS["general_telecom"])

    return (
        f"{base_prompt} "
        f"The customer complaint is: {transcript}. "
        f"Make the image clear, simple, professional, and easy to understand. "
        f"Do not include unreadable text. "
        f"Do not include extra confusing objects."
    )


def get_recommended_solutions(category: str) -> list[str]:
    """
    Returns recommended troubleshooting steps for the detected telecom category.
    """
    return CATEGORY_SOLUTIONS.get(category, CATEGORY_SOLUTIONS["general_telecom"])