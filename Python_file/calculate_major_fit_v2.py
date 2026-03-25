def calculate_major_fit_v2(mbti_scores, bf_scores):
    """
    Calculates Major Fit by integrating Personality Traits and Learning Styles.
    :param mbti_scores: dict {'I': 0-1, 'N': 0-1, 'S': 0-1, 'J': 0-1, ...} (Clarity Index)
    :param bf_scores: dict {'C': 0-1, 'O': 0-1, 'N': 0-1, ...} (Percentile)
    """
    
    # --- Feature Engineering: Learning Style Scores ---
    # 1. Structure: Systematic & Ordered (Focus on C and J)
    structure_score = (mbti_scores.get('J', 0) * 0.85) + (bf_scores['C'] * 0.95)
    
    # 2. Research: Theoretical & Analytical (Focus on N, I, and O)
    research_score = (mbti_scores.get('N', 0) * 0.80) + (mbti_scores.get('I', 0) * 0.70) + (bf_scores['O'] * 0.90)
    
    # 3. Hands-on: Practical & Applied (Focus on S and Low O)
    hands_on_score = (mbti_scores.get('S', 0) * 0.85) + ((1 - bf_scores['O']) * 0.60)

    # --- Major Recommendation Logic with Feature Boosting ---
    majors = {
        'Mechanical Engineering': {'base_mbti': ['S', 'T', 'J'], 'style': 'Hands-on', 'min_structure': 0.7},
        'Psychology': {'base_mbti': ['N', 'F'], 'style': 'Research', 'min_structure': 0.4},
        'Law': {'base_mbti': ['T', 'J'], 'style': 'Structure', 'min_structure': 0.8},
        'Data Science': {'base_mbti': ['I', 'T', 'J'], 'style': 'Research', 'min_structure': 0.6}
    }

    style_map = {
        'Structure': structure_score,
        'Research': research_score,
        'Hands-on': hands_on_score
    }

    final_recommendations = {}

    for major, criteria in majors.items():
        # Base Match: Traditional personality alignment
        base_match = sum([mbti_scores.get(trait, 0) for trait in criteria['base_mbti']]) / len(criteria['base_mbti'])
        
        # Style Match: Environmental compatibility
        style_fit = style_map[criteria['style']]
        
        # Final Integrative Score (Weighted 40% Base, 60% Style Fit)
        total_fit = (base_match * 0.4) + (style_fit * 0.6)
        
        # Stress/Persistence Logic
        status = "Good Fit"
        if criteria['min_structure'] > structure_score:
            status = "Potential Burnout Risk (Low Structure Adaptability)"
        if bf_scores['N'] > 0.7:
            status = "High Stress Warning (Emotional Resilience Low)"

        final_recommendations[major] = {
            "Total_Fit_Score": round(total_fit, 2),
            "Environmental_Fit": round(style_fit, 2),
            "Status": status
        }

    return final_recommendations

# --- Example: Testing an 'ISTJ' with High Stress ---
user_mbti = {'I': 0.8, 'S': 0.9, 'T': 0.7, 'J': 0.9}
user_bf = {'C': 0.95, 'O': 0.2, 'N': 0.8, 'A': 0.5, 'E': 0.2}

results = calculate_major_fit_v2(user_mbti, user_bf)
for major, res in results.items():
    print(f"Major: {major} | Score: {res['Total_Fit_Score']} | Style Fit: {res['Environmental_Fit']} | Note: {res['Status']}")
