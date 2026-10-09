from hf import generate_response
import streamlit as st
import io

def role_prompt(role, question):
    return f"You are a {role}. Please answer the following question clearly:\n{question}"

def setup_ui():
    st.title("Enhanced AI Teaching Assistant")
    st.write("Ask questions and view your conversation history!")

    st.session_state.setdefault("conversation", [])

    role = st.selectbox("Select AI Role", ["Teacher", "Expert", "Friendly Helper"])
    user_input = st.text_input("Enter your question:", placeholder="What is photosynthesis?")

    c1, c2 = st.columns(2)
    with c1:
        ask = st.button("Ask")
    with c2:
        clear = st.button("Clear Conversation")

    if ask:
        if user_input.strip():
            prompt = role_prompt(role, user_input.strip())
            try:
                with st.spinner("Generating response..."):
                    answer = generate_response(prompt, temperature=0.3, max_tokens=1024)
            except Exception as e:
                answer = f"Error generating response: {e}"

            st.session_state.conversation.append({
                "role": role,
                "question": user_input.strip(),
                "answer": answer
            })
            st.rerun()
        else:
            st.warning("Please enter a question.")

    if clear:
        st.session_state.conversation = []
        st.rerun()

    if st.session_state.conversation:
        export_text = ""
        for i, chat in enumerate(st.session_state.conversation, 1):
            export_text += f"Q{i} ({chat['role']}): {chat['question']}\nA{i}: {chat['answer']}\n\n"

        st.download_button(
            "Export Chat History",
            io.BytesIO(export_text.encode("utf-8")),
            "conversation.txt",
            "text/plain"
        )

        st.markdown("### Conversation History")
        for chat in st.session_state.conversation:
            st.markdown(f"**You:** {chat['question']}")
            st.markdown(f"**AI ({chat['role']}):** {chat['answer']}")
            st.markdown("---")

def main():
    setup_ui()

if __name__ == "__main__":
    main()