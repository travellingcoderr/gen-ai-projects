from app.services.travel.state import TravelState


class AnalysisAgent:
    def run(self, state: TravelState) -> TravelState:
        budget = state["budget_usd"]
        interests = [item.lower() for item in state["interests"]]
        ranked: list[dict[str, object]] = []

        for property_item in state["property_candidates"]:
            score = 70.0
            pros: list[str] = []
            cons: list[str] = []

            total_cost = int(property_item["total_estimated_usd"])
            rating = float(property_item["rating"])
            amenities = [str(item).lower() for item in property_item.get("amenities", [])]

            if total_cost <= budget * 0.75:
                score += 12
                pros.append("Comfortably within stay budget.")
            elif total_cost <= budget:
                score += 6
                pros.append("Fits within stated budget.")
            else:
                score -= 14
                cons.append("Stay cost may exceed your target budget.")

            if rating >= 4.7:
                score += 10
                pros.append("Strong guest rating.")
            elif rating < 4.5:
                score -= 5
                cons.append("Lower rating than top alternatives.")

            if interests and any(interest in amenity for interest in interests for amenity in amenities):
                score += 8
                pros.append("Amenities align with your stated interests.")
            elif interests:
                cons.append("Interest match is weaker than a tailored listing.")

            ranked.append(
                {
                    **property_item,
                    "match_score": round(max(0.0, min(score, 99.0)), 1),
                    "pros": pros or ["Balanced option for a general traveler."],
                    "cons": cons or ["No major issues found from the current tool output."],
                }
            )

        ranked.sort(key=lambda item: float(item["match_score"]), reverse=True)
        return {
            **state,
            "top_properties": ranked[:10],
        }
