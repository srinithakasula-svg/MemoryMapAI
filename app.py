import os

import streamlit as st

from document_processor import (
    extract_text,
    split_text
)

from rag import (
    save_documents,
    search_documents,
    get_document_names,
    get_document_count,
    get_chunk_count,
    get_document_chunks,
    delete_document
)

from ai import (
    ask_ai,
    generate_quiz
)

from quiz import (
    calculate_score,
    performance_level,
    get_recommendation,
    find_weak_topics
)


# ==================================================
# PAGE SETTINGS
# ==================================================

st.set_page_config(
    page_title="***MemoryMap AI***",
    page_icon="🧠",
    layout="wide"
)


# ==================================================
# SESSION STATE
# ==================================================

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = []

if "latest_score" not in st.session_state:
    st.session_state.latest_score = None

if "weak_topics" not in st.session_state:
    st.session_state.weak_topics = []


# ==================================================
# CUSTOM DESIGN
# ==================================================

st.markdown(
    """
    <style>

    .stApp {
    background: linear-gradient(
        135deg,
        #EEF2FF 0%,
        #F5F3FF 45%,
        #ECFEFF 100%
    );
}

    .hero {
        background: linear-gradient(
            135deg,
            #6C63FF,
            #8B5CF6,
            #00BFA6
        );

        padding: 35px;
        border-radius: 22px;
        color: white;
        margin-bottom: 25px;
    }

    .hero h1 {
        color: white;
        font-size: 42px;
        margin-bottom: 5px;
    }

    .hero p {
        color: white;
        font-size: 17px;
    }

    .card {
        background: white;
        padding: 22px;
        border-radius: 18px;
        border: 1px solid #E5E7EB;
        box-shadow: 0px 5px 20px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }

    .number {
        font-size: 32px;
        font-weight: bold;
        color: #635BFF;
    }

    .label {
        color: #667085;
        font-size: 14px;
    }

    .answer {
        background: white;
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #635BFF;
        box-shadow: 0px 5px 20px rgba(0,0,0,0.05);
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.markdown(
        "# 🧠 **MemoryMap AI**"
    )

    st.caption(
        "Personal Revision Platform"
    )

    st.divider()

    if st.button(
        "🏠 Dashboard",
        use_container_width=True
    ):
        st.session_state.page = "Dashboard"

    if st.button(
        "📚 My Notes",
        use_container_width=True
    ):
        st.session_state.page = "My Notes"

    if st.button(
        "💬 Ask AI",
        use_container_width=True
    ):
        st.session_state.page = "Ask AI"

    if st.button(
        "📝 AI Quiz",
        use_container_width=True
    ):
        st.session_state.page = "AI Quiz"

    if st.button(
        "📊 Performance",
        use_container_width=True
    ):
        st.session_state.page = "Performance"

    st.divider()

    st.markdown("### 📌 Quick Stats")

    st.metric(
        "Documents",
        get_document_count()
    )

    st.metric(
        "Note Chunks",
        get_chunk_count()
    )


# ==================================================
# HEADER
# ==================================================

# ==================================================
# HEADER
# ==================================================

st.markdown(
    """
    <div class="hero">
        <h1>🧠 MemoryMap AI</h1>
        <p>
            Turn your study notes into an intelligent
            learning experience.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ==================================================
# DASHBOARD
# ==================================================

# ==================================================
# DASHBOARD
# ==================================================

if st.session_state.page == "Dashboard":

    st.title(
        "Learning Dashboard"
    )

    st.write(
        "Your personal study intelligence center."
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📚 Documents",
            get_document_count()
        )

    with col2:

        st.metric(
            "🧩 Note Chunks",
            get_chunk_count()
        )

    with col3:

        score = st.session_state.latest_score

        score_text = (
            f"{score}%"
            if score is not None
            else "--"
        )

        st.metric(
            "🎯 Latest Score",
            score_text
        )

    with col4:

        st.metric(
            "⚠️ Weak Topics",
            len(st.session_state.weak_topics)
        )

    st.markdown(
        "### 🚀 What can you do?"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            "📚 **Upload Notes**\n\n"
            "Build your personal study knowledge base."
        )

    with col2:

        st.info(
            "💬 **Ask AI**\n\n"
            "Ask questions directly from your notes."
        )

    with col3:

        st.info(
            "📝 **AI Quiz**\n\n"
            "Generate quizzes and identify weak topics."
        )
# ==================================================
# ASK AI
# ==================================================

elif st.session_state.page == "Ask AI":

    st.title(
        "💬 Ask AI"
    )

    st.write(
        "Ask questions from your uploaded notes."
    )

    question = st.text_area(
        "Your question",
        placeholder=(
            "Example: What is inheritance?"
        ),
        height=120
    )

    if st.button(
        "🔍 Ask from My Notes",
        type="primary"
    ):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        elif get_chunk_count() == 0:

            st.warning(
                "Please upload and process notes first."
            )

        else:

            with st.spinner(
                "Searching your notes..."
            ):

                results = search_documents(
                    question,
                    5
                )

            if not results:

                st.warning(
                    "I couldn't find this information "
                    "in your uploaded notes."
                )

            else:

                context = "\n\n".join(
                    result["text"]
                    for result in results
                )

                with st.spinner(
                    "Generating answer..."
                ):

                    answer = ask_ai(
                        question,
                        context
                    )

                st.markdown(
                    "### 💡 Answer"
                )

                st.markdown(
                    f"""
                    <div class="answer">
                    {answer}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    "### 📚 Relevant Notes"
                )

                for index, result in enumerate(
                    results,
                    1
                ):

                    with st.expander(
                        f"Note {index} — {result['source']}"
                    ):

                        st.write(
                            result["text"]
                        )


# ==================================================
# AI QUIZ
# ==================================================


# ==================================================
# MY NOTES
# ==================================================

elif st.session_state.page == "My Notes":

    st.title("📚 My Notes")

    st.write(
        "Upload your study material and build your personal knowledge base."
    )

    st.markdown("### 📤 Upload File")

    uploaded_file = st.file_uploader(
        "Choose a TXT or CSV file",
        type=["txt", "csv"],
        help="Upload your study notes in TXT or CSV format."
    )

    if uploaded_file is not None:

        st.success(
            f"Selected file: {uploaded_file.name}"
        )

        file_path = os.path.join(
            "documents",
            uploaded_file.name
        )

        with open(
            file_path,
            "wb"
        ) as file:

            file.write(
                uploaded_file.getbuffer()
            )

        if st.button(
            "🚀 Process Notes",
            type="primary"
        ):

            with st.spinner(
                "Reading and processing notes..."
            ):

                text = extract_text(
                    file_path
                )

                chunks = split_text(
                    text
                )

                if not chunks:

                    st.error(
                        "No readable text found."
                    )

                else:

                    count = save_documents(
                        chunks,
                        uploaded_file.name
                    )

                    st.success(
                        f"{count} note chunks stored successfully!"
                    )

    st.markdown(
        "### 📖 Your Documents"
    )

    documents = get_document_names()

    if not documents:

        st.info(
            "No notes uploaded yet."
        )

    else:

        for document in documents:

            col1, col2 = st.columns(
                [5, 1]
            )

            with col1:

                chunks = get_document_chunks(
                    document
                )

                st.markdown(
                    f"""
                    <div class="card">

                    📄 <b>{document}</b>

                    <br><br>

                    🧩 {len(chunks)} chunks

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col2:

                if st.button(
                    "Delete",
                    key=f"delete_{document}"
                ):

                    delete_document(
                        document
                    )

                    st.rerun()



# ==================================================
# AI QUIZ
# ==================================================

elif st.session_state.page == "AI Quiz":

    st.title("📝 AI Quiz")

    st.write(
        "Generate questions dynamically from your uploaded notes."
    )

    documents = get_document_names()

    if not documents:

        st.warning(
            "📚 No notes found. Please go to My Notes and upload a TXT or CSV file first."
        )

    else:

        st.success(
            f"📚 {len(documents)} document(s) available for quiz generation."
        )

        selected_document = st.selectbox(
            "📖 Select your notes",
            documents
        )

        number_of_questions = st.slider(
            "🔢 Number of questions",
            min_value=3,
            max_value=10,
            value=5
        )

        st.write(
            f"Quiz will contain **{number_of_questions} questions**."
        )

        if st.button(
            "✨ Generate Quiz",
            type="primary",
            use_container_width=True
        ):

            chunks = get_document_chunks(
                selected_document
            )

            if not chunks:

                st.error(
                    "No content found in the selected document."
                )

            else:

                context = "\n\n".join(
                    chunks
                )[:6000]
                with st.spinner(
                    "🤖 AI is generating your quiz..."
                ):

                    quiz = generate_quiz(
                        context,
                        number_of_questions
                    )

                if quiz:

                    st.session_state.quiz_data = quiz

                    st.success(
                        f"🎉 {len(quiz)} questions generated successfully!"
                    )

                else:

                    st.error(
                        "❌ Quiz generation failed. "
                        "Please check that Ollama is running and try again."
                    )

        if st.session_state.quiz_data:

            st.markdown(
                "### 🎯 Answer the Questions"
            )

            user_answers = {}

            for index, question in enumerate(
                st.session_state.quiz_data
            ):

                st.markdown(
                    f"### Q{index + 1}. "
                    f"{question['question']}"
                )

                user_answers[index] = st.radio(
                    "Choose your answer:",
                    question["options"],
                    key=f"quiz_{index}"
                )

                st.divider()

            if st.button(
                "✅ Submit Quiz",
                type="primary",
                use_container_width=True
            ):

                correct = 0

                answer_indexes = {}

                for index, question in enumerate(
                    st.session_state.quiz_data
                ):

                    selected = user_answers[index]

                    options = question["options"]

                    selected_index = options.index(
                        selected
                    )

                    answer_indexes[index] = (
                        selected_index
                    )

                    if selected_index == question["answer"]:

                        correct += 1

                total = len(
                    st.session_state.quiz_data
                )

                score = calculate_score(
                    correct,
                    total
                )

                st.session_state.latest_score = score

                st.session_state.weak_topics = (
                    find_weak_topics(
                        st.session_state.quiz_data,
                        answer_indexes
                    )
                )

                st.success(
                    f"🎉 Your Score: {score}%"
                )

                st.info(
                    f"Correct Answers: {correct} / {total}"
                )

                st.balloons()

# ==================================================
# PERFORMANCE
# ==================================================

elif st.session_state.page == "Performance":

    st.title(
        "📊 Performance"
    )

    score = st.session_state.latest_score

    if score is None:

        st.info(
            "Complete a quiz to see your performance."
        )

    else:

        st.metric(
            "Latest Score",
            f"{score}%"
        )

        st.progress(
            min(score / 100, 1.0)
        )

        st.subheader(
            performance_level(score)
        )

        st.markdown(
            "### 💡 Recommendation"
        )

        st.info(
            get_recommendation(score)
        )

        st.markdown(
            "### ⚠️ Weak Topics"
        )

        if st.session_state.weak_topics:

            for topic in st.session_state.weak_topics:

                st.warning(
                    f"📌 {topic}"
                )

        else:

            st.success(
                "Excellent! No weak topics detected."
            )