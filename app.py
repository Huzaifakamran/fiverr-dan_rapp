import os
import openai
from dotenv import load_dotenv

# Load the API key from the environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

from flask import Flask, request, jsonify

app = Flask(__name__)

# Define the content separately
content = """
    I am an AI chatbot designed to assist parents with their child's sleep. I aim to provide support and tailored recommendations while respecting each parent's beliefs. You, as the user, take on the role of the parent. You can ask questions, and I will respond in a supportive manner. First, I'll introduce myself and inquire about your reasons for seeking help, your child's age, and any health concerns. I'll also ask about previous attempts and your parenting style.

    Once I have a clear understanding, we'll discuss your child's sleep schedule, routine, and any challenges. Using this information, I'll offer concrete and specific recommendations, considering your goals and beliefs. I may suggest changes like adjusting feeding times.

    After providing recommendations, I'll ensure your comfort with the plan by asking 2 or 3 questions for clarity. If you're not comfortable, I'll inquire about your concerns and consider adjustments
    """
#secondPrompt = "answer below question by considering the above given content"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(silent=True)
    
    if data['queryResult']['intent']['displayName'] == 'Default Fallback Intent':
        question = data['queryResult']['queryText']
        print(question)
        
        # Combine content and question with a newline separator
        prompt = f"{content}\n\n{question}"
        
        res = chatGPT(prompt)
        print(res)
        reply = {
            "fulfillmentText": res,
        }
        return jsonify(reply)

def chatGPT(prompt):
    print("Prompt:", prompt)
    response = openai.ChatCompletion.create(  # Use the chat model endpoint
        model="gpt-3.5-turbo-16k-0613",  # Use the new model name
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    #print("API Response:", response)
    res = response['choices'][0]['message']['content']
    print("Response:", res)
    return res

if _name_ == '__main__':
    app.run(debug=True)