# from retriever import search_catalog
# from conversation import latest_user_message, previous_messages
# from comparator import compare_assessments
# from filters import is_off_topic
# from prompts import CLARIFICATION


# def process(messages):

#     latest = latest_user_message(messages).lower()
#     history = previous_messages(messages)

#     # ----------------------------------
#     # OFF TOPIC
#     # ----------------------------------

#     if is_off_topic(latest):
#         return {
#             "reply": (
#                 "I'm an SHL Assessment Assistant. "
#                 "I can only help with SHL assessments, hiring, recruitment, "
#                 "candidate evaluation, and assessment recommendations."
#             ),
#             "recommendations": [],
#             "end_of_conversation": False
#         }

#     # ----------------------------------
#     # COMPARISON
#     # ----------------------------------

#     if "compare" in latest or "difference" in latest:

#         results = search_catalog(latest, top_k=2)

#         return {
#             "reply": compare_assessments(results),
#             "recommendations": [],
#             "end_of_conversation": False
#         }

#     # ----------------------------------
#     # REFINEMENT
#     # ----------------------------------

#     if any(word in latest for word in [
#         "actually",
#         "instead",
#         "also",
#         "add",
#         "another",
#         "change"
#     ]):

#         results = search_catalog(history)

#         recommendations = []

#         for item in results:

#             recommendations.append(
#                 {
#                     "name": item["name"],
#                     "url": item["link"],
#                     "reason": f"Updated recommendation based on: {latest}"
#                 }
#             )

#         return {
#             "reply": "I've updated the recommendations based on your additional requirements.",
#             "recommendations": recommendations,
#             "end_of_conversation": True
#         }

#     # ----------------------------------
#     # CLARIFICATION
#     # ----------------------------------

#     vague_queries = [
#         "assessment",
#         "test",
#         "hire",
#         "hiring",
#         "job",
#         "candidate"
#     ]

#     has_context = any(skill in latest for skill in [

#         "python",
#         "java",
#         "sql",
#         "developer",
#         "engineer",
#         "manager",
#         "sales",
#         "finance",
#         "analyst",
#         "personality",
#         "behavioral",
#         "cognitive",
#         "leadership"

#     ])

#     if any(word in latest for word in vague_queries) and not has_context:

#         return {
#             "reply": CLARIFICATION,
#             "recommendations": [],
#             "end_of_conversation": False
#         }

#     # ----------------------------------
#     # NORMAL SEARCH
#     # ----------------------------------

#     results = search_catalog(history)

#     recommendations = []

#     for item in results:

#         recommendations.append(
#             {
#                 "name": item["name"],
#                 "url": item["link"],
#                 "reason": f"Recommended based on: {latest}"
#             }
#         )

#     return {
#         "reply": "Based on your requirements, here are the most relevant SHL assessments.",
#         "recommendations": recommendations,
#         "end_of_conversation": True
#     }
from retriever import search_catalog
import re

CLARIFICATION = "Could you provide job role, skills, and experience level?"

OFF_TOPIC = [
    "weather",
    "cricket",
    "movie",
    "politics",
    "song",
    "football",
    "ipl",
    "bitcoin",
    "crypto",
    "recipe",
    "music",
    "stock",
    "travel",
    "visa",
    "salary",
    "compensation",
    "interview tips",
    "legal",
    "employment law",
]

VAGUE = ["assessment", "test", "hire", "hiring"]

PERSONALITY = ["personality", "opq"]
COGNITIVE = ["cognitive", "aptitude"]
SKILLS = ["python", "java", "sql", "developer", "engineer", "analyst"]
SHL_SCOPE_TERMS = [
    "shl",
    "assessment",
    "test",
    "hire",
    "hiring",
    "candidate",
    "screen",
    "role",
    "job description",
    "jd",
    "personality",
    "cognitive",
    "aptitude",
    "skills",
    "opq",
    "gsa",
]


def text(messages):
    return " ".join([m["content"] for m in messages]).lower()


def is_off_topic(q):
    # Explicit blocked domains
    if any(x in q for x in OFF_TOPIC):
        return True

    # If user asks a broad non-assessment question and gives no SHL hiring signal,
    # treat it as off-topic for this assignment.
    has_scope_signal = any(x in q for x in SHL_SCOPE_TERMS)
    generic_question = bool(
        re.search(
            r"\b(what|why|how|when|where|who)\b", q
        )
    )
    return generic_question and not has_scope_signal


def is_comparison(q):
    # Accept common typo variants like "differnce"/"diffrence" as well.
    return bool(
        re.search(r"\b(compare|comparison|vs|versus|differ\w*|diff\w*)\b", q)
    )


def needs_clarification(q):
    return any(x in q for x in VAGUE) and not any(x in q for x in PERSONALITY + COGNITIVE + SKILLS)


def compare_opq_gsa():
    return {
        "reply": (
            "OPQ (Occupational Personality Questionnaire) measures personality traits "
            "like behavior, motivation, and working style. "
            "GSA (Global Skills Assessment) measures job-related skills and behavioral performance. "
            "So OPQ focuses on personality, while GSA focuses on skills."
        ),
        "recommendations": [],
        "end_of_conversation": False
    }


def process(messages):

    q = text(messages)

    # 1. OFF TOPIC
    if is_off_topic(q):
        return {
            "reply": (
                "I can only help with SHL assessments from the SHL catalog. "
                "I cannot answer non-assessment or general legal/hiring advice requests."
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # 2. CLARIFICATION
    if needs_clarification(q):
        return {
            "reply": CLARIFICATION,
            "recommendations": [],
            "end_of_conversation": False
        }

    # 3. IMPORTANT FIX: STRICT COMPARISON HANDLING
    if is_comparison(q):

        # ONLY trigger comparison for OPQ vs GSA
        if "opq" in q and "gsa" in q:
            return compare_opq_gsa()

        return {
            "reply": "Please specify which assessments you want to compare (e.g., OPQ vs GSA).",
            "recommendations": [],
            "end_of_conversation": False
        }

    # 4. NORMAL SEARCH (ONLY WHEN NOT COMPARISON)
    results = search_catalog(q, top_k=5)

    recommendations = [
        {
            "name": r.get("name", ""),
            "url": r.get("link", ""),
            "reason": f"Matched based on: {q}"
        }
        for r in results
    ]

    return {
        "reply": "Here are the most relevant SHL assessments based on your requirement.",
        "recommendations": recommendations,
        "end_of_conversation": True
    }