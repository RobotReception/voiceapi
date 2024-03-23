import streamlit as st
import requests

st.title('Send Message')

# URL of the endpoint
url = 'http://172.31.27.15:8003/send-message/'

# User input for the message
message = st.text_input('Enter your message:', '')

if st.button('Send Message'):
    if message:
        # Payload with the user-provided message
        payload = {'message': message}

        # Sending a POST request to the specified URL with the payload
        response = requests.post(url, json=payload)

        # Checking if the request was successful
        if response.status_code == 200:
            # Displaying the JSON response
            st.success('Message sent successfully!')

            # Extracting the response JSON
            response_data = response.json()

            # Displaying each key-value pair in the JSON response
            for key, value in response_data.items():
                # Using columns to align labels and their corresponding values nicely
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown(f"**{key.replace('_', ' ').capitalize()}:**")
                with col2:
                    # Handling None values gracefully
                    if value is None or value == "":
                        st.text('Not provided')
                    else:
                        st.text(value)
        else:
            st.error('Failed to send message. Please try again.')
    else:
        st.error('Please enter a message before sending.')
