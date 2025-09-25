import os
import json
import openai

# --- Configuration ---
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set.")
openai.api_key = OPENAI_API_KEY

# --- API Connectors ---
def get_openai_completion(prompt, model="gpt-4.1-mini"):
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": "You are a helpful research assistant."}, 
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        return None

# --- Research Functions ---
def verify_claim_with_openai(claim):
    prompt = f"Please verify the following claim and provide a confidence score (0-100) and a brief explanation. Claim: '{claim}'"
    response = get_openai_completion(prompt)
    # In a real scenario, you would parse the response to extract the score and explanation
    return {"zts": 85, "explanation": response}

# --- Main Execution Logic ---
if __name__ == "__main__":
    # Example of verifying a claim
    claim_to_verify = "Alex Kumar has 7 years of experience with AWS and Kubernetes."
    verification_result = verify_claim_with_openai(claim_to_verify)
    print(json.dumps(verification_result, indent=2))

