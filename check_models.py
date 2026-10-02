import google.generativeai as genai

# Replace with your actual API key
genai.configure(api_key="YOUR_GEMINI_API_KEY")

print("Models available for your API Key:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)