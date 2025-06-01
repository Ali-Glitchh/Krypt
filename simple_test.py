import torch
print("PyTorch available:", torch.__version__)

from crypto_chatbot import chatbot
print("Chatbot imported successfully")

# Test basic functionality
response = chatbot.generate_response("hi", None)
print("Response to 'hi':", response)
