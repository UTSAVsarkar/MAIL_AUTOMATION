from transformers import pipeline

generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base"
)

def generate_reply(email_text: str) -> str:
    prompt = f"""
You are a customer support agent.
Your job is to write the email reply.

Instructions:
- Write ONLY the reply email.
- Do NOT mention rules, intent, or analysis.
- Do NOT repeat the customer message.
- Be polite, professional, and helpful.

Examples:

Customer Email:
Where is my order?

Reply:
Thank you for reaching out. Your order is currently being processed and we will update you once it is shipped.

---

Customer Email:
I want a refund for my recent purchase.

Reply:
We’re sorry to hear that. Please share your order ID so we can assist you with the refund process.

---

Customer Email:
{email_text}

Reply:
""".strip()

    result = generator(
        prompt,
        max_length=120,
        do_sample=False
    )

    reply = result[0]["generated_text"].strip()

    # Safety cleanup (very important)
    if "rule" in reply.lower() or "intent" in reply.lower():
        return (
            "Thank you for contacting us. "
            "We are reviewing your request and will get back to you shortly."
        )

    return reply
