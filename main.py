from text_cleaner import clean_email_text
from intent_classifier import is_customer_inquiry
from gmail_auth import authenticate_gmail
from gmail_reader import fetch_unread_email
from ai_responder import generate_reply
from gmail_sender import send_reply, mark_as_read


def wrap_in_professional_template(body_text):
    return f"""Hi,

{body_text.strip()}

If you have any additional details or questions, please feel free to reply to this email.

Best regards,  
Customer Support Team
"""


def main():
    service = authenticate_gmail()
    email = fetch_unread_email(service)

    if not email:
        print("❌ No unread emails found.")
        return

    print("\n📩 INCOMING EMAIL")
    print("=" * 60)
    print("FROM   :", email['sender'])
    print("SUBJECT:", email['subject'])

    # Clean email body
    clean_body = clean_email_text(email['body'])

    print("\n🧹 CLEANED EMAIL (LLM INPUT):\n", clean_body)

    # Check if this is a customer inquiry
    if not is_customer_inquiry(clean_body):
        print("\n🚫 Not a customer inquiry. Skipping.")
        mark_as_read(service, email['id'])
        return

    # Generate AI reply (LLM output only)
    ai_reply = generate_reply(clean_body)

    # Wrap in professional mail template
    final_reply = wrap_in_professional_template(ai_reply)

    print("\n📨 AUTO-GENERATED REPLY (FINAL)")
    print("=" * 60)
    print(final_reply)
    print("=" * 60)

    # Send reply and mark as read
    send_reply(
        service,
        email['sender'],
        email['subject'],
        final_reply
    )
    mark_as_read(service, email['id'])

    print("✅ Reply sent automatically and email marked as read.")


if __name__ == "__main__":
    main()