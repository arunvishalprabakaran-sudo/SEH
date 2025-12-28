import requests
import re

# ---------------- READ STRUCTURED PROMPT ----------------
with open("structured_prompt.txt", encoding="utf-8") as f:
    base_prompt = f.read()

# ---------------- STRONG SYSTEM PROMPT ----------------
json_rules = """
You are an industrial PLC logic generator.

IMPORTANT OUTPUT RULES (MANDATORY):
- Output ONLY valid JSON
- Do NOT include explanations, comments, or markdown
- Do NOT include text before or after JSON
- JSON must start with { and end with }
- Use lowercase true / false only
- Variable references must be strings (e.g., "Manual_Pump")
- Do NOT use PLC keywords like TRUE/FALSE
- Follow the JSON schema exactly as specified
"""

# ---------------- JSON SCHEMA (VERY IMPORTANT) ----------------
json_schema = """
Required JSON Structure:

{
  "FUNCTION_BLOCK": {
    "Tank_Level_Control": {
      "Inputs": [
        {"Name": "string", "Type": "INT or BOOL"}
      ],
      "Outputs": [
        {"Name": "string", "Type": "BOOL"}
      ]
    }
  },
  "PROGRAM": {
    "MAIN_PROGRAM": {
      "VAR": [
        {"Name": "string", "Type": "BOOL"}
      ],
      "INIT": {
        "auto_mode": false
      },
      "RUN": [
        {
          "CASE": {
            "expr": "string",
            "THEN": [
              { "VAR": "string", "ASSIGN": "string or boolean" }
            ]
          }
        }
      ],
      "OUTPUTS": [
        {"Name": "string", "Value": "string"}
      ]
    }
  }
}
"""

full_prompt = base_prompt + json_rules + json_schema

# ---------------- OLLAMA API CALL ----------------
url = "http://localhost:11434/api/generate"

payload = {
    "model": "llama3.1:latest",
    "prompt": full_prompt,
    "stream": False
}

response = requests.post(url, json=payload)
data = response.json()

# ---------------- EXTRACT MODEL OUTPUT ----------------
if "response" in data:
    result = data["response"]
elif "message" in data and "content" in data["message"]:
    result = data["message"]["content"]
else:
    raise ValueError(f"Unexpected Ollama response format: {data}")

# ---------------- CLEAN OUTPUT (CRITICAL) ----------------
# Remove markdown if any
result = re.sub(r"```json|```", "", result).strip()

# Extract only JSON block
match = re.search(r"\{.*\}", result, re.DOTALL)
if not match:
    raise ValueError("No valid JSON object found in LLaMA output")

clean_json = match.group()

# ---------------- SAVE FINAL JSON ----------------
with open("llama_output.json", "w", encoding="utf-8") as f:
    f.write(clean_json)

print("✅ Clean JSON generated successfully: llama_output.json")
