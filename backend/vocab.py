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