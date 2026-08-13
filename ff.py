elif st.session_state.floor == 5:
        st.header("🇪🇬 Floor 5: Sisi AI")
        st.write("Chat with Sisi AI powered by Gemini!")

        # Pulls the key safely from local secrets file or Streamlit Cloud Settings
        api_key = st.secrets.get("GEMINI_API_KEY", "")

        if not api_key:
            st.error("API Key not found! Please check your secrets configuration.")
        else:
            client = genai.Client(api_key=api_key)

            for message in st.session_state.sisi_messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            if prompt := st.chat_input("Ask me anything..."):
                with st.chat_message("user"):
                    st.markdown(prompt)
                st.session_state.sisi_messages.append({"role": "user", "content": prompt})

                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        try:
                            response = client.interactions.create(
                                model="gemini-3.6-flash",
                                input=prompt
                            )
                            bot_reply = response.output_text
                        except Exception as e:
                            bot_reply = f"Error generating response: {e}"

                    st.markdown(bot_reply)
                st.session_state.sisi_messages.append({"role": "assistant", "content": bot_reply})