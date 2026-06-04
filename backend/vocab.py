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
        "A high-fidelity, professional documentary-style photograph of a modern smartphone resting on a wooden desk, "
        "showing a loading spinner and a low bandwidth gauge on a speed test application. In the soft, blurry background, "
        "a telecom cellular transmission tower is visible against a twilight sky. Volumetric lighting, shallow depth of field, "
        "realistic textures, sharp focus, 8k resolution."
    ),
    "no_signal": (
        "A detailed close-up photograph of a sleek smartphone screen held in a hand, showing a 'No Service' message "
        "and empty network signal bars. An out-of-focus telecom cellular tower stands in the distant background under overcast weather. "
        "Moody natural lighting, shallow depth of field, highly detailed, realistic, 8k resolution."
    ),
    "call_drop": (
        "A candid documentary-style photograph of a frustrated person looking at a smartphone displaying a 'Call Failed' screen. "
        "A glowing red disconnected call icon is visible. Indoor ambient light, clean cinematic tones, highly realistic, "
        "detailed textures, sharp focus, 8k resolution."
    ),
    "router_issue": (
        "A professional product photograph of a modern Wi-Fi home router on a shelf. A single glowing red warning light "
        "blinks next to the internet status icon. Detailed ethernet cables are connected to the back. Soft studio lighting, "
        "realistic plastic and metallic textures, clean composition, 8k resolution."
    ),
    "billing_issue": (
        "A clean, professional flat lay photograph of a modern workspace featuring a tablet displaying a telecom invoice spreadsheet, "
        "a credit card, and a smartphone showing a warning payment notification. Natural soft side lighting, sharp details, "
        "organized desk setup, realistic materials, 8k resolution."
    ),
    "sim_issue": (
        "A detailed macro photograph of a gold-plated nano SIM card being inserted into a smartphone SIM tray with a metal ejector pin. "
        "Crisp focus on the SIM card metallic circuits, soft ambient studio lighting, highly detailed textures, realistic metallic reflection."
    ),
    "general_telecom": (
        "A professional documentary-style photograph showing telecom customer service infrastructure, a neat modern server rack cabinet "
        "with blue blinking LED status lights, and a support technician's workspace in a clean environment. Soft technical illumination, "
        "high fidelity, 8k resolution."
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