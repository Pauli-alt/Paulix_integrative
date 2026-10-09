# Diseño de Módulos - ResumeLens

## Módulo 1: Extractor (Regex)
| Aspecto | Descripción |
|---------|-------------|
| Archivo | src/extractor.py |
| Clase | Extractor |
| Input | text: str |
| Output | dict con email, phone, years_experience, raw_skills |
| Formalismo | Expresiones Regulares |

## Módulo 2: Normalizer (FST)
| Aspecto | Descripción |
|---------|-------------|
| Archivo | src/normalizer.py |
| Clase | Normalizer |
| Input | raw_skills: list |
| Output | normalized_skills: list |
| Formalismo | Transductores de Estados Finitos (7-tupla) |

## Módulo 3: ProfileClassifier (DFA)
| Aspecto | Descripción |
|---------|-------------|
| Archivo | src/classifier.py |
| Clase | ProfileClassifier |
| Input | normalized_skills: list |
| Output | dict con {profile_name: ACCEPTED/REJECTED} |
| Formalismo | Autómatas Finitos Deterministas (5-tupla) |

## Módulo 4: DSLGenerator (TextX)
| Aspecto | Descripción |
|---------|-------------|
| Archivo | src/dsl_generator.py |
| Clase | DSLGenerator |
| Input | candidate_data: dict, evaluation: dict |
| Output | html: str |
| Formalismo | Gramáticas Libres de Contexto (EBNF) |

## Módulo 5: ResumeLensApp (Orquestador)
| Aspecto | Descripción |
|---------|-------------|
| Archivo | src/main.py |
| Clase | ResumeLensApp |
| Input | resume_text: str, candidate_name: str |
| Output | dict con html_file, classification, normalized_skills |
| Descripción | Orquesta el pipeline completo |