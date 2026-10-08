from pyformlang.fst import FST

class Normalizer:
    """
    Etapa 2: Normalización usando Transductores de Estados Finitos (FST).
    """
    def __init__(self):
        self.transducers = {}
        self._build_transducers()

    def _build_transducers(self):
        self.transducers["javascript"] = self._create_transducer(
            inputs=["JS", "Javascript", "javascript"], output="JAVASCRIPT")
        self.transducers["react"] = self._create_transducer(
            inputs=["React.js", "ReactJS", "react"], output="REACT")
        self.transducers["node"] = self._create_transducer(
            inputs=["NodeJS", "Node.js", "node"], output="NODE_JS")
        self.transducers["postgres"] = self._create_transducer(
            inputs=["Postgres", "PostgreSQL", "postgres"], output="POSTGRESQL")
        self.transducers["scikit"] = self._create_transducer(
            inputs=["sklearn", "scikit learn", "Scikit-learn"], output="SCIKIT_LEARN")
        self.transducers["tensorflow"] = self._create_transducer(
            inputs=["Tensor Flow", "TensorFlow", "tensorflow"], output="TENSORFLOW")
        self.transducers["pytorch"] = self._create_transducer(
            inputs=["Py Torch", "PyTorch", "pytorch"], output="PYTORCH")
        self.transducers["pandas"] = self._create_transducer(
            inputs=["Pandas", "pandas"], output="PANDAS")
        self.transducers["numpy"] = self._create_transducer(
            inputs=["NumPy", "numpy"], output="NUMPY")

    def _create_transducer(self, inputs, output):
        fst = FST()
        q0 = fst.add_state()
        q1 = fst.add_state()
        for inp in inputs:
            fst.add_transition(q0, inp, q1, [output])
        fst.add_initial_state(q0)
        fst.add_final_state(q1)
        return fst

    def normalize(self, raw_skills: list) -> list:
        normalized = []
        for skill in raw_skills:
            found = False
            for name, fst in self.transducers.items():
                result = fst.transduce([skill])
                if result and result[0] != skill:
                    normalized.append(result[0])
                    found = True
                    break
            if not found:
                normalized.append(skill.upper())
        return list(dict.fromkeys(normalized))

    def sort_by_profile(self, skills: list, profile: str) -> list:
        orders = {
            "Full Stack Developer": [
                "JAVASCRIPT", "TYPESCRIPT", "REACT", "ANGULAR", "VUE",
                "NODE_JS", "DJANGO", "SPRING_BOOT",
                "SQL", "NOSQL", "POSTGRESQL", "MONGODB",
                "REST_API", "GIT"
            ],
            "Machine Learning Engineer": [
                "PYTHON", "PANDAS", "NUMPY",
                "SCIKIT_LEARN", "TENSORFLOW", "PYTORCH",
                "SQL", "POSTGRESQL", "GIT"
            ],
            "Backend Developer": [
                "PYTHON", "JAVA", "NODE_JS", "DJANGO", "SPRING_BOOT",
                "POSTGRESQL", "MONGODB", "REST_API", "DOCKER", "GIT"
            ],
            "Data Scientist": [
                "PYTHON", "R", "PANDAS", "NUMPY",
                "SCIKIT_LEARN", "TENSORFLOW",
                "SQL", "TABLEAU", "POWER_BI", "GIT"
            ]
        }
        order = orders.get(profile, [])
        return sorted(skills, key=lambda x: order.index(x) if x in order else len(order))