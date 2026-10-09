import unittest
import sys
import os

# Asegurar que los módulos de src se encuentren en el path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from extractor import Extractor
from normalizer import Normalizer
from classifier import ProfileClassifier


class TestExtractor(unittest.TestCase):
    """Pruebas para el módulo Extractor (Regex)"""

    def setUp(self):
        self.extractor = Extractor()

    def test_extract_email(self):
        text = "Contact: wednesday.addams@example.com"
        result = self.extractor.extract(text)
        self.assertEqual(result["email"], "wednesday.addams@example.com")

    def test_extract_years_experience(self):
        text = "3 years of experience developing web applications."
        result = self.extractor.extract(text)
        self.assertEqual(result["years_experience"], 3)

    def test_extract_skills(self):
        text = "Skills: JS, React.js, NodeJS, Postgres, Git."
        result = self.extractor.extract(text)
        self.assertIn("JS", result["raw_skills"])
        self.assertIn("React.js", result["raw_skills"])
        self.assertIn("NodeJS", result["raw_skills"])
        self.assertIn("Postgres", result["raw_skills"])
        self.assertIn("Git", result["raw_skills"])

    def test_extract_no_email(self):
        text = "No contact info here."
        result = self.extractor.extract(text)
        self.assertIsNone(result["email"])

    def test_extract_empty_skills(self):
        text = "No technical skills mentioned."
        result = self.extractor.extract(text)
        self.assertEqual(result["raw_skills"], [])


class TestNormalizer(unittest.TestCase):
    """Pruebas para el módulo Normalizer (FST)"""

    def setUp(self):
        self.normalizer = Normalizer()

    def test_normalize_javascript(self):
        raw = ["JS", "Javascript", "javascript"]
        normalized = self.normalizer.normalize(raw)
        # Todos deben mapear a JAVASCRIPT (solo uno tras eliminar duplicados)
        self.assertEqual(normalized, ["JAVASCRIPT"])

    def test_normalize_react(self):
        raw = ["React.js", "ReactJS", "react"]
        normalized = self.normalizer.normalize(raw)
        self.assertEqual(normalized, ["REACT"])

    def test_normalize_node(self):
        raw = ["NodeJS", "Node.js", "node"]
        normalized = self.normalizer.normalize(raw)
        self.assertEqual(normalized, ["NODE_JS"])

    def test_normalize_postgres(self):
        raw = ["Postgres", "PostgreSQL", "postgres"]
        normalized = self.normalizer.normalize(raw)
        self.assertEqual(normalized, ["POSTGRESQL"])

    def test_normalize_mixed(self):
        raw = ["JS", "React.js", "NodeJS", "Postgres", "Git"]
        normalized = self.normalizer.normalize(raw)
        self.assertIn("JAVASCRIPT", normalized)
        self.assertIn("REACT", normalized)
        self.assertIn("NODE_JS", normalized)
        self.assertIn("POSTGRESQL", normalized)
        self.assertIn("GIT", normalized)

    def test_normalize_unknown_skill(self):
        raw = ["COBOL"]
        normalized = self.normalizer.normalize(raw)
        self.assertEqual(normalized, ["COBOL"])

    def test_sort_by_profile_fsd(self):
        skills = ["GIT", "POSTGRESQL", "NODE_JS", "REACT", "JAVASCRIPT"]
        sorted_skills = self.normalizer.sort_by_profile(skills, "Full Stack Developer")
        # El orden debe ser: JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, GIT
        self.assertEqual(sorted_skills[0], "JAVASCRIPT")
        self.assertEqual(sorted_skills[-1], "GIT")


class TestClassifier(unittest.TestCase):
    """Pruebas para el módulo ProfileClassifier (Autómatas)"""

    def setUp(self):
        self.classifier = ProfileClassifier()

    def test_fsd_accepted(self):
        skills = ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]
        results = self.classifier.classify(skills)
        self.assertEqual(results["Full Stack Developer"], "ACCEPTED")

    def test_fsd_rejected(self):
        skills = ["PYTHON", "PANDAS"]
        results = self.classifier.classify(skills)
        self.assertEqual(results["Full Stack Developer"], "REJECTED")

    def test_mle_accepted(self):
        skills = ["PYTHON", "PANDAS", "SCIKIT_LEARN", "SQL", "GIT"]
        results = self.classifier.classify(skills)
        self.assertEqual(results["Machine Learning Engineer"], "ACCEPTED")

    def test_mle_rejected(self):
        skills = ["JAVASCRIPT", "REACT"]
        results = self.classifier.classify(skills)
        self.assertEqual(results["Machine Learning Engineer"], "REJECTED")

    def test_backend_accepted(self):
        skills = ["PYTHON", "DJANGO", "POSTGRESQL", "REST_API", "DOCKER", "GIT"]
        results = self.classifier.classify(skills)
        self.assertEqual(results["Backend Developer"], "ACCEPTED")

    def test_data_scientist_accepted(self):
        skills = ["PYTHON", "PANDAS", "SCIKIT_LEARN", "SQL", "TABLEAU", "GIT"]
        results = self.classifier.classify(skills)
        self.assertEqual(results["Data Scientist"], "ACCEPTED")


class TestEndToEnd(unittest.TestCase):
    """Pruebas de integración del pipeline completo"""

    def setUp(self):
        self.extractor = Extractor()
        self.normalizer = Normalizer()
        self.classifier = ProfileClassifier()

    def test_full_pipeline_wednesday(self):
        text = """
        WEDNESDAY ADDAMS
        3 years of experience developing web applications.
        Email: wednesday.addams@example.com
        Technical Skills: JS, React.js, NodeJS, Postgres, Git.
        """
        # Extracción
        extracted = self.extractor.extract(text)
        self.assertIn("JS", extracted["raw_skills"])

        # Normalización
        normalized = self.normalizer.normalize(extracted["raw_skills"])
        self.assertIn("JAVASCRIPT", normalized)

        # Clasificación
        sorted_skills = self.normalizer.sort_by_profile(normalized, "Full Stack Developer")
        results = self.classifier.classify(sorted_skills)
        self.assertEqual(results["Full Stack Developer"], "ACCEPTED")

    def test_full_pipeline_mary(self):
        text = """
        MARY JANE WATSON
        2 years of experience developing predictive models.
        Technical Skills: Python, Pandas, NumPy, Scikit-learn, TensorFlow, SQL, Git.
        """
        extracted = self.extractor.extract(text)
        normalized = self.normalizer.normalize(extracted["raw_skills"])
        sorted_skills = self.normalizer.sort_by_profile(normalized, "Machine Learning Engineer")
        results = self.classifier.classify(sorted_skills)
        self.assertEqual(results["Machine Learning Engineer"], "ACCEPTED")


if __name__ == "__main__":
    unittest.main()