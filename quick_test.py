from crypto_chatbot import CryptoChatbot

# Quick test
bot = CryptoChatbot()
print("Bot initialized!")
print(f"Sub-Zero responses: {len(bot.chat_dataset.get('sub_zero_responses', []))}")
print(f"Sub-Zero jokes: {len(bot.chat_dataset.get('sub_zero_jokes', []))}")

# Test a greeting
response = bot.generate_response("hi")
print(f"Greeting response: {response}")

# Test a joke request
joke_response = bot.generate_response("tell me a joke")
print(f"Joke response: {joke_response}")
