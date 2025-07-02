from flask import Flask, render_template, request, jsonify
import dotenv
import os
from models import CONVERSATION_MODELS, TOOLCALLING_MODELS

app = Flask(__name__)
dotenv.load_dotenv(override=True)

@app.route('/')
def index():
    api_key = os.getenv("OPENAI_API_KEY")
    key_exists = bool(api_key)
    
    return render_template('index.html', key_exists=key_exists, 
                           conversation_models=CONVERSATION_MODELS, 
                           toolcalling_models=TOOLCALLING_MODELS)

@app.route('/save_key', methods=['POST'])
def save_key():
    data = request.get_json()
    api_key = data.get('apiKey')
    conversation_model = data.get('conversationModel')
    toolcalling_model = data.get('toolcallingModel')

    if not api_key:
        return jsonify({'error': 'API Key é obrigatória'}), 400

    os.environ['OPENAI_API_KEY'] = api_key
    os.environ['MODEL_ID_CONVERSATION'] = conversation_model
    os.environ['MODEL_ID_TOOLCALLING'] = toolcalling_model

    return jsonify({'message': 'Chave e modelos salvos com sucesso!'})

if __name__ == '__main__':
    app.run(debug=True)