from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"

AI_SKILLS = {
    "NLP",
    "Fine-tuning LLMs",
    "Milvus",
    "Embeddings",
    "RAG",
    "Vector Search",
    "Machine Learning",
    "Recommendation Systems",
    "Information Retrieval",
    "Semantic Search",
    "FAISS",
    "Pinecone",
}

POSITIVE_TITLE_WORDS = [
    "ai",
    "machine learning",
    "ml",
    "recommendation",
    "search",
    "data scientist",
    "nlp",
    "research engineer",
    "mlops",
    "ranking",
    "retrieval",
    "applied scientist",
]

NEGATIVE_TITLE_WORDS = [
    "marketing",
    "civil",
    "mechanical",
    "hr",
    "sales",
    "project manager",
    "business development",
    "graphic designer",
    "accountant",
]

HISTORY_WORDS = [
    "ai",
    "machine learning",
    "recommendation",
    "search",
    "retrieval",
    "ranking",
    "nlp",
    "ml",
    "data scientist",
    "applied scientist",
    "embeddings",
    "vector",
    "llm",
]


def iter_candidates(limit: int | None = None):
    path = DATA_DIR / "candidates.jsonl"
    with path.open("r", encoding="utf-8") as f:
        for index, line in enumerate(f):
            if limit is not None and index >= limit:
                break
            yield json.loads(line)


def ai_skill_count(candidate: dict) -> int:
    return sum(1 for skill in candidate["skills"] if skill.get("name") in AI_SKILLS)


def role_score(candidate: dict) -> float:
    title = candidate["profile"].get("current_title", "").lower()
    score = 0.0
    for word in POSITIVE_TITLE_WORDS:
        if word in title:
            score += 1.0
    for word in NEGATIVE_TITLE_WORDS:
        if word in title:
            score -= 1.25
    return score


def history_score(candidate: dict) -> float:
    score = 0.0
    for job in candidate["career_history"]:
        title = job.get("title", "").lower()
        description = job.get("description", "").lower()
        for word in HISTORY_WORDS:
            if word in title:
                score += 1.0
            if word in description:
                score += 0.25
    return score


def experience_score(candidate: dict) -> float:
    years = candidate["profile"].get("years_of_experience", 0)
    if 5 <= years <= 9:
        return 1.0
    if 4 <= years < 5 or 9 < years <= 11:
        return 0.75
    if years < 3:
        return 0.2
    return 0.45


def signal_score(candidate: dict) -> float:
    signal = candidate["redrob_signals"]
    score = 0.0
    if signal.get("open_to_work_flag"):
        score += 10
    score += signal.get("profile_completeness_score", 0) / 10
    score += signal.get("github_activity_score", 0)
    score += signal.get("interview_completion_rate", 0) * 10
    score += signal.get("recruiter_response_rate", 0) * 10
    score += min(signal.get("saved_by_recruiters_30d", 0), 10)
    if signal.get("last_active_date", "") >= "2026-05-01":
        score += 5
    return score


def tier(candidate: dict, role: float, history: float, skills: int) -> str:
    if role > 0:
        return "A"
    if role <= 0 and history >= 4 and skills >= 3:
        return "B"
    if history >= 2 and skills >= 2:
        return "C"
    return "D"


def score_candidate(candidate: dict) -> dict:
    role = role_score(candidate)
    history = history_score(candidate)
    skills = ai_skill_count(candidate)
    candidate_tier = tier(candidate, role, history, skills)

    tier_bonus = {"A": 2.0, "B": 1.0, "C": 0.0, "D": -1.0}[candidate_tier]
    base_score = (
        0.35 * min(skills / 6, 1)
        + 0.25 * min(history / 6, 1)
        + 0.20 * max(min(role / 3, 1), -1)
        + 0.10 * experience_score(candidate)
        + 0.10 * min(signal_score(candidate) / 100, 1)
    )

    profile = candidate["profile"]
    return {
        "candidate_id": candidate["candidate_id"],
        "score": tier_bonus + base_score,
        "tier": candidate_tier,
        "headline": profile.get("headline", ""),
        "current_title": profile.get("current_title", ""),
        "role_score": role,
        "history_score": history,
        "ai_skill_count": skills,
    }


def write_submission(rows: list[dict], output_path: Path) -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["candidate_id", "rank", "score", "reasoning"],
        )
        writer.writeheader()
        for rank, row in enumerate(rows, start=1):
            writer.writerow(
                {
                    "candidate_id": row["candidate_id"],
                    "rank": rank,
                    "score": f"{row['score']:.6f}",
                    "reasoning": (
                        f"Tier {row['tier']}: {row['current_title']} with "
                        f"{row['ai_skill_count']} AI skills and "
                        f"history score {row['history_score']:.2f}."
                    ),
                }
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=1000)
    parser.add_argument("--top", type=int, default=20)
    parser.add_argument("--output", default=str(OUTPUT_DIR / "submission.csv"))
    args = parser.parse_args()

    scored = [score_candidate(candidate) for candidate in iter_candidates(args.limit)]
    ranked = sorted(scored, key=lambda row: row["score"], reverse=True)[: args.top]

    output_path = Path(args.output)
    write_submission(ranked, output_path)

    print(f"Ranked {len(scored)} candidates")
    print(f"Wrote {output_path}")
    for rank, row in enumerate(ranked[:10], start=1):
        print(
            f"{rank:>2}. {row['candidate_id']} | {row['tier']} | "
            f"{row['score']:.4f} | {row['headline']}"
        )


if __name__ == "__main__":
    main()
