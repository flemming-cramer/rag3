import sys
sys.path.insert(0, '/tmp/click_pkg')
import click
from chatcore import answer

@click.command()
def chat():
    print("🧠 COBOL Local RAG Chatbot (Ollama)")
    print("Type 'exit' to quit")

    while True:
        q = input("\nYou: ")
        if q.lower() in ["exit", "quit"]:
            break

        print("\nBot:", answer(q))

if __name__ == "__main__":
    chat()