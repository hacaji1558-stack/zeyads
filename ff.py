import streamlit as st
import time
import os
import plotly.graph_objects as px_go
from google import genai

st.set_page_config(page_title="med7at saleh", layout="wide")

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

if "habits_data" not in st.session_state:
    st.session_state.habits_data = {}

if "custom_categories" not in st.session_state:
    st.session_state.custom_categories = []

if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = 0

if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0

if "quiz_answered" not in st.session_state:
    st.session_state.quiz_answered = False

if "show_flashcard_answer" not in st.session_state:
    st.session_state.show_flashcard_answer = False

if "last_card_idx" not in st.session_state:
    st.session_state.last_card_idx = 0

if "show_dropdown" not in st.session_state:
    st.session_state.show_dropdown = False

if "selected_person" not in st.session_state:
    st.session_state.selected_person = "Zeyad"


target = st.sidebar.number_input("Destination Floor", 1, 8, st.session_state.floor)
direction = st.sidebar.radio("Direction", ["Up", "Down"])
passengers = st.sidebar.slider("Passengers", 0, 10, 1)
elevator_btn = st.sidebar.button("GO")

st.title("Smart Elevator Dashboard")
floor_ph = st.empty()
status_ph = st.empty()
bar_ph = st.empty()

floor_ph.metric("CURRENT FLOOR", st.session_state.floor)
status_ph.metric("STATUS", "IDLE")
bar_ph.progress(0)

if elevator_btn:
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
    st.title("Welcome to the Portfolio Directory! 👋")


    PROFILES = {
        "Zeyad": {
            "title": "Profile: Zeyad 👨‍💻",
            "bio": (
                "Welcome to Zeyad's profile! Zeyad is currently an 11th grade high school student "
                "exploring computer science, web development, and interactive coding."
            ),
            "metrics": {
                "Grade": "11th Grade",
                "Role": "Student / Instructor",
                "Status": "Active Learning"
            }
        },
        "adam": { 
            "title": "Profile: adam 👤",
            "bio": "Welcome to adam profile! adam is currently an 8th grade high school student "
                "exploring computer science, web development, and interactive coding",
            "metrics": {
                "Grade": "8th",
                "Role": "Role / Specialization",
                "Status": "student"
            }
        },
        "basem": {  
            "title": "Profile: bassem 👤",
            "bio": "Welcome to basem profile! basem is currently an 8th grade high school student "
                "exploring computer science, web development, and interactive coding",
            "metrics": {
                "Grade": "8th",
                "Role": "Role / Specialization",
                "Status": "student"
            }
        }
    }

    profile_names = list(PROFILES.keys())


    if st.session_state.get("selected_person") not in profile_names:
        st.session_state.selected_person = profile_names[0]

    if st.button("Select Person Info"):
        st.session_state.show_dropdown = not st.session_state.show_dropdown

    if st.session_state.show_dropdown:
        st.session_state.selected_person = st.selectbox(
            "Choose a person to display profile:",
            profile_names,
            index=profile_names.index(st.session_state.selected_person)
        )

    st.write("---")

    active_person = st.session_state.selected_person
    p_data = PROFILES[active_person]

    st.subheader(p_data["title"])
    st.write(p_data["bio"])

    col1, col2, col3 = st.columns(3)
    metrics_items = list(p_data["metrics"].items())

    with col1:
        st.metric(label=metrics_items[0][0], value=metrics_items[0][1])
    with col2:
        st.metric(label=metrics_items[1][0], value=metrics_items[1][1])
    with col3:
        st.metric(label=metrics_items[2][0], value=metrics_items[2][1])

    st.success("Select Destination Floor 2 to 8 in the sidebar elevator to explore!")

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
    st.header("🇪🇬 Floor 4: Sisi AI")
    st.write("Chat with Sisi AI powered by Gemini!")

    api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

    if not api_key:
        st.error("API Key missing! Add GEMINI_API_KEY to .streamlit/secrets.toml")
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
                        response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=prompt
                        )
                        bot_reply = response.text
                    except Exception as e:
                        bot_reply = f"Error generating response: {e}"

                st.markdown(bot_reply)
            st.session_state.sisi_messages.append({"role": "assistant", "content": bot_reply})

