from app.rules import rules

class ForwardChainingExpertSystem:
    def __init__(self, knowledge_base):
        self.knowledge_base = knowledge_base
        self.facts = set()  # Working memory untuk menyimpan fakta
        self.inferred_diseases = []  # Conclusions yang telah diperoleh
        
    def add_facts(self, symptoms):
        """Menambahkan fakta (gejala) ke working memory"""
        if isinstance(symptoms, (list, tuple)):
            self.facts.update(symptoms)
        elif isinstance(symptoms, set):
            self.facts.update(symptoms)
        else:
            self.facts.add(symptoms)
    
    def clear_facts(self):
        """Menghapus semua fakta dari working memory"""
        self.facts.clear()
        self.inferred_diseases.clear()
    
    def forward_chaining(self):
        """
        Implementasi Forward Chaining:
        1. Mulai dengan fakta yang diketahui (gejala)
        2. Cari aturan yang dapat diaktifkan
        3. Terapkan aturan dan tambahkan kesimpulan baru
        4. Ulangi sampai tidak ada aturan baru yang dapat diterapkan
        """
        changed = True
        iteration = 0
        
        while changed and iteration < 100:  # Batasi iterasi untuk mencegah infinite loop
            changed = False
            iteration += 1
            
            # Evaluasi setiap aturan penyakit
            for disease, required_symptoms in self.knowledge_base.items():
                if disease not in [d['disease'] for d in self.inferred_diseases]:
                    # Hitung kecocokan gejala dengan aturan
                    matched_symptoms = self.facts.intersection(required_symptoms)
                    match_count = len(matched_symptoms)
                    total_required = len(required_symptoms)
                    
                    if match_count > 0:
                        confidence = round((match_count / total_required) * 100, 2)
                        
                        # Threshold untuk inferensi (bisa disesuaikan)
                        if confidence >= 40:  # Minimal 40% kecocokan
                            # Tambahkan kesimpulan baru
                            disease_info = {
                                'disease': disease,
                                'percentage': confidence,
                                'matched_symptoms': list(matched_symptoms),
                                'required_symptoms': list(required_symptoms),
                                'match_count': match_count,
                                'total_symptoms': total_required
                            }
                            
                            self.inferred_diseases.append(disease_info)
                            changed = True
                            
                            # Dalam forward chaining murni, kita bisa menambahkan
                            # fakta baru ke working memory berdasarkan kesimpulan
                            # Contoh: jika didiagnosis penyakit tertentu, 
                            # bisa menambahkan fakta "diagnosis_" + disease
                            self.facts.add(f"diagnosis_{disease.lower().replace(' ', '_')}")
        
        return self.get_diagnosis_results()
    
    def get_diagnosis_results(self):
        """Mengembalikan hasil diagnosis yang telah diurutkan"""
        if not self.inferred_diseases:
            return {
                "status": "no_diagnosis",
                "message": "Tidak ada penyakit dengan kecocokan di atas 40%.",
                "diagnoses": []
            }
        
        # Urutkan berdasarkan persentase kecocokan tertinggi
        sorted_diseases = sorted(
            self.inferred_diseases, 
            key=lambda x: x['percentage'], 
            reverse=True
        )
        
        return {
            "status": "success",
            "total_facts": len(self.facts),
            "total_diagnoses": len(sorted_diseases),
            "diagnoses": sorted_diseases
        }
    
    def explain_reasoning(self):
        """Menjelaskan proses reasoning yang dilakukan"""
        explanation = []
        explanation.append(f"Fakta yang diketahui: {list(self.facts)}")
        explanation.append(f"Jumlah aturan yang dievaluasi: {len(self.knowledge_base)}")
        
        for disease_info in self.inferred_diseases:
            exp = f"Aturan '{disease_info['disease']}' diaktifkan karena "
            exp += f"{disease_info['match_count']}/{disease_info['total_symptoms']} "
            exp += f"gejala cocok ({disease_info['percentage']}%)"
            explanation.append(exp)
        
        return explanation

def diagnose_disease(symptoms):
    """
    Fungsi utama untuk diagnosis menggunakan Forward Chaining
    
    Args:
        symptoms: list, set, atau tuple berisi gejala-gejala
    
    Returns:
        dict: Hasil diagnosis dengan informasi lengkap
    """
    # Inisialisasi expert system
    expert_system = ForwardChainingExpertSystem(rules)
    
    # Tambahkan gejala sebagai fakta awal
    expert_system.add_facts(symptoms)
    
    # Jalankan forward chaining
    results = expert_system.forward_chaining()
    
    # Tambahkan informasi tambahan
    results['input_symptoms'] = list(symptoms) if isinstance(symptoms, (set, list, tuple)) else [symptoms]
    results['reasoning'] = expert_system.explain_reasoning()
    
    return results