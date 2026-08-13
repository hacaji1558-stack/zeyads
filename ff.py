import streamlit as st
import time
from google import genai

st.set_page_config(page_title="Ahmed's Elevator Portfolio", layout="wide")

if "floor" not in st.session_state:
    st.session_state.floor = 1

if "room" not in st.session_state:
    st.session_state.room = 1

if "hp" not in st.session_state:
    st.session_state.hp = 3

if "bot_messages" not in st.session_state:
    st.session_state.bot_messages = []

if "sisi_messages" not in st.session_state:
    st.session_state.sisi_messages = []

current_name = st.session_state.get("floor4_name_input", "").strip().lower()
show_clean_message = st.session_state.floor == 4 and current_name in ["mazen", "zeyad", "ziad", "devora", "esraa"]

if show_clean_message:
    if current_name == "mazen":
        st.write(
            "hey mazen i wanted to thank you for making me code , "
            "i always hated cooding and a came to this course so i prepare to second year of secondry school "
            "but i had so much fun and iam said to say goodbye , "
            "you were a great teacher and an amazing friend thank u"
        )
    elif current_name in ["zeyad", "ziad"]:
        st.write(
            "hey ziad i wanted to thank u for your efforts , "
            "unlike mazen i just knew u , but u were one of the best teachers i ever had , "
            "i want to say that i actually that was the best course i ever because of you"
        )
    elif current_name == "devora":
        st.write("WE WILL MISS YOU A LOT 💙")
    elif current_name == "esraa":
        st.write(
            "hey esraa i just wanted to say how much i love u and how much you made my life better , "
            "i really love u and thanks for making my life better"
        )

    st.write("")
    if st.button("⬅️ Back"):
        st.session_state["floor4_name_input"] = ""
        st.rerun()

else:
    target = st.sidebar.number_input("Destination Floor", 1, 5, st.session_state.floor)
    direction = st.sidebar.radio("Direction", ["Up", "Down"])
    passengers = st.sidebar.slider("Passengers", 0, 10, 1)
    go = st.sidebar.button("GO")

    st.title("Smart Elevator Dashboard")
    floor_ph = st.empty()
    status_ph = st.empty()
    bar_ph = st.empty()

    floor_ph.metric("CURRENT FLOOR", st.session_state.floor)
    status_ph.metric("STATUS", "IDLE")
    bar_ph.progress(0)

    if go:
        delay = 0.2 + passengers * 0.15
        step = 1 if target > st.session_state.floor else -1
        total = abs(target - st.session_state.floor) or 1

        status_ph.metric("STATUS", f"MOVING {direction.upper()}")
        moved = 0
        while st.session_state.floor != target:
            st.session_state.floor += step
            moved += 1
            floor_ph.metric("CURRENT FLOOR", st.session_state.floor)
            bar_ph.progress(moved / total)
            time.sleep(delay)

        status_ph.metric("STATUS", "ARRIVED")
        time.sleep(0.5)
        st.rerun()

    st.write("---")

    if st.session_state.floor == 1:
        st.title("Welcome to My Portfolio! 👋")
        st.write(
            "Hi, I'm Ahmed! I'm a high school student passionate about programming and web development. "
            "I started learning Python to build cool projects, and Streamlit allowed me to transform my scripts "
            "into interactive web apps. Check out my projects and learning journey using the elevator in the sidebar!"
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Grade", value="11th Grade")
        with col2:
            st.metric(label="Language", value="Python 📂 🐍")
        with col3:
            st.metric(label="Status", value="Building Projects")

        st.success("Select Destination Floor 2, 3, 4, or 5 in the sidebar elevator to explore!")

    elif st.session_state.floor == 2:
        st.header("🎮 Floor 2: The Escape Room Game")
        st.write("A text-based interactive adventure game using `st.session_state`.")

        if st.session_state.hp <= 0:
            st.error("💀 You have 0 HP. Game Over.")
            if st.button("Restart Game", key="restart_game"):
                st.session_state.hp = 3
                st.session_state.room = 1
                st.rerun()
        else:
            hearts = " ❤️ " * st.session_state.hp
            st.subheader(f"Current HP: {hearts}")

            if st.session_state.room == 1:
                st.subheader("Room 1: The Gate")
                choice = st.radio("Choose a door:", ["Left", "Right"], index=None, key="room1_choice")
                if st.button("Next", key="btn_room1"):
                    if choice is None:
                        st.warning("Please choose a door first!")
                    elif choice == "Left":
                        st.session_state.room = 2
                        st.rerun()
                    else:
                        st.error("Wrong choice! -1 HP")
                        st.session_state.hp -= 1
                        st.rerun()

            elif st.session_state.room == 2:
                st.subheader("Room 2: The Puzzle")
                choice = st.radio("Choose an answer:", ["A", "B"], index=None, key="room2_choice")
                if st.button("Next", key="btn_room2"):
                    if choice is None:
                        st.warning("Please choose an answer first!")
                    elif choice == "A":
                        st.session_state.room = 3
                        st.rerun()
                    else:
                        st.error("Wrong choice! -1 HP")
                        st.session_state.hp -= 1
                        st.session_state.room = 1
                        st.rerun()

            elif st.session_state.room == 3:
                st.success("🎉 You escaped!")
                if st.button("Play Again", key="play_again"):
                    st.session_state.hp = 3
                    st.session_state.room = 1
                    st.rerun()

    elif st.session_state.floor == 3:
        st.header("🤖 Floor 3: The Infinite Chatbot")
        st.write("A simple chat interface built using Streamlit native components.")

        for msg in st.session_state.bot_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if prompt := st.chat_input("Say something..."):
            st.session_state.bot_messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            bot_response = "Goodbye! Closing chat." if prompt.lower() == "bye" else "Hi! Say 'bye' to exit."

            st.session_state.bot_messages.append({"role": "assistant", "content": bot_response})
            with st.chat_message("assistant"):
                st.markdown(bot_response)

    elif st.session_state.floor == 4:
        st.header("🔒 Floor 4: Messages Lounge")
        st.write("Please enter your name to unlock your personalized floor view:")

        entered_name = st.text_input("Enter your name:", key="floor4_name_input").strip().lower()

        if entered_name and entered_name not in ["mazen", "zeyad", "ziad", "devora", "esraa"]:
            st.error("imposter get the fuck out")

    elif st.session_state.floor == 5:
        st.header("🇪🇬 Floor 5: Sisi AI")
        st.write("Chat with Sisi AI powered by Gemini!")

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
