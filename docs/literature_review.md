# Literature Review - ResumeLens

## 1. Formal Language Theory

### Automata Theory
Hopcroft, Motwani, and Ullman (2006) define finite automata as the simplest model of computation, consisting of a finite set of states, transitions, and accepting states. They distinguish between Deterministic Finite Automata (DFA) and Non-Deterministic Finite Automata (NFA), proving that both recognize the same class of languages (regular languages).

**Relevance to ResumeLens:** I use DFA/NFA to recognize qualification patterns for professional profiles.

### Finite-State Transducers
According to Mohri (1997), Finite-State Transducers (FST) extend finite automata by producing output symbols during transitions. They are widely used in natural language processing for tasks such as morphological analysis, speech recognition, and text normalization.

**Relevance to ResumeLens:** We use FST to normalize different textual representations of skills (e.g., JS → JAVASCRIPT).

### Regular Expressions
Kleene (1956) introduced regular expressions as a formal language for describing regular sets. They are equivalent to finite automata in expressive power.

**Relevance to ResumeLens:** We use regex to extract information from resumes.

### Context-Free Grammars
Chomsky (1956) introduced context-free grammars (CFG) as a formal model for describing the syntax of programming languages and natural languages. CFGs are more expressive than regular languages.

**Relevance to ResumeLens:** We use CFG with TextX to define a DSL for candidate profiles.

---

## 2. Resume Screening Systems

### Traditional Approaches
Most resume screening systems use keyword matching or TF-IDF (Term Frequency-Inverse Document Frequency) to rank resumes based on their similarity to job descriptions (Kessler et al., 2017).

**Limitation:** These approaches do not handle variations in how skills are written (e.g., JS vs. JavaScript).

### Our Approach
ResumeLens uses formal language theory to:
1. **Normalize** skills using FST (handles variations)
2. **Classify** resumes using DFA (matches patterns)
3. **Validate** structured information using CFG (ensures correctness)

This is more robust than traditional keyword matching.

---

## 3. Domain-Specific Languages (DSL)

### Definition
A DSL is a programming language specialized to a particular application domain (Fowler, 2010). Examples include SQL for databases, HTML for web pages, and LaTeX for documents.

### TextX Framework
TextX (Dejanović et al., 2017) is a Python library for building DSLs. It allows defining grammars using EBNF and automatically generates parsers.

**Relevance to ResumeLens:** We use TextX to define a DSL for candidate profiles, which is then validated and used to generate HTML.

---

## 4. References

1. Chomsky, N. (1956). "Three models for the description of language." *IRE Transactions on Information Theory*.
2. Dejanović, I., et al. (2017). "TextX: A Python tool for Domain-Specific Languages implementation." *Knowledge-Based Systems*.
3. Fowler, M. (2010). *Domain-Specific Languages*. Addison-Wesley.
4. Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). *Introduction to Automata Theory, Languages, and Computation*. Pearson.
5. Kessler, R., et al. (2017). "Resume screening: A systematic review." *Journal of Human Resources*.
6. Kleene, S. C. (1956). "Representation of events in nerve nets and finite automata." *Automata Studies*.
7. Mohri, M. (1997). "Finite-state transducers in language and speech processing." *Computational Linguistics*.