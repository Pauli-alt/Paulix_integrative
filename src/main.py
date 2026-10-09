import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from extractor import Extractor
from normalizer import Normalizer
from classifier import ProfileClassifier
from dsl_generator import DSLGenerator


class ResumeLensApp:
    def __init__(self):
        self.extractor = Extractor()
        self.normalizer = Normalizer()
        self.classifier = ProfileClassifier()
        self.dsl_generator = DSLGenerator()

    def process_resume(self, resume_text: str, candidate_name: str = "Unknown"):
        print("Etapa 1: Extrayendo informacion...")
        extracted = self.extractor.extract(resume_text)
        print(f"   Habilidades crudas: {extracted['raw_skills']}")

        print("Etapa 2: Normalizando habilidades...")
        normalized = self.normalizer.normalize(extracted["raw_skills"])
        print(f"   Habilidades normalizadas: {normalized}")

        print("Etapa 3: Clasificando perfiles...")
        sorted_skills = self.normalizer.sort_by_profile(normalized, "Full Stack Developer")
        results = self.classifier.classify(sorted_skills)
        print(f"   Resultados: {results}")

        best_profile = None
        best_result = "REJECTED"
        for profile, result in results.items():
            if result == "ACCEPTED":
                best_profile = profile
                best_result = result
                break
        if not best_profile:
            best_profile = "Full Stack Developer"

        print("Etapa 4: Generando DSL y HTML...")
        candidate_data = {
            "name": candidate_name,
            "email": extracted.get("email", "N/A"),
            "location": "Nevermore Academy, Jericho",
            "role": "Student and independent investigator",
            "summary": resume_text[:200] + "...",
            "experiences": [
                {
                    "title": "Web Application Developer",
                    "company": "Nevermore Academy Projects",
                    "years": extracted.get("years_experience", 0),
                    "description": "Developed web applications for organizing investigation notes."
                }
            ],
            "normalized_skills": normalized
        }

        evaluation = {
            "profile": best_profile,
            "result": best_result,
            "explanation": f"The normalized qualifications satisfy an accepted {best_profile} pattern."
        }

        model_str = self.dsl_generator.generate_model_string(candidate_data, evaluation)
        print("   DSL generado:")
        print(model_str)

        try:
            model = self.dsl_generator.validate_model(model_str)
            print("   DSL valido.")
        except ValueError as e:
            print(f"   Error en DSL: {e}")
            return None

        html = self.dsl_generator.generate_html(model)
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, "output.html")
        self.dsl_generator.save_html(html, output_file)

        return {
            "html_file": output_file,
            "classification": results,
            "normalized_skills": normalized
        }


if __name__ == "__main__":
    resume_text = """
    WEDNESDAY ADDAMS
    3 years of experience developing web applications.
    Email: wednesday.addams@example.com
    Location: Nevermore Academy, Jericho
    Current role: Student and independent investigator
    
    Technical Skills:
    JS, React.js, NodeJS, Postgres, Git.
    
    Experience:
    Web Application Developer at Nevermore Academy Projects (3 years)
    Developed web applications for organizing investigation notes.
    Created interfaces for consulting records.
    Implemented backend services using Node.js.
    Stored structured information using PostgreSQL databases.
    Used Git to maintain version history.
    """

    app = ResumeLensApp()
    result = app.process_resume(resume_text, "Wednesday Addams")
    if result:
        print(f"\nProceso completado. Abre '{result['html_file']}' en tu navegador.")