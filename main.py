import os
from dotenv import load_dotenv 
from google import genai
from google.genai import types
import argparse

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

if api_key is None:
    raise RuntimeError("GEMINI_API_KEY is not set.")

parser = argparse.ArgumentParser(description="EOS prompt")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

def main():
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    attempt = client.models.generate_content(model="gemini-2.5-flash", contents=messages)
    if attempt.usage_metadata is None:
        raise RuntimeError("Fail to fetch usage metadata.")
    # attempt.usage_metadata.thoughts_token_count
    prompt_token, response_token = attempt.usage_metadata.prompt_token_count, attempt.usage_metadata.candidates_token_count
    # attempt.usage_metadata.prompt_token_count
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_token}\nResponse tokens: {response_token}")
        print(f"Response:\n{attempt.text}")
    else:
        print(attempt.text)


if __name__ == "__main__":
    main()
