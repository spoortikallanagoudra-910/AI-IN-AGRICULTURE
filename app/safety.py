import re


_CHEMICAL_TERMS = (
    r"herbicide|pesticide|fungicide|insecticide|nematicide|rodenticide|"
    r"acaricide|chemical|fumigant|defoliant"
)
_CHEMICAL_ACTIONS = (
    r"mix|mixing|mixed|combine|combining|tank[- ]?mix|dose|dosage|rate|"
    r"apply|application|spray|spraying|dilute|dilution|boom"
)

_VET_TERMS = (
    r"\b(dose|dosage|mg/?kg|inject|injection|vaccinate|vaccine|vaccination|"
    r"antibiotic|anthelmintic|dewormer|drench|medicine|drug|ivermectin|"
    r"oxytetracycline|penicillin)\b"
)
_VET_CONTEXT = (
    r"\b(cattle|cow|cows|buffalo|goat|goats|sheep|poultry|chicken|chickens|"
    r"bird|birds|pig|pigs|swine|animal|animals|livestock|herd|flock|calf|"
    r"calves|lamb|lambs|kid|kids)\b"
)


def screen_safety(message: str) -> list[dict]:
    """Return safety findings for a free-text user message.

    Findings are advisory banners shown alongside the assistant answer. They
    never block the request; they remind the user to follow product labels,
    regulations, and professional advice.
    """
    text = (message or "").lower()
    findings: list[dict] = []

    chemical_hit = re.search(_CHEMICAL_TERMS, text)
    chemical_action = re.search(_CHEMICAL_ACTIONS, text)

    if chemical_hit and chemical_action:
        findings.append(
            {
                "category": "chemical_safety",
                "severity": "warning",
                "message": (
                    "Pesticide and fertilizer mixing, dosing, and application "
                    "must follow the current product label and local "
                    "regulations. Confirm tank-mix compatibility, correct "
                    "rate, PPE, pre-harvest interval, and re-entry interval "
                    "before applying, and consult a licensed extension or "
                    "agronomy specialist."
                ),
            }
        )

    if re.search(_VET_TERMS, text) and re.search(_VET_CONTEXT, text):
        findings.append(
            {
                "category": "veterinary_safety",
                "severity": "critical",
                "message": (
                    "Drug selection and dosing for animals must be set by a "
                    "licensed veterinarian who can examine the animal. Do not "
                    "dose from a description or photo alone; follow the label "
                    "dose and milk/meat withdrawal periods, and seek urgent "
                    "veterinary review if welfare appears compromised."
                ),
            }
        )

    return findings
