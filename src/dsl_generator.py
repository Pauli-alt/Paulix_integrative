from textx import metamodel_from_str

GRAMMAR = """
Model: candidates+=Candidate;
Candidate: 'Candidate' name=STRING '{'
    contact=Contact
    summary=Summary
    experience*=Experience
    skills=Skills
    evaluation=Evaluation
'}';

Contact: 'Contact' '{'
    'email' email=STRING
    'location' location=STRING
    'role' role=STRING
'}';

Summary: 'Summary' '{'
    'text' text=STRING
'}';

Experience: 'Experience' '{'
    'title' title=STRING
    'company' company=STRING
    'years' years=INT
    'description' description=STRING
'}';

Skills: 'Skills' '{'
    skills+=STRING[',']
'}';

Evaluation: 'Evaluation' '{'
    'profile' profile=STRING
    'result' result=STRING
    'explanation' explanation=STRING
'}';
"""

class DSLGenerator:
    def __init__(self):
        self.metamodel = metamodel_from_str(GRAMMAR)

    def generate_model_string(self, candidate_data: dict, evaluation: dict) -> str:
        skills_str = ", ".join(candidate_data.get("normalized_skills", []))
        experience_str = ""
        for exp in candidate_data.get("experiences", []):
            experience_str += f"""
    Experience {{
        title "{exp.get('title', 'N/A')}"
        company "{exp.get('company', 'N/A')}"
        years {exp.get('years', 0)}
        description "{exp.get('description', 'N/A')}"
    }}"""
        model_str = f"""
Candidate "{candidate_data.get('name', 'Unknown')}" {{
    Contact {{
        email "{candidate_data.get('email', 'N/A')}"
        location "{candidate_data.get('location', 'N/A')}"
        role "{candidate_data.get('role', 'N/A')}"
    }}
    Summary {{
        text "{candidate_data.get('summary', 'N/A')}"
    }}{experience_str}
    Skills {{
        {skills_str}
    }}
    Evaluation {{
        profile "{evaluation.get('profile', 'N/A')}"
        result "{evaluation.get('result', 'REJECTED')}"
        explanation "{evaluation.get('explanation', 'N/A')}"
    }}
}}
"""
        return model_str

    def validate_model(self, model_str: str):
        try:
            return self.metamodel.model_from_str(model_str)
        except Exception as e:
            raise ValueError(f"Error de validación DSL: {e}")

    def generate_html(self, model) -> str:
        candidate = model.candidates[0]
        name = candidate.name
        contact = candidate.contact
        summary = candidate.summary.text
        experiences = candidate.experience
        skills = candidate.skills.skills
        evaluation = candidate.evaluation

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ResumeLens - {name}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root {{
            --pastel-pink: #FFD1DC;
            --pastel-lavender: #E6E6FA;
            --pastel-blue: #B0E0E6;
            --pastel-mint: #B2FBA5;
            --pastel-yellow: #FFFACD;
            --pastel-peach: #FFDAB9;
            --text-dark: #4A4A4A;
            --text-light: #7A7A7A;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, var(--pastel-lavender), var(--pastel-blue));
            margin: 0;
            padding: 40px;
            color: var(--text-dark);
        }}
        .candidate-card {{
            max-width: 900px;
            margin: auto;
            background-color: white;
            border: 2px solid var(--pastel-pink);
            border-radius: 20px;
            padding: 35px;
            box-shadow: 0 10px 30px rgba(255, 209, 220, 0.5);
            position: relative;
            overflow: hidden;
        }}
        .candidate-card::before {{
            content: "🌸";
            position: absolute;
            top: -20px;
            right: -20px;
            font-size: 120px;
            opacity: 0.1;
            transform: rotate(15deg);
        }}
        .header {{
            border-bottom: 3px solid var(--pastel-pink);
            margin-bottom: 25px;
            padding-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.2em;
        }}
        .header h1 i {{
            color: var(--pastel-pink);
            margin-right: 10px;
        }}
        .header p {{
            margin: 5px 0 0 0;
            color: var(--text-light);
            font-style: italic;
        }}
        .section {{
            margin-bottom: 30px;
        }}
        .section h2 {{
            border-bottom: 2px dashed var(--pastel-blue);
            padding-bottom: 8px;
            font-size: 1.4em;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .section h2 i {{
            color: var(--pastel-pink);
        }}
        .info-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }}
        .info-item {{
            background-color: var(--pastel-lavender);
            padding: 12px 15px;
            border-radius: 12px;
            border-left: 5px solid var(--pastel-pink);
        }}
        .skills {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
        }}
        .skill {{
            background: linear-gradient(135deg, var(--pastel-pink), var(--pastel-peach));
            border-radius: 25px;
            padding: 10px 20px;
            font-weight: 600;
            box-shadow: 0 4px 6px rgba(255, 209, 220, 0.4);
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .skill i {{
            color: white;
        }}
        .evaluation {{
            background: linear-gradient(135deg, var(--pastel-mint), var(--pastel-yellow));
            padding: 25px;
            border-radius: 15px;
            border: 2px solid var(--pastel-pink);
            text-align: center;
        }}
        .accepted {{
            font-weight: bold;
            color: #2E8B57;
            font-size: 1.3em;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }}
        .rejected {{
            font-weight: bold;
            color: #CD5C5C;
            font-size: 1.3em;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }}
        .experience-item {{
            background-color: var(--pastel-blue);
            padding: 15px;
            border-radius: 12px;
            margin-bottom: 15px;
            border-left: 5px solid var(--pastel-pink);
        }}
        .experience-item h3 {{
            margin: 0 0 5px 0;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            color: var(--text-light);
            font-size: 0.9em;
        }}
        .footer i {{
            color: var(--pastel-pink);
        }}
    </style>
</head>
<body>
<div class="candidate-card">
    <div class="header">
        <h1><i class="fas fa-female"></i> {name}</h1>
        <p><i class="fas fa-magic"></i> Candidate Profile generated by ResumeLens</p>
    </div>

    <div class="section">
        <h2><i class="fas fa-id-card"></i> Personal Information</h2>
        <div class="info-grid">
            <div class="info-item"><strong><i class="fas fa-envelope"></i> Email:</strong> {contact.email}</div>
            <div class="info-item"><strong><i class="fas fa-map-marker-alt"></i> Location:</strong> {contact.location}</div>
            <div class="info-item"><strong><i class="fas fa-briefcase"></i> Current Role:</strong> {contact.role}</div>
        </div>
    </div>

    <div class="section">
        <h2><i class="fas fa-star"></i> Profile Summary</h2>
        <p>{summary}</p>
    </div>

    <div class="section">
        <h2><i class="fas fa-history"></i> Experience</h2>
        {"".join([f'''
        <div class="experience-item">
            <h3>{exp.title}</h3>
            <p><i class="fas fa-building"></i> {exp.company} · {exp.years} years</p>
            <p>{exp.description}</p>
        </div>
        ''' for exp in experiences])}
    </div>

    <div class="section">
        <h2><i class="fas fa-code"></i> Normalized Technical Skills</h2>
        <div class="skills">
            {"".join([f'<span class="skill"><i class="fas fa-check-circle"></i> {skill}</span>' for skill in skills])}
        </div>
    </div>

    <div class="section">
        <h2><i class="fas fa-clipboard-check"></i> Qualification Evaluation</h2>
        <div class="evaluation">
            <h3><i class="fas fa-user-tie"></i> Profile Evaluated: {evaluation.profile}</h3>
            <p>
                <strong>Qualification Pattern:</strong>
                <span class="{'accepted' if evaluation.result == 'ACCEPTED' else 'rejected'}">
                    <i class="fas {'fa-check-circle' if evaluation.result == 'ACCEPTED' else 'fa-times-circle'}"></i>
                    {evaluation.result}
                </span>
            </p>
            <p>{evaluation.explanation}</p>
        </div>
    </div>

    <div class="footer">
        <p><i class="fas fa-heart"></i> Generated with love by ResumeLens <i class="fas fa-heart"></i></p>
    </div>
</div>
</body>
</html>"""
        return html

    def save_html(self, html_content: str, filename: str = "output.html"):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"HTML generado: {filename}")