elif st.session_state.floor == 5:
    st.header("📈 Floor 5: Interactive Habit & Goal Tracker")
    st.write("Set habits, log daily progress, and track your active streak.")

    col_habits, col_stats = st.columns([2, 1])

    with col_habits:
        selected_date = st.date_input("Select Logging Day", key="habit_date")
        date_str = str(selected_date)

        if date_str not in st.session_state.habits_data:
            st.session_state.habits_data[date_str] = {
                "Drink 2L Water": False,
                "Read 10 Pages": False,
                "Code for 30 mins": False,
                "Exercise for 20 mins": False
            }

        st.subheader(f"Habits for {date_str}")
        daily_habits = st.session_state.habits_data[date_str]

        completed_count = 0
        total_habits = len(daily_habits)

        for habit_name in list(daily_habits.keys()):
            is_checked = st.checkbox(
                habit_name,
                value=daily_habits[habit_name],
                key=f"{date_str}_{habit_name}"
            )
            st.session_state.habits_data[date_str][habit_name] = is_checked
            if is_checked:
                completed_count += 1

    with col_stats:
        st.subheader("Progress & Statistics")
        progress_ratio = completed_count / total_habits if total_habits > 0 else 0.0

        st.write(f"**Completion Rate:** {int(progress_ratio * 100)}%")
        st.progress(progress_ratio)

        all_dates = sorted(list(st.session_state.habits_data.keys()), reverse=True)
        streak = 0
        for d in all_dates:
            habits_dict = st.session_state.habits_data[d]
            if all(habits_dict.values()) and len(habits_dict) > 0:
                streak += 1
            else:
                break

        st.metric("Current Streak", f"{streak} Days")

        if progress_ratio == 1.0:
            st.balloons()
            st.success("🎉 Fantastic! All daily habits completed!")

elif st.session_state.floor == 6:
    st.header("💰 Floor 6: Smart Expense & Budget Planner")
    st.write("Track monthly income, monitor expense categories, and view real-time budget health.")

    currency = st.selectbox("Select Currency", ["$", "€", "£", "EGP"], index=0)

    col_in, col_exp = st.columns(2)

    with col_in:
        st.subheader("Income & Standard Expenses")
        income = st.number_input(f"Monthly Income ({currency})", min_value=0.0, value=1000.0, step=50.0)

        food = st.number_input(f"Food ({currency})", min_value=0.0, value=200.0, step=10.0)
        transport = st.number_input(f"Transport ({currency})", min_value=0.0, value=100.0, step=10.0)
        entertainment = st.number_input(f"Entertainment ({currency})", min_value=0.0, value=150.0, step=10.0)
        tech = st.number_input(f"Tech ({currency})", min_value=0.0, value=100.0, step=10.0)

    with col_exp:
        st.subheader("Dynamic Custom Categories")
        with st.form("custom_category_form", clear_on_submit=True):
            c_name = st.text_input("Category Name")
            c_val = st.number_input("Amount", min_value=0.0, value=0.0)
            if st.form_submit_button("Add Category") and c_name.strip():
                st.session_state.custom_categories.append({"name": c_name.strip(), "amount": c_val})
                st.rerun()

        custom_expenses_dict = {}
        if st.session_state.custom_categories:
            st.write("**Added Categories:**")
            for item in st.session_state.custom_categories:
                st.write(f"- {item['name']}: {item['amount']} {currency}")
                custom_expenses_dict[item["name"]] = item["amount"]

    expenses_dict = {
        "Food": food,
        "Transport": transport,
        "Entertainment": entertainment,
        "Tech": tech,
        **custom_expenses_dict
    }

    total_expenses = sum(expenses_dict.values())
    remaining_balance = income - total_expenses

    st.write("---")
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("Total Income", f"{income:.2f} {currency}")
    m_col2.metric("Total Expenses", f"{total_expenses:.2f} {currency}")
    m_col3.metric("Remaining Balance", f"{remaining_balance:.2f} {currency}")

    if total_expenses > income:
        st.error("⚠️ Warning: You are over budget!")
    else:
        st.success("✅ You are within budget!")

    categories = list(expenses_dict.keys())
    amounts = list(expenses_dict.values())

    with st.expander("📊 View Expense Visualization Breakdown", expanded=True):
        chart_col1, chart_col2 = st.columns(2)

        static_config = {"staticPlot": True}

        with chart_col1:
            st.subheader("Pie Chart Breakdown")
            fig_pie = px_go.Figure(data=[px_go.Pie(labels=categories, values=amounts, hole=0.3)])
            fig_pie.update_layout(margin=dict(t=20, b=20, l=20, r=20))
            st.plotly_chart(fig_pie, use_container_width=True, config=static_config)

        with chart_col2:
            st.subheader("Bar Graph Breakdown")
            fig_bar = px_go.Figure(data=[px_go.Bar(x=categories, y=amounts)])
            fig_bar.update_layout(margin=dict(t=20, b=20, l=20, r=20), yaxis_title=f"Amount ({currency})")
            st.plotly_chart(fig_bar, use_container_width=True, config=static_config)

