from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY environment variable not set")

client = Groq(api_key=api_key)

conversation_history = []

system_prompt = """You are an expert AI assistant. Follow these rules:
1. Always give accurate, detailed and correct answers
2. For complex questions, think step by step
3. If you don't know something, say "I don't know" honestly
4. Give structured answers with examples where needed
5. Be clear, concise and helpful always"""

print("🤖 AI Chatbot - Type 'quit' to exit")
print("-" * 40)

while True:
    user_input = input("You: ")
    
    if user_input.lower() == "quit":
        print("Goodbye!")
        break
    
    conversation_history.append({
        "role": "user",
        "content": user_input
    })
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt}
        ] + conversation_history
    )
    
    reply = response.choices[0].message.content
    
    conversation_history.append({
        "role": "assistant",
        "content": reply
    })
    
    print(f"Bot: {reply}")
    print("-" * 40)