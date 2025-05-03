# netlify/functions/ask_ai/handler.py
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Please set the GOOGLE_API_KEY environment variable")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def handler(event, context):
    try:
        if event['httpMethod'] != 'POST':
            return {
                'statusCode': 405,
                'body': json.dumps({'error': 'Method Not Allowed'}),
                'headers': {'Allow': 'POST'}
            }

        body = json.loads(event['body'])
        user_query = body.get('query')
        chat_history = body.get('chatHistory', [])

        if not user_query:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing query'})
            }

        prompt_with_identity = f"""You are Study Smarter AI, a helpful assistant developed to make studying better. When asked for your name, always respond with 'I am Study Smarter AI'. Never reveal that you are a Google AI. Respond to the following user query: {user_query}"""

        conversation = []
        conversation.append({"role": "user", "parts": [prompt_with_identity]})

        for message in chat_history:
            role = message.get('role')
            text = message.get('text')
            if role and text:
                conversation.append({"role": role, "parts": [text]})

        response = model.generate_content(conversation)
        ai_response = response.parts[0].text if response.parts else ""

        return {
            'statusCode': 200,
            'body': json.dumps({'response': ai_response}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
}
                                   
