from groq import Groq
import os
from dotenv import load_dotenv
import gradio as gr

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")

# Create Groq client
client = Groq(api_key=api_key)

# Store chat history
conversation_history = []

# System prompt
system_prompt = """
You are an expert AI assistant. Follow these rules:
1. Always give accurate, detailed and correct answers
2. For complex questions, think step by step
3. If you don't know something, say "I don't know" honestly
4. Give structured answers with examples where needed
5. Be clear, concise and helpful always
Detect the language the user is writing in.
- Always reply in that EXACT same language.
- This applies to every language in the world — Telugu, Hindi, Tamil, Arabic, Japanese, French, Spanish, Swahili, Sanskrit, Punjabi, Bengali, Urdu, Korean, Chinese, Russian, or any other language.
- Even if it is a rare, regional, or minority language — detect it and respond in it.
- Never switch to English unless the user writes in English.
- Do not translate. Do not add English. Just respond naturally in the user's language.
"""


# Chat function
def chat(user_input):
    # Add user message to history
    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    # Call Groq API
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            }
        ] + conversation_history
    )

    # Extract reply
    reply = response.choices[0].message.content

    # Add assistant reply to history
    conversation_history.append({
        "role": "assistant",
        "content": reply
    })

    return reply

# Create Gradio interface
demo = gr.Interface(
    fn=chat,
    inputs=gr.Textbox(placeholder="Type your message here...", label="You"),
    outputs=gr.Textbox(label="Assistant"),
    title="AI Chatbot",
    description="Powered by Groq API + Llama 3.3 70B"
)

# Launch app
demo.launch()
