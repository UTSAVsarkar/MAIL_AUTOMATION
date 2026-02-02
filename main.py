from text_cleaner import clean_email_text
from intent_classifier import is_customer_inquiry
from gmail_auth import authenticate_gmail
from gmail_reader import fetch_unread_email
from ai_responder import generate_reply
from gmail_sender import send_reply, mark_as_read


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

    # Generate AI reply
    reply = generate_reply(clean_body)
    reply += "\n\n---\nThis is an automated response."

    print("\n📨 AUTO-GENERATED REPLY")
    print("=" * 60)
    print(reply)
    print("=" * 60)

    # AUTO-SEND (no permission)
    send_reply(service, email['sender'], email['subject'], reply)
    mark_as_read(service, email['id'])

    print("✅ Reply sent automatically and email marked as read.")


if __name__ == "__main__":
    main()
