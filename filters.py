# filters.py

def is_off_topic(query: str) -> bool:
    """
    Returns True if the query is NOT related to SHL assessments,
    hiring, recruitment, or candidate evaluation.
    """

    query = query.lower().strip()

    shl_keywords = [
        # General
        "assessment",
        "assessments",
        "test",
        "tests",
        "exam",
        "candidate",
        "candidates",
        "job",
        "role",
        "position",
        "hire",
        "hiring",
        "recruitment",
        "recruit",

        # Skills
        "python",
        "java",
        "sql",
        "c++",
        "excel",
        "power bi",
        "tableau",
        "aws",
        "azure",
        "sales",
        "finance",
        "marketing",
        "developer",
        "engineer",
        "analyst",
        "manager",

        # Assessment types
        "personality",
        "behavioral",
        "behavioural",
        "cognitive",
        "aptitude",
        "ability",
        "technical",
        "coding",
        "leadership",
        "communication",
        "numerical",
        "verbal",
        "reasoning",

        # SHL Products
        "shl",
        "verify",
        "opq",
        "gsa",
        "sjt",
        "mq"
    ]

    return not any(keyword in query for keyword in shl_keywords)