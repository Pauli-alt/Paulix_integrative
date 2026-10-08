# Diseño de Módulos - ResumeLens

## Módulo 1: Extractor (Regex)

| Aspecto | Descripción |
|---------|-------------|
| Archivo | src/extractor.py |
| Clase | Extractor |
| Input | text: str |
| Output | dict con email, phone, years_experience, raw_skills |
| Formalismo | Expresiones Regulares |

### Patrones Regex
- Email: [a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}
- Phone: \+?\d[\d\s\-()]{7,}\d
- Years: (\d+)\s*(?:years?|años?)\s*(?:of\s*)?(?:experience|experiencia)
- Skills: Lista de alternancias.