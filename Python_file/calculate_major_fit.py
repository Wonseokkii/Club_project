#Python Simulation Code (Feature-Ready)
#This code uses a dictionary-based mapping to calculate scores for different majors based on user input.
#python
def calculate_major_fit(mbti, big_five_scores):
    """
    Calculates Success and Satisfaction scores for academic majors.
    :param mbti: string (e.g., 'ISTJ')
    :param big_five_scores: dict {'C': 0-1.0, 'N': 0-1.0, 'O': 0-1.0, 'A': 0-1.0, 'E': 0-1.0}
    :return: dict of major recommendations
    """
    # 1. Define Weights for MBTI and Big Five Traits
    mbti_weights = {
        'I': 0.75, 'E': 0.30, 'S': 0.60, 'N': 0.20,
        'T': 0.80, 'F': 0.25, 'J': 0.90, 'P': 0.15
    }
    
    # 2. Define Major Profiles (Requirement Logic)
    majors = {
        'Engineering': {'mbti_req': ['S', 'T', 'J'], 'bf_req': 'C'},
        'Psychology': {'mbti_req': ['N', 'F', 'P'], 'bf_req': 'A'},
        'Business': {'mbti_req': ['E', 'T', 'J'], 'bf_req': 'C'},
        'Arts': {'mbti_req': ['N', 'F', 'P'], 'bf_req': 'O'}
    }

    results = {}

    for major, profile in majors.items():
        # Calculate Success Score (GPA Prediction)
        mbti_score = sum([mbti_weights[trait] for trait in mbti if trait in profile['mbti_req']])
        success_score = (mbti_score * 0.4) + (big_five_scores['C'] * 0.95)
        
        # Calculate Satisfaction Score (Retention Prediction)
        # Higher Neuroticism (N) reduces satisfaction
        satisfaction_score = (mbti_score * 0.3) + ((1 - big_five_scores['N']) * 0.90)
        
        # Stress Alert Logic
        alert = "Stable"
        if success_score > 0.7 and satisfaction_score < 0.4:
            alert = "High Academic Stress Warning"
        elif success_score < 0.4:
            alert = "Low Academic Persistence Expected"

        results[major] = {
            "Success_Prob": round(success_score, 2),
            "Satisfaction_Prob": round(satisfaction_score, 2),
            "Status": alert
        }

    return results

# --- Example Usage ---
user_mbti = "ISTJ"
user_big_five = {
    'C': 0.9,  # High Conscientiousness
    'N': 0.8,  # High Neuroticism (Stress-prone)
    'O': 0.4, 'A': 0.5, 'E': 0.3
}

recommendations = calculate_major_fit(user_mbti, user_big_five)

print(f"--- Analysis for {user_mbti} ---")
for major, data in recommendations.items():
    print(f"[{major}] Success: {data['Success_Prob']}, Satisfaction Satisfaction: {data['Satisfaction_Prob']}, Note: {data['Status']}")