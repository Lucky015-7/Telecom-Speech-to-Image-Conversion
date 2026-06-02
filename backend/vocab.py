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


CATEGORY_SOLUTIONS = {
    "slow_internet": [
        "Advise the customer to clear browser cache and cookies.",
        "Perform a speed test on fast.com or speedtest.net to confirm current bandwidth.",
        "Verify if customer's package high-speed data quota has been exhausted.",
        "Recommend disconnecting background applications and other devices from the network."
    ],
    "no_signal": [
        "Ask the customer to toggle Airplane Mode ON for 10 seconds, then turn it OFF to force network re-registration.",
        "Check the operator database for any localized cell tower outages or maintenance in their region.",
        "Advise the customer to clean the SIM card gold contact plate and re-insert the SIM tray.",
        "Check if the device network settings are set to Auto-Select Operator."
    ],
    "call_drop": [
        "Advise the customer to switch their cellular network preferences from 4G/LTE to 3G/2G if indoor reception is weak.",
        "Perform a subscriber profile reset (VLR reset) via the operator control panel.",
        "Check if VoLTE (Voice over LTE) is enabled on the device and is supported in the current location.",
        "Advise customer to check for physical obstructions or high-interference appliances nearby."
    ],
    "router_issue": [
        "Advise the customer to unplug the router's power cable for 30 seconds, then reconnect (Power Cycle).",
        "Instruct the customer to verify if the fiber/DSL broadband cable is firmly plugged into the WAN/DSL port.",
        "Check router status lights: if the PON/Internet light is blinking red, register an optical line degradation ticket.",
        "Recommend restoring router factory settings only as a last resort."
    ],
    "billing_issue": [
        "Retrieve customer's recent invoice history and verify active package subscription fees.",
        "Check for any overlapping auto-renewal services or double payments in the billing ledger.",
        "Verify if any international roaming or premium SMS services were triggered during the current cycle.",
        "Explain billing cycle breakdown and due dates to the customer."
    ],
    "sim_issue": [
        "Advise the customer to check the SIM card in another handset to isolate hardware faults.",
        "Verify if SIM card status is active, suspended, or blocked (due to incorrect PIN/PUK entries).",
        "If hardware is faulty, initiate a SIM Replacement request with standard fee waiver.",
        "Instruct the customer on SIM activation steps."
    ],
    "general_telecom": [
        "Perform basic client information verification.",
        "Log a detailed description of the incident in the support CRM ticketing system.",
        "Escalate to Level 2 technical engineering queue if issue is unresolved after primary checks."
    ]
}


def get_recommended_solutions(category: str) -> list[str]:
    """
    Returns list of troubleshooting solutions mapped to a telecom category.
    """
    return CATEGORY_SOLUTIONS.get(category, CATEGORY_SOLUTIONS["general_telecom"])