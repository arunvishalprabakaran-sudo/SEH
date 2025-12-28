import json
import re

# -------------------------------------------------
# OPERATOR FIX FUNCTION (IEC 61131-3 SAFE)
# -------------------------------------------------
def fix_st_operators(expr: str) -> str:
    if not isinstance(expr, str):
        return expr

    expr = expr.replace("&&", " AND ")
    expr = expr.replace("||", " OR ")
    expr = re.sub(r'!\s*(?!=)', 'NOT ', expr)  # avoid breaking !=
    expr = re.sub(r'\btrue\b', 'TRUE', expr, flags=re.IGNORECASE)
    expr = re.sub(r'\bfalse\b', 'FALSE', expr, flags=re.IGNORECASE)

    return expr


# -------------------------------------------------
# LOAD JSON FROM LLaMA
# -------------------------------------------------
with open("llama_output.json", encoding="utf-8") as f:
    data = json.load(f)


# -------------------------------------------------
# EXTRACT STRUCTURE
# -------------------------------------------------
fb = data["FUNCTION_BLOCK"]["Tank_Level_Control"]
inputs = fb["Inputs"]
outputs = fb["Outputs"]

program = data["PROGRAM"]["MAIN_PROGRAM"]
internal_vars = program["VAR"]
run_logic = program["RUN"]
output_map = program["OUTPUTS"]


# -------------------------------------------------
# DECLARATION SECTION
# -------------------------------------------------
declaration = "VAR\n"

for var in inputs:
    declaration += f"    {var['Name']} : {var['Type']};\n"

for var in outputs:
    declaration += f"    {var['Name']} : {var['Type']};\n"

for var in internal_vars:
    declaration += f"    {var['Name']} : {var['Type']};\n"

declaration += "END_VAR\n"


# -------------------------------------------------
# IMPLEMENTATION SECTION
# -------------------------------------------------
implementation = ""

for block in run_logic:
    case = block["CASE"]

    # FIX MAIN IF CONDITION
    expr = fix_st_operators(case["expr"])
    implementation += f"IF {expr} THEN\n"

    for action in case["THEN"]:

        # SIMPLE ASSIGNMENT
        if "VAR" in action:
            value = fix_st_operators(str(action["ASSIGN"]))
            implementation += f"    {action['VAR']} := {value};\n"

        # NESTED IF
        elif "IF" in action:
            cond = fix_st_operators(action["IF"]["expr"])
            assign = action["IF"]["THEN"]
            value = fix_st_operators(str(assign["ASSIGN"]))

            implementation += f"    IF {cond} THEN\n"
            implementation += f"        {assign['VAR']} := {value};\n"
            implementation += f"    END_IF;\n"

    implementation += "END_IF;\n\n"


# -------------------------------------------------
# OUTPUT MAPPING
# -------------------------------------------------
for out in output_map:
    value = fix_st_operators(str(out["Value"]))
    implementation += f"{out['Name']} := {value};\n"


# -------------------------------------------------
# FINAL ST CODE
# -------------------------------------------------
st_code = (
    "(* AUTO-GENERATED PLC LOGIC *)\n\n"
    "PROGRAM MAIN_PROGRAM\n"
    + declaration
    + "\n"
    + implementation
)

# -------------------------------------------------
# WRITE TO FILE
# -------------------------------------------------
with open("plc_logic.st", "w", encoding="utf-8") as f:
    f.write(st_code)

print("✅ plc_logic.st generated successfully (CODESYS compatible)")