elif st.session_state.floor == 7:
    st.header("🧠 Floor 7: Mini Study Flashcard & Quiz App")
    st.write("Master your knowledge with quick flashcard review or interactive quiz mode!")

    quiz_dataset = [
        {
            "question": "What is the primary function of Streamlit?",
            "options": ["Building web applications rapidly in Python", "Managing SQL Databases", "Compiling C++ code", "Designing vector graphics"],
            "answer": "Building web applications rapidly in Python"
        },
        {
            "question": "Which parameter stores variables across reruns in Streamlit?",
            "options": ["st.memory", "st.session_state", "st.cache_data", "st.save_state"],
            "answer": "st.session_state"
        },
        {
            "question": "What key component is used to manage API keys securely on Streamlit Cloud?",
            "options": ["st.secrets", "st.env", "st.passwords", "st.private"],
            "answer": "st.secrets"
        },
        {
            "question": "Which function displays interactive multiple choice options in Streamlit?",
            "options": ["st.selectbox", "st.radio", "st.checkbox", "All of the above"],
            "answer": "All of the above"
        },
        {
            "question": "Which Python library is natively used for Gemini AI integration?",
            "options": ["google-genai", "openai", "requests", "flask"],
            "answer": "google-genai"
        }
    ]

    mode = st.toggle("📚 Enable Study Mode (Flashcards)", value=False)

    if mode:
        st.subheader("Study Mode - Flashcards")
        card_idx = st.slider("Select Card", 1, len(quiz_dataset), 1) - 1

        # Check if user moved to a different card; reset answer visibility if so
        if card_idx != st.session_state.last_card_idx:
            st.session_state.show_flashcard_answer = False
            st.session_state.last_card_idx = card_idx

        card = quiz_dataset[card_idx]

        st.info(f"**Question {card_idx + 1}:**\n\n{card['question']}")

        if st.button("Flip Flashcard"):
            st.session_state.show_flashcard_answer = not st.session_state.show_flashcard_answer

        if st.session_state.show_flashcard_answer:
            st.success(f"**Answer:**\n\n{card['answer']}")

    else:
        st.subheader("Quiz Mode")
        idx = st.session_state.quiz_index

        if idx < len(quiz_dataset):
            q = quiz_dataset[idx]
            st.write(f"**Question {idx + 1} of {len(quiz_dataset)}:**")
            st.write(f"### {q['question']}")

            selected_opt = st.radio("Choose your answer:", q["options"], index=None, key=f"q_radio_{idx}")

            col_sub, col_nxt = st.columns(2)

            with col_sub:
                if st.button("Submit Answer", disabled=st.session_state.quiz_answered):
                    if selected_opt is None:
                        st.warning("Please select an answer first!")
                    else:
                        st.session_state.quiz_answered = True
                        if selected_opt == q["answer"]:
                            st.session_state.quiz_score += 1
                            st.success("✅ Correct!")
                        else:
                            st.error(f"❌ Incorrect. The correct answer was: {q['answer']}")

            with col_nxt:
                if st.session_state.quiz_answered:
                    if st.button("Next Question ➡️"):
                        st.session_state.quiz_index += 1
                        st.session_state.quiz_answered = False
                        st.rerun()

        else:
            st.balloons()
            st.subheader("🎉 Quiz Completed!")
            st.write(f"You scored **{st.session_state.quiz_score} / {len(quiz_dataset)}**!")

            if st.button("Restart Quiz"):
                st.session_state.quiz_index = 0
                st.session_state.quiz_score = 0
                st.session_state.quiz_answered = False
                st.rerun()

elif st.session_state.floor == 8:
    st.header("🔒 Floor 8: Messages Lounge")
    entered_name = st.text_input("Enter your name to unlock your floor:", key="floor8_name_input").strip().lower()

    if entered_name:
        if entered_name == "mazen":
            st.write(
                "hey mazen i wanted to thank you for making me code , "
                "i always hated cooding and a came to this course so i prepare to second year of secondry school "
                "but i had so much fun and iam said to say goodbye , "
                "you were a great teacher and an amazing friend thank u"
            )
        elif entered_name in ["zeyad", "ziad"]:
            st.write(
                "hey ziad i wanted to thank u for your efforts , "
                "unlike mazen i just knew u , but u were one of the best teachers i ever had , "
                "i want to say that i actually that was the best course i ever because of you"
            )
        elif entered_name == "devora":
            st.write("WE WILL MISS YOU A LOT 💙")
        else:
            st.error("imposter get out")
