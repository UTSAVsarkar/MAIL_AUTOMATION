from transformers import pipeline

classifier = pipeline(
    "text2text-generation",
    model="google/flan-t5-base"
)

def is_customer_inquiry(email_text: str) -> bool:
    prompt = f"""
Task:
Classify the email into exactly ONE label.

Labels:
Customer Inquiry
Marketing / Promotion
Newsletter
System Notification

Rules:
- Output ONLY the label.
- Do NOT explain.
- Do NOT repeat the email.

Examples:
Email: Where is my order?
Label: Customer Inquiry

Email: Renew now and get 30% off
Label: Marketing / Promotion

Email: Your OTP for login is 123456
Label: System Notification

Email:
{email_text}

Label:
""".strip()

    output = classifier(prompt, max_length=8, do_sample=False)[0]["generated_text"]
    output = output.lower().strip()

    return output == "customer inquiry"