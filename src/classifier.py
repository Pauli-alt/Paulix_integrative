# src/classifier.py
# Implementación manual de DFA (sin pyformlang)

class DFA:
    """Implementación simple de un Autómata Finito Determinista."""
    def __init__(self):
        self.states = set()
        self.transitions = {}  # (state, symbol) -> state
        self.initial_state = None
        self.final_states = set()

    def add_state(self):
        state = len(self.states)
        self.states.add(state)
        return state

    def add_transition(self, from_state, symbol, to_state):
        self.transitions[(from_state, symbol)] = to_state

    def add_initial_state(self, state):
        self.initial_state = state

    def add_final_state(self, state):
        self.final_states.add(state)

    def accepts(self, input_sequence):
        """Verifica si la secuencia es aceptada por el autómata."""
        current = self.initial_state
        for symbol in input_sequence:
            key = (current, symbol)
            if key in self.transitions:
                current = self.transitions[key]
            else:
                # Si no hay transición, intentar avanzar ignorando símbolos no relevantes
                continue
        return current in self.final_states


class ProfileClassifier:
    """
    Etapa 3: Reconocimiento de patrones usando Autómatas Finitos.
    """
    def __init__(self):
        self.automata = {}
        self._build_automata()

    def _build_automata(self):
        self.automata["Machine Learning Engineer"] = self._build_mle_automaton()
        self.automata["Full Stack Developer"] = self._build_fsd_automaton()
        self.automata["Backend Developer"] = self._build_backend_automaton()
        self.automata["Data Scientist"] = self._build_data_scientist_automaton()

    def _build_mle_automaton(self):
        dfa = DFA()
        q0, q1, q2, q3, q4, q5 = [dfa.add_state() for _ in range(6)]
        dfa.add_transition(q0, "PYTHON", q1)
        dfa.add_transition(q1, "PANDAS", q2)
        dfa.add_transition(q1, "NUMPY", q2)
        dfa.add_transition(q2, "SCIKIT_LEARN", q3)
        dfa.add_transition(q2, "TENSORFLOW", q3)
        dfa.add_transition(q2, "PYTORCH", q3)
        dfa.add_transition(q3, "SQL", q4)
        dfa.add_transition(q3, "POSTGRESQL", q4)
        dfa.add_transition(q4, "GIT", q5)
        dfa.add_initial_state(q0)
        dfa.add_final_state(q5)
        return dfa

    def _build_fsd_automaton(self):
        """
        Full Stack Developer:
        Paso 1: JAVASCRIPT o TYPESCRIPT
        Paso 2: REACT, ANGULAR o VUE
        Paso 3: NODE_JS, DJANGO o SPRING_BOOT
        Paso 4: SQL, NOSQL, POSTGRESQL o MONGODB
        Paso 5 (opcional): REST_API
        Paso 6: GIT (obligatorio al final)
        """
        dfa = DFA()
        q0, q1, q2, q3, q4, q5, q6 = [dfa.add_state() for _ in range(7)]

        # Paso 1: Lenguaje frontend
        dfa.add_transition(q0, "JAVASCRIPT", q1)
        dfa.add_transition(q0, "TYPESCRIPT", q1)

        # Paso 2: Framework frontend
        dfa.add_transition(q1, "REACT", q2)
        dfa.add_transition(q1, "ANGULAR", q2)
        dfa.add_transition(q1, "VUE", q2)

        # Paso 3: Framework backend
        dfa.add_transition(q2, "NODE_JS", q3)
        dfa.add_transition(q2, "DJANGO", q3)
        dfa.add_transition(q2, "SPRING_BOOT", q3)

        # Paso 4: Base de datos
        dfa.add_transition(q3, "SQL", q4)
        dfa.add_transition(q3, "NOSQL", q4)
        dfa.add_transition(q3, "POSTGRESQL", q4)
        dfa.add_transition(q3, "MONGODB", q4)

        # Paso 5: REST API (opcional, pero si está debe ir antes de GIT)
        dfa.add_transition(q4, "REST_API", q5)

        # Paso 6: GIT - se acepta tanto desde q4 (sin REST_API) como desde q5 (con REST_API)
        dfa.add_transition(q4, "GIT", q6)   # <-- ¡ESTA LÍNEA ES LA CLAVE!
        dfa.add_transition(q5, "GIT", q6)

        dfa.add_initial_state(q0)
        dfa.add_final_state(q6)
        return dfa

    def _build_backend_automaton(self):
        dfa = DFA()
        q0, q1, q2, q3, q4, q5, q6 = [dfa.add_state() for _ in range(7)]
        dfa.add_transition(q0, "PYTHON", q1)
        dfa.add_transition(q0, "JAVA", q1)
        dfa.add_transition(q1, "NODE_JS", q2)
        dfa.add_transition(q1, "DJANGO", q2)
        dfa.add_transition(q1, "SPRING_BOOT", q2)
        dfa.add_transition(q2, "POSTGRESQL", q3)
        dfa.add_transition(q2, "MONGODB", q3)
        dfa.add_transition(q3, "REST_API", q4)
        dfa.add_transition(q4, "DOCKER", q5)
        dfa.add_transition(q5, "GIT", q6)
        dfa.add_initial_state(q0)
        dfa.add_final_state(q6)
        return dfa

    def _build_data_scientist_automaton(self):
        dfa = DFA()
        q0, q1, q2, q3, q4, q5, q6 = [dfa.add_state() for _ in range(7)]
        dfa.add_transition(q0, "PYTHON", q1)
        dfa.add_transition(q0, "R", q1)
        dfa.add_transition(q1, "PANDAS", q2)
        dfa.add_transition(q1, "NUMPY", q2)
        dfa.add_transition(q2, "SCIKIT_LEARN", q3)
        dfa.add_transition(q2, "TENSORFLOW", q3)
        dfa.add_transition(q3, "SQL", q4)
        dfa.add_transition(q4, "TABLEAU", q5)
        dfa.add_transition(q4, "POWER_BI", q5)
        dfa.add_transition(q5, "GIT", q6)
        dfa.add_initial_state(q0)
        dfa.add_final_state(q6)
        return dfa

    def classify(self, normalized_skills: list) -> dict:
        results = {}
        for profile, automaton in self.automata.items():
            accepted = automaton.accepts(normalized_skills)
            results[profile] = "ACCEPTED" if accepted else "REJECTED"
        return results