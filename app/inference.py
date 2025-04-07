from app.rules import rules

def diagnose_disease(symptoms):
    diagnosis_results = []

    for disease, required_symptoms in rules.items():
        match_count = len(symptoms.intersection(required_symptoms))
        total_required = len(required_symptoms)

        if match_count > 0:
            match_percentage = round((match_count / total_required) * 100, 2)

            if match_percentage > 40:  # Hanya ambil yang di atas 50%
                diagnosis_results.append({"disease": disease, "match_percentage": match_percentage})

    # Urutkan berdasarkan kecocokan tertinggi
    diagnosis_results.sort(key=lambda x: x["match_percentage"], reverse=True)

    if diagnosis_results:
        return {"diagnoses": diagnosis_results}
    else:
        return {"diagnoses": "Tidak ada penyakit dengan kecocokan di atas 50%."}
