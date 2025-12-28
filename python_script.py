# Read customer plain text
with open("C:\\Users\\arunv\\Desktop\\SEH\\customer_input.txt", "r") as f:
    text = f.read().lower()
# Default values
application = "Unknown Process"
inputs = []
outputs = []
modes = []
rules = []

# Simple keyword-based extraction
if "tank" in text:
    application = "Tank level control system"

if "level sensor" in text:
    inputs.append("- Level : INT")

if "pump" in text:
    outputs.append("- Pump : BOOL")

if "manual" in text:
    inputs.append("- Manual_Mode : BOOL")
    inputs.append("- Manual_Pump : BOOL")
    modes.append("- Manual Mode")
    rules.append("- If Manual_Mode = TRUE → Pump follows Manual_Pump")

if "automatic" in text:
    modes.append("- Automatic Mode")
    rules.append("- If Manual_Mode = FALSE:")
    rules.append("  - Pump ON when Level < Low_Threshold")
    rules.append("  - Pump OFF when Level > High_Threshold")
    inputs.append("- Low_Threshold : INT")
    inputs.append("- High_Threshold : INT")

# Build structured prompt
structured_prompt = f"""
SYSTEM ROLE:
You are an industrial PLC logic designer.

APPLICATION:
{application}

SIGNALS:
Inputs:
{chr(10).join(inputs)}

Outputs:
{chr(10).join(outputs)}

OPERATING MODES:
{chr(10).join(modes)}

CONTROL RULES:
{chr(10).join(rules)}

CONSTRAINTS:
- Use only BOOL and INT
- No timers or PID
"""

# Save structured prompt
with open("structured_prompt.txt", "w", encoding="utf-8") as f:
    f.write(structured_prompt)

print("Structured prompt generated successfully.")

