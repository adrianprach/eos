import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import call_function
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

if api_key is None:
    raise RuntimeError("GEMINI_API_KEY is not set.")

parser = argparse.ArgumentParser(description="EOS prompt")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)


def main():
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    iteration_ceil = 20

    for i in range(iteration_ceil):
        attempt = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt, tools=[available_functions]
            ),
        )
        if attempt.candidates is not None:
            messages.extend(attempt.candidates)
        if attempt.usage_metadata is None:
            raise RuntimeError("Fail to fetch usage metadata.")
        # attempt.usage_metadata.thoughts_token_count
        prompt_token, response_token = (
            attempt.usage_metadata.prompt_token_count,
            attempt.usage_metadata.candidates_token_count,
        )
        functions_results = []
        if attempt.function_calls is not None:
            for fc in attempt.function_calls:
                function_call_result = call_function(fc, args.verbose)
                if function_call_result.parts is None:
                    raise RuntimeError("Parts is None.")
                if function_call_result.parts[0].function_response is None:
                    raise RuntimeError("First function response from first part is None.")
                if function_call_result.parts[0].function_response.response is None:
                    raise RuntimeError("First response from first function is None.")
                functions_results.append(function_call_result.parts[0])
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
        else:
            print("Function called not required.")
            break
        messages.append(types.Content(role="user", parts=functions_results))
        if i >= iteration_ceil - 1:
            print(f"Max iteration reached: {iteration_ceil}, not able to complete the response.")
            return 1

    # attempt.usage_metadata.prompt_token_count
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_token}\nResponse tokens: {response_token}")
        print(f"Response:\n{attempt.text}")
    else:
        print(f"Final response: \n{attempt.text}")


if __name__ == "__main__":
    main()
