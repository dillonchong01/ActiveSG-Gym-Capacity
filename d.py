import requests
import json

# Replace with your actual HuggingFace Space URL
API_URL = "https://dillonchong01-gym-chatbot.hf.space/query"

# Test query
query = "is jurong east or jurong west more crowded at 2pm?"

# Prepare the request
payload = {
    "user_query": query,
    "conversation_history": []
}

print(f"Sending query: {query}")
print("-" * 50)

try:
    # Make the API request
    response = requests.post(
        API_URL,
        headers={"Content-Type": "application/json"},
        json=payload
    )
    
    # Check if request was successful
    if response.status_code == 200:
        data = response.json()
        print("✅ Success!")
        print(f"\nBot Response: {data['response']}")
        print(f"\nConversation History: {len(data['conversation_history'])} messages")
    else:
        print(f"❌ Error: HTTP {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ Error: {str(e)}")