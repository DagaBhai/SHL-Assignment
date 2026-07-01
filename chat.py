import requests

URL = "http://127.0.0.1:8000/chat"

messages = []

print("SHL Hiring Assistant")
print("Type 'quit' to exit.\n")

while True:
    user = input("You: ")

    if user.lower() == "quit":
        break

    messages.append(
        {
            "role": "user",
            "content": user,
        }
    )

    response = requests.post(
        URL,
        json={"messages": messages},
    )

    response.raise_for_status()

    data = response.json()

    print("\nAssistant:", data)

    # Save assistant reply for the next request
    # (content must be a string — the server's Message model rejects a dict)
    messages.append(
        {
            "role": "assistant",
            "content": data.get("reply", ""),
        }
    )

    if not data["recommendations"] :
        print("\ncomparison\n")
        print(data)
    if data["recommendations"]:
        print("\nRecommendations:\n")
        for rec in data["recommendations"]:
            print(f"- {rec['name']}")
            print(f"  {rec['url']}")
            print(f"  {rec['description']}\n")

    if data["end_of_conversation"]:
        break