import re

class Extractor:
    """
    Etapa 1: Extracción de información usando Expresiones Regulares.
    """
    def __init__(self):
        self.patterns = {
            "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            "phone": r"\+?\d[\d\s\-()]{7,}\d",
            "years_experience": r"(\d+)\s*(?:years?|años?)\s*(?:of\s*)?(?:experience|experiencia)",
            "skills": r"\b(?:JS|Javascript|javascript|React\.js|ReactJS|react|NodeJS|Node\.js|node|Postgres|PostgreSQL|postgres|Python|Pandas|pandas|NumPy|numpy|Scikit-learn|sklearn|scikit learn|TensorFlow|Tensor Flow|tensorflow|PyTorch|Py Torch|pytorch|SQL|Git|Docker|MongoDB|REST API|Tableau|Power BI|Java|R)\b"
        }

    def extract(self, text: str) -> dict:
        extracted = {
            "email": None,
            "phone": None,
            "years_experience": 0,
            "raw_skills": []
        }

        email_match = re.search(self.patterns["email"], text)
        if email_match:
            extracted["email"] = email_match.group(0)

        phone_match = re.search(self.patterns["phone"], text)
        if phone_match:
            extracted["phone"] = phone_match.group(0)

        exp_match = re.search(self.patterns["years_experience"], text, re.IGNORECASE)
        if exp_match:
            extracted["years_experience"] = int(exp_match.group(1))

        skills_found = re.findall(self.patterns["skills"], text, re.IGNORECASE)
        extracted["raw_skills"] = list(dict.fromkeys(skills_found))

        return extracted