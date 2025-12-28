import json

# Load JSON
with open("llama_output.json", encoding="utf-8") as f:
    data = json.load(f)

# ---------------- EXTRACT VARIABLES ----------------
fb = data["FUNCTION_BLOCK"]["Tank_Level_Control"]
inputs = fb["Inputs"]
outputs = fb["Outputs"]

program = data["PROGRAM"]["MAIN_PROGRAM"]
internal_vars = program["VAR"]
run_logic = program["RUN"]
output_map = program["OUTPUTS"]

# ---------------- DECLARATION ----------------
declaration = "VAR\n"

for var in inputs:
    declaration += f"    {var['Name']} : {var['Type']};\n"

for var in outputs:
    declaration += f"    {var['Name']} : {var['Type']};\n"

for var in internal_vars:
    declaration += f"    {var['Name']} : {var['Type']};\n"

declaration += "END_VAR\n"

# ---------------- IMPLEMENTATION ----------------
implementation = ""

for block in run_logic:
    case = block["CASE"]
    expr = case["expr"]

    implementation += f"IF {expr} THEN\n"

    for action in case["THEN"]:
        if "VAR" in action:
            implementation += f"    {action['VAR']} := {action['ASSIGN']};\n"
        elif "IF" in action:
            cond = action["IF"]["expr"]
            assign = action["IF"]["THEN"]
            implementation += f"    IF {cond} THEN\n"
            implementation += f"        {assign['VAR']} := {str(assign['ASSIGN']).upper()};\n"
            implementation += f"    END_IF;\n"

    implementation += "END_IF;\n\n"

# ---------------- MAP OUTPUT ----------------
for out in output_map:
    implementation += f"{out['Name']} := {out['Value']};\n"

# ---------------- FINAL ST ----------------
st_code = (
    "(* AUTO-GENERATED PLC LOGIC *)\n\n"
    "DECLARATION\n"
    + declaration
    + "\nIMPLEMENTATION\n"
    + implementation
)

with open("plc_logic.st", "w", encoding="utf-8") as f:
    f.write(st_code)

print("plc_logic.st generated successfully")
