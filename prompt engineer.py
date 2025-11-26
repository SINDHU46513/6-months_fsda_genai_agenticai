import streamlit as st
import openai

# Set your OpenAI API key
openai.api_key = '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'  # Replace with your actual API key

def generate_response(prompt, model="gpt-4o", max_length=100,temperature=0.2,topp=0.7):
    try:
        # Create a chat completion request
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_length,
            temperature=temperature
        )
        # Extract and return the response content
        return response['choices'][0]['message']['content']
    
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Streamlit app layout
st.title("Prompt Engineering with OpenAI")
st.write("Enter your prompt below and see how the model responds.")

# User input for the prompt
user_prompt = st.text_area("Prompt", height=200)

# Generate response button
if st.button("Generate Response"):
    if user_prompt:
        with st.spinner("Generating response..."):
            response = generate_response(user_prompt)
            if response:
                st.subheader("Assistant's Response:")
                st.write(response)
    else:
        st.warning("Please enter a prompt before generating a response.")

# Optional: add footer or additional information
st.write("This app uses OpenAI's API to generate responses based on your prompts.")


