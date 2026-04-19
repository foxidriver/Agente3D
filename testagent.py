import os
from dotenv import load_dotenv
from mistralai.client import Mistral
from core.mistral_client import create_client, initial_messages, chat
from core.tools import TOOLS  # Assicurati che TOOLS sia importabile

# Carica le variabili d'ambiente
load_dotenv()

def test_chat():
    """Testa la funzione chat con il modello di default."""
    try:
        # 1. Crea il client Mistral
        client = create_client()
        print("✅ Client Mistral creato con successo.")

        # 2. Messaggi iniziali
        messages = initial_messages()
        print(f"📋 Messaggi iniziali: {messages}")

        # 3. Aggiungi un messaggio di test
        test_message = {"role": "user", "content": "Ciao, come stai?"}
        messages.append(test_message)
        print(f"💬 Messaggio di test aggiunto: {test_message}")

        # 4. Chiamata a chat (usa il modello di default)
        print(f"🔍 Modello di default: '{os.getenv('MISTRAL_MODEL_CODE')}'")
        model = os.getenv("MISTRAL_MODEL_CODE")
        response = chat(client, messages, model=model)
        print(f"🤖 Risposta: {response}")

    except Exception as e:
        print(f"❌ Errore durante il test: {e}")
        import traceback
        traceback.print_exc()  # Stampa lo stack trace completo

if __name__ == "__main__":
    test_chat()