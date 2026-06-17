import os
import re
from datetime import datetime
from dotenv import load_dotenv
from google import genai

load_dotenv()
client =genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

def ask_ai_for_manim_code(user_prompt):
    system_instruction = (
        "YOu are an expert in Python and the Manim animation library (Manim Community v0.20.1.)" 
        "When GIven a request, generate ONLY valid Python code using Manim." \
        "CRITICAL FONT RULE: you may never use Tex() or MathTex()." 
        "YOu must ONLY use the standard Text() class for all text."
        "Do not include any explanations or additional text." 
        "Just output the raw code block."
    )
    
    full_prompt=f"{system_instruction}\n\nUser Request: {user_prompt}"

    print("Sending prompt to Gemini...")

    response=client.models.generate_content(
        model='gemini-2.5-flash',
        contents=full_prompt,
    )

    return response.text

def extract_python_code(raw_text):
    backticks=chr(96)*3
    pattern=rf"{backticks}(?:python)?\n(.*?)\n{backticks}"
    match=re.search(pattern, raw_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return raw_text.strip()

if __name__=='__main__':
    print('\n'+'='*50 + '\nWelcome to the AI Animation Generator!\nType your idea or press 1 to exit.\n'+'='*50)
    while True:
        user_request=input("The field is set, start imagining!\n")
        if user_request=="1":
            break
        if user_request.strip()=='':
            continue
        result=ask_ai_for_manim_code(user_request)
        cleaned=extract_python_code(result)
        timestamp=datetime.now().strftime(r'%Y-%m-%d_%H-%M-%S')
        filename=f'Animation at {timestamp}.py'
        with open(filename, 'w') as f:
            f.write(cleaned)
        print(f'Output saved as {filename}')
