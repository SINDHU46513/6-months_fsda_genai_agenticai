import openai

openai.api_key = "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"

def retriever_info(query):
    # Dummy implementation for example purposes
    return "about prime minister of india"

def rag_query(query):
    retrieved_info = retriever_info(query)  # Call to the retriever_info function
    augmented_prompt = f"User query: {query}. Retrieved information: {retrieved_info}"
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",  # Use the correct model
        messages=[
            {"role": "user", "content": augmented_prompt}
        ],
        max_tokens=150,
        temperature=0.7,
    )
    
    return response.choices[0].message['content'].strip()

# Example usage
query = "Tell me about the prime minister of india"
response = rag_query(query)
print(response)

