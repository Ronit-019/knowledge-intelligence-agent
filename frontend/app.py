import os
import requests
import streamlit as st


# ============================================================
# CONFIG
# ============================================================

API_URL = os.getenv(
    "KNOWLEDGE_API_URL",
    "http://127.0.0.1:8000",
)


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="Knowledge Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# THEME-SAFE CSS
# ============================================================

st.markdown(
    """
    <style>

    /* -------------------------------------------------------
       Global
    ------------------------------------------------------- */

    .stApp {
        background: var(--background-color);
        color: var(--text-color);
    }

    .block-container {
        max-width: 1100px;
        padding-top: 2.5rem;
        padding-bottom: 5rem;
    }

    /* -------------------------------------------------------
       Header
    ------------------------------------------------------- */

    .ki-header {
        margin-bottom: 1.8rem;
    }

    .ki-title {
        font-size: 2.2rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        color: var(--text-color);
        margin-bottom: 0.25rem;
    }

    .ki-subtitle {
        color: var(--text-color);
        opacity: 0.65;
        font-size: 0.95rem;
    }

    /* -------------------------------------------------------
       Status
    ------------------------------------------------------- */

    .status {
        border: 1px solid var(--secondary-background-color);
        background: var(--secondary-background-color);
        color: var(--text-color);
        border-radius: 10px;
        padding: 0.65rem 0.9rem;
        margin-bottom: 1.5rem;
        font-size: 0.85rem;
    }

    .status-online {
        color: #22c55e;
        font-weight: 600;
    }

    /* -------------------------------------------------------
       Chat
    ------------------------------------------------------- */

    [data-testid="stChatMessage"] {
        background: transparent;
        border: none;
    }

    [data-testid="stChatMessageContent"] {
        color: var(--text-color);
    }

    /* -------------------------------------------------------
       Markdown inside chat
    ------------------------------------------------------- */

    [data-testid="stChatMessageContent"] p,
    [data-testid="stChatMessageContent"] li,
    [data-testid="stChatMessageContent"] span,
    [data-testid="stChatMessageContent"] strong {
        color: inherit;
    }

    [data-testid="stChatMessageContent"] code {
        background: rgba(128, 128, 128, 0.15);
        color: inherit;
    }


    /* -------------------------------------------------------
       Grounding
    ------------------------------------------------------- */

    .grounded {
        color: #22c55e;
        font-size: 0.78rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }

    .not-grounded {
        color: #f59e0b;
        font-size: 0.78rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }

    /* -------------------------------------------------------
       Empty state
    ------------------------------------------------------- */

    .empty-state {
        text-align: center;
        padding: 5rem 1rem 3rem;
        color: var(--text-color);
    }

    .empty-icon {
        font-size: 3rem;
        margin-bottom: 0.7rem;
    }

    .empty-title {
        font-size: 1.4rem;
        font-weight: 600;
    }

    .empty-description {
        opacity: 0.6;
        font-size: 0.9rem;
        max-width: 500px;
        margin: 0 auto;
    }

    /* -------------------------------------------------------
       Chat input
    ------------------------------------------------------- */

    [data-testid="stChatInput"] {
        background: var(--background-color);
    }

    /* -------------------------------------------------------
       Buttons
    ------------------------------------------------------- */

    div.stButton > button {
        border-radius: 8px;
    }

    /* -------------------------------------------------------
       Hide unnecessary Streamlit decoration
    ------------------------------------------------------- */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# API
# ============================================================

def check_api() -> bool:
    try:
        response = requests.get(
            f"{API_URL}/health",
            timeout=3,
        )

        return response.status_code == 200

    except requests.RequestException:
        return False


def ask_knowledge_base(
    query: str,
    history: list[dict],
):
    response = requests.post(
        f"{API_URL}/query",
        json={
            "query": query,
            "history": history,
        },
        timeout=120,
    )

    response.raise_for_status()

    return response.json()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="ki-header">
        <div class="ki-title">Knowledge Intelligence</div>
        <div class="ki-subtitle">
            Ask questions across your company's internal knowledge base.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>

    .stApp {
        background: var(--background-color);
        color: var(--text-color);
    }

    .block-container {
        max-width: 1000px;
        padding-top: 2.5rem;
        padding-bottom: 5rem;
    }

    .ki-title {
        font-size: 2.2rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        color: var(--text-color);
    }

    .ki-subtitle {
        color: var(--text-color);
        opacity: 0.65;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }

    .status {
        background: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 10px;
        padding: 0.7rem 0.9rem;
        margin-bottom: 1.5rem;
        font-size: 0.85rem;
    }

    .grounded {
        color: #22c55e;
        font-size: 0.78rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }

    .not-grounded {
        color: #f59e0b;
        font-size: 0.78rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }

    .empty-state {
        text-align: center;
        padding: 5rem 1rem 3rem;
        color: var(--text-color);
    }

    .empty-icon {
        font-size: 3rem;
    }

    .empty-title {
        font-size: 1.4rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }

    .empty-description {
        opacity: 0.6;
        font-size: 0.9rem;
        max-width: 500px;
        margin: auto;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)
# ============================================================
# API STATUS
# ============================================================

api_online = check_api()

if api_online:
    st.markdown(
        """
        <div class="status">
            <span class="status-online">● Knowledge API online</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <div class="status">
            <span style="color:#ef4444;font-weight:600;">
                ● Knowledge API offline
            </span>
            <br>
            <span style="opacity:0.65;font-size:0.8rem;">
                Start the FastAPI server before asking a question.
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# EMPTY STATE
# ============================================================

if not st.session_state.messages:

    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-icon">🧠</div>
            <div class="empty-title">
                Ask your knowledge base
            </div>
            <div class="empty-description">
                Search company policies, security standards,
                HR documents, financial policies and other
                indexed knowledge.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    role = message["role"]

    with st.chat_message(
        role,
        avatar="👤" if role == "user" else "🧠",
    ):

        if role == "user":

            st.markdown(
                message["content"]
            )

        else:

            result = message["result"]

            # -----------------------------------------------
            # Answer
            # -----------------------------------------------

            st.markdown(
                result["answer"]
            )

            # -----------------------------------------------
            # Grounding
            # -----------------------------------------------

            if result["grounded"]:

                st.markdown(
                    """
                    <div class="grounded">
                        ✓ Grounded in company documents
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            else:

                st.markdown(
                    """
                    <div class="not-grounded">
                        ⚠ Not enough evidence in company documents
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # -----------------------------------------------
            # Sources
            # -----------------------------------------------

            sources = result.get(
                "sources",
                [],
            )

            if sources:

                with st.expander(
                    f"📚 Sources · {len(sources)}"
                ):

                    for index, source in enumerate(
                        sources,
                        start=1,
                    ):

                        st.markdown(
                            f"**{index}. 📄 {source['title']}**"
                        )

                        st.caption(
                            f"{source['document_id']} · "
                            f"Version {source['version']} · "
                            f"Page {source['page']} · "
                            f"Chunk {source['chunk_id']}"
                        )

                        if source.get("rerank_score") is not None:

                            st.caption(
                                f"Semantic relevance: "
                                f"{source['semantic_score']:.3f} · "
                                f"Rerank relevance: "
                                f"{source['rerank_score']:.3f}"
                            )

                        if index < len(sources):
                            st.divider()


# ============================================================
# CHAT INPUT
# ============================================================

prompt = st.chat_input(
    "Ask a question about your company knowledge..."
)


# ============================================================
# NEW QUESTION
# ============================================================

if prompt:

    prompt = prompt.strip()

    if not prompt:
        st.stop()

    # -----------------------------------------------
    # Add user message
    # -----------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    # -----------------------------------------------
    # Display user message immediately
    # -----------------------------------------------

    with st.chat_message(
        "user",
        avatar="👤",
    ):
        st.markdown(prompt)

    # -----------------------------------------------
    # Generate answer
    # -----------------------------------------------

    with st.chat_message(
        "assistant",
        avatar="🧠",
    ):

        with st.spinner(
            "Searching your knowledge base..."
        ):

            try:

                history = [
                    {
                        "role": message["role"],
                        "content": (
                            message["content"]
                            if message["role"] == "user"
                            else message["result"]["answer"]
                        ),
                    }
                    for message in st.session_state.messages
                ]

                result = ask_knowledge_base(
                    prompt,
                    history,
                )

                # ---------------------------------------
                # Answer
                # ---------------------------------------

                st.markdown(
                    result["answer"]
                )

                # ---------------------------------------
                # Grounding
                # ---------------------------------------

                if result["grounded"]:

                    st.markdown(
                        """
                        <div class="grounded">
                            ✓ Grounded in company documents
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                else:

                    st.markdown(
                        """
                        <div class="not-grounded">
                            ⚠ Not enough evidence in company documents
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                # ---------------------------------------
                # Sources
                # ---------------------------------------

                sources = result.get(
                    "sources",
                    [],
                )

                if sources:

                    with st.expander(
                        f"Sources · {len(sources)}"
                    ):

                        for source in sources:

                            st.markdown(
                                f"""
                                <div class="source-card">

                                    <div class="source-title">
                                        {source["title"]}
                                    </div>

                                    <div class="source-meta">
                                        {source["document_id"]}
                                        · Version {source["version"]}
                                        · Page {source["page"]}
                                    </div>

                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                # ---------------------------------------
                # Save assistant response
                # ---------------------------------------

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "result": result,
                    }
                )

            except requests.HTTPError as exc:

                st.error(
                    f"Knowledge API error: {exc}"
                )

            except requests.RequestException:

                st.error(
                    "Could not connect to the Knowledge API."
                )

            except Exception as exc:

                st.error(
                    f"Unexpected error: {exc}"
                )