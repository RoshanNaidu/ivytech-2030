"""Project identity — Single source of truth for the StudyBuddy prototype.

Every page and AI prompt reads from here so the entire app re-themes itself
when these values change.
"""

TEAM_NAME = "Innovation Squad"
PRODUCT_NAME = "StudyBuddy"
TAGLINE = "Plain-language study help, any hour, on any phone."

# Strategic Plan 2030 pillar
PILLAR = "Academic & Instructional Quality"

# Statewide strategy (Strategic Plan 2030)
STRATEGY = "Ensure Consistent Quality Across Learning Modalities"

# The person we serve
PERSONA = "Lena — online working adult, ESL, phone-only, studies 11 pm–1 am"
PROBLEM = (
    "Dense academic readings on a small phone screen, no plain-language version, "
    "no way to check understanding before the graded quiz, tutoring closed by 9 pm."
)

# 2030 outcome metric
# ASSUMPTION: OUTCOME_BASELINE = 62.0 % is the assumed current online-course completion rate.
# This must be confirmed with actual Ivy Tech data once it is provided on challenge day.
# Source once confirmed: Ivy Tech semester-end completion records for online sections.
OUTCOME_METRIC = "Online course completion rate"
OUTCOME_BASELINE = 62.0      # ASSUMPTION — replace with real data on challenge day
OUTCOME_TARGET = 70.0        # 2030 target (8-point lift)
OUTCOME_UNIT = "%"

# Statewide scale facts (Ivy Tech press release, Jul 2026). Used by the Impact page.
STATEWIDE_HEADCOUNT = 215_000
CAMPUSES = 19

# Accent colour used across charts.
ACCENT = "#00843D"

# Languages supported for summary/questions output.
# Limited to languages IBM Granite 3.3 handles natively.
# Each entry: (display_label, BCP-47 tag for speechSynthesis)
SUPPORTED_LANGUAGES: list[tuple[str, str]] = [
    ("English",    "en-US"),
    ("Spanish",    "es-ES"),
    ("French",     "fr-FR"),
    ("Portuguese", "pt-PT"),
    ("Arabic",     "ar-SA"),
    ("Chinese",    "zh-CN"),
    ("Japanese",   "ja-JP"),
    ("Korean",     "ko-KR"),
    ("German",     "de-DE"),
    ("Italian",    "it-IT"),
]

# Reading levels offered to the user.
READING_LEVELS: list[str] = ["Simple", "Standard"]
