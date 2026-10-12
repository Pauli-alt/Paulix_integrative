class FST:
    """Implementación simple de un Transductor de Estados Finitos."""
    def __init__(self):
        self.states = set()
        self.transitions = {}  # (state, input) -> (next_state, output)
        self.initial_state = None
        self.final_states = set()

    def add_state(self):
        state = len(self.states)
        self.states.add(state)
        return state

    def add_transition(self, from_state, input_symbol, to_state, output_symbols):
        self.transitions[(from_state, input_symbol)] = (to_state, output_symbols)

    def add_initial_state(self, state):
        self.initial_state = state

    def add_final_state(self, state):
        self.final_states.add(state)

    def transduce(self, input_sequence):
        """Aplica el transductor a una secuencia de entrada."""
        results = []
        for inp in input_sequence:
            current = self.initial_state
            key = (current, inp)
            if key in self.transitions:
                next_state, output = self.transitions[key]
                results.extend(output)
        return results


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