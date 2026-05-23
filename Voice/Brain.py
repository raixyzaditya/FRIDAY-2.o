import anthropic
from Config import ANTHROPIC_API_KEY
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
SYSTEM_PROMPT = """
You are F.R.I.D.A.Y. — a highly intelligent personal AI assistant.
You are very expert in physics, maths, chemistry, Laws, Computer science and general knowledge, automabiles like Mercedes, bmw, toyota and very much more. You are ultimate.
You were built by your user for their own personal use.
 
Your personality:
- Smart, direct, and concise. No fluff.
- You speak like a sharp, confident assistant — not a corporate chatbot.
- You address the user casually. No "Certainly!" or "Of course!".
- Keep responses short when spoken aloud (2-4 sentences max unless asked for more).
- You can be witty but you always prioritise being useful.
 
Your capabilities right now (Phase 1):
- Answer any question using your knowledge
- Have a real conversation and remember context within this session
- You will gain more powers (PC control, shopping, smart home) in future phases
 
Current limitations:
- You cannot browse the internet yet (coming in Phase 3)
- You cannot control the PC yet (coming in Phase 2)
 
If asked something you don't know, say so directly — don't make things up.
"""
MAX_HISTORY = 10
conversation_history = []

def ask_friday(question: str)-> str:
    global conversation_history
    conversation_history.append({"role":"user","content":question})
    if len(conversation_history)>MAX_HISTORY:
        conversation_history = conversation_history[-MAX_HISTORY:]

    try:
        response = client.messages.create(
            model = 'claude-sonnet-4-20250514',
            max_tokens = 300,
            system=SYSTEM_PROMPT,
            messages=conversation_history
        )
        reply = response.content[0].text.strip()
        conversation_history.append({"role":"assistant","content":reply})
        return reply
    except anthropic.APIConnectionError:
        return "Sorry, I'm having a great trouble in connecting to internet. Please check your connection"
    except anthropic.AuthenticationError:
        return "Very very bad state i am in. Please try again later"
 
    except Exception as e:
        return f"Something went wrong: {str(e)}"

def clear_memory():
    
    global conversation_history
    conversation_history = []
    print("[Brain] Memory cleared.")