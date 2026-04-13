from langchain_google_vertexai import ChatVertexAI

# Test with Gemini 2.5
try:
    llm = ChatVertexAI(model="gemini-2.5-flash")
    response = llm.invoke("Hello, are you active?")
    print("Success! Model responded:", response.content)
except Exception as e:
    print(f"Error: {e}")
