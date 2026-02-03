from transformers import pipeline

generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base"
)

def generate_reply(email_text: str) -> str:
    prompt = f"""
You are a customer support assistant.

Task:
You are given a small set of example customer emails and their correct responses.
Learn from these examples and generate an appropriate response for a new customer email.

Guidelines:
- Write ONLY the reply email.
- Do NOT repeat the customer message.
- Do NOT explain your reasoning.
- Be polite, professional, and helpful.
- Ask for relevant information only when needed.

Examples:

Customer Email:
Where is my order?

Response:
Thank you for reaching out. We’re sorry for the delay. Please share your order ID so we can check the status for you.


Customer Email:
I want a refund for my recent purchase.

Response:
We’re sorry to hear that. Please provide your order ID so we can assist you with the refund process.


Customer Email:
I cannot log in to my account.

Response:
We’re sorry you’re experiencing issues accessing your account. Please confirm your registered email address so we can assist you further.


Now generate a response for the following email by applying the same pattern.

Customer Email:
{email_text}

Response:
""".strip()

    result = generator(
    prompt,
    max_new_tokens=60,
    temperature=0.2,
    top_p=0.9,
    repetition_penalty=1.2,
    do_sample=True
    )

    reply = result[0]["generated_text"].strip()

    # Safety fallback
    if len(reply) < 10 or "customer email" in reply.lower():
        return (
            "Thank you for contacting us. "
            "Please share more details so we can assist you further."
        )

    return reply