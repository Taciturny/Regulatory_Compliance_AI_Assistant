from flask import Flask, render_template, request, jsonify, session
from gradio_client import Client
from flask_session import Session


app = Flask(__name__)
app.secret_key = '6yygoypu87tyvtir8-8'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():

    if 'history' not in session:
        session['history'] = []

    history = session['history']

    user_message = request.form['message']

    history_context = """
    Conversation History:
    This is a conversation history between the user and the assistant. The user asks questions, and the assistant provides answers based on the context of the conversation. The assistant's responses are informed by previous interactions and relevant information retrieved from documents.
    The history is to provide you with knowledge of the user and the context of the conversation, don't use it to answer the question.
    {history}
    """

    user_message = user_message + history_context.format(history="\n".join([f"{msg['role']}: {msg['content']}" for msg in history]))

    client = Client("https://d125f64a21587bade4.gradio.live")
    result = client.predict(
		message= user_message,
		api_name="/chat"
)
    
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": result})
    session['history'] = history

    return jsonify({'response': result})

if __name__ == '__main__':
    app.run(debug=True)
