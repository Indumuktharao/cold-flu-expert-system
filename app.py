from flask import Flask, render_template, request

app = Flask(__name__)

SYMPTOMS = [
    ("fever", "Fever"),
    ("high_fever", "High fever"),
    ("sneezing", "Sneezing"),
    ("runny_nose", "Runny nose"),
    ("cough", "Cough"),
    ("body_pain", "Body pain"),
    ("severe_fatigue", "Severe fatigue"),
    ("headache", "Headache"),
    ("sore_throat", "Sore throat"),
    ("chills", "Chills"),
]

RULES = [
    {"id": "R1", "conditions": ["runny_nose", "sneezing"],
     "conclusion": "cold_pattern",
     "reason": "Runny nose and sneezing together support a cold-like pattern."},
    {"id": "R2", "conditions": ["sore_throat", "sneezing"],
     "conclusion": "cold_pattern",
     "reason": "Sore throat and sneezing together support a cold-like pattern."},
    {"id": "R3", "conditions": ["high_fever", "body_pain"],
     "conclusion": "flu_pattern",
     "reason": "High fever and body pain together support a flu-like pattern."},
    {"id": "R4", "conditions": ["chills", "severe_fatigue"],
     "conclusion": "flu_pattern",
     "reason": "Chills and severe fatigue together support a flu-like pattern."},
    {"id": "R5", "conditions": ["flu_pattern", "cough"],
     "conclusion": "flu_more_likely",
     "reason": "A flu-like pattern plus cough adds support to the flu-like classification."},
    {"id": "R6", "conditions": ["cold_pattern"],
     "conclusion": "cold_more_likely",
     "reason": "A cold-like pattern supports the cold-like classification."},
]

def forward_chain(input_facts):
    facts = set(input_facts)
    trace = []
    fired = set()
    changed = True

    while changed:
        changed = False
        for rule in RULES:
            if rule["id"] in fired:
                continue
            if all(condition in facts for condition in rule["conditions"]):
                facts.add(rule["conclusion"])
                fired.add(rule["id"])
                trace.append(rule)
                changed = True

    cold = "cold_more_likely" in facts
    flu = "flu_more_likely" in facts

    if cold and flu:
        result = "Mixed indicators"
        detail = "The sample rules identified both cold-like and flu-like patterns."
        category = "mixed"
    elif flu:
        result = "Flu-like pattern"
        detail = "The selected symptoms match the flu-like pattern in this educational rule base."
        category = "flu"
    elif cold:
        result = "Common-cold-like pattern"
        detail = "The selected symptoms match the cold-like pattern in this educational rule base."
        category = "cold"
    else:
        result = "Insufficient matching evidence"
        detail = "The selected symptoms did not activate a classification rule."
        category = "unknown"

    return {
        "input_facts": sorted(input_facts),
        "facts": sorted(facts),
        "trace": trace,
        "result": result,
        "detail": detail,
        "category": category,
    }

@app.route("/", methods=["GET", "POST"])
def home():
    selected = []
    report = None
    if request.method == "POST":
        allowed = {key for key, _ in SYMPTOMS}
        selected = [key for key in request.form.getlist("symptoms") if key in allowed]
        if selected:
            report = forward_chain(selected)
    return render_template("index.html", symptoms=SYMPTOMS,
                           selected=selected, report=report)

if __name__ == "__main__":
    app.run(debug=True)
