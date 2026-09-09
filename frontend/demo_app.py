import sys
from pathlib import Path
from api.dependencies import build_knowledge_application
from services.conversation_service import ConversationMessage
import streamlit as st


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from api.dependencies import build_knowledge_application


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

.stApp {
    background: var(--background-color);
    color: var(--text-color);
}

.block-container {
    max-width: 1000px;
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
    background: var(--secondary-background-color);
    border: 1px solid rgba(128, 128, 128, 0.2);
    border-radius: 10px;
    padding: 0.7rem 0.9rem;
    margin-bottom: 1.5rem;
    font-size: 0.85rem;
}

.status-online {
    color: #22c55e;
    font-weight: 600;
}

.status-offline {
    color: #ef4444;
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
    margin-top: 0.5rem;
}

.empty-description {
    opacity: 0.6;
    font-size: 0.9rem;
    max-width: 500px;
    margin: auto;
}


/* -------------------------------------------------------
   Sources
------------------------------------------------------- */

.source-title {
    font-weight: 600;
    color: var(--text-color);
    margin-bottom: 0.25rem;
}

.source-meta {
    font-size: 0.8rem;
    opacity: 0.65;
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
   Hide Streamlit decoration
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
# KNOWLEDGE APPLICATION
# ============================================================

@st.cache_resource
def get_application():
    return build_knowledge_application()


# ============================================================
# LOAD KNOWLEDGE BASE
# ============================================================

try:

    with st.spinner("Loading knowledge base..."):
        application = get_application()

except Exception as exc:

    st.html(
        """
        <div class="status">
            <span class="status-offline">
                ● Knowledge base unavailable
            </span>
            <br>
            <span style="opacity:0.65;font-size:0.8rem;">
                The knowledge application could not be initialized.
            </span>
        </div>
        """
    )

    st.error(f"Knowledge base error: {exc}")

    st.stop()


# ============================================================
# HEADER
# ============================================================

st.html(
    """
    <div class="ki-header">

        <div class="ki-title">
            Knowledge Intelligence
        </div>

        <div class="ki-subtitle">
            Ask questions across your company's internal knowledge base.
        </div>

    </div>
    """
)


# ============================================================
# KNOWLEDGE BASE STATUS
# ============================================================

document_count = len(
    application.knowledge_base.documents
)

st.html(
    f"""
    <div class="status">

        <span class="status-online">
            ● Knowledge base ready · {document_count} active documents
        </span>

    </div>
    """
)


# ============================================================
# EMPTY STATE
# ============================================================

if not st.session_state.messages:

    st.html(
        """
        <div class="empty-state">

            <div class="empty-icon">
                🧠
            </div>

            <div class="empty-title">
                Ask your knowledge base
            </div>

            <div class="empty-description">
                Search company policies, security standards,
                HR documents, financial policies and other
                indexed knowledge.
            </div>

        </div>
        """
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

        # ----------------------------------------------------
        # USER
        # ----------------------------------------------------

        if role == "user":

            st.markdown(
                message["content"]
            )

        # ----------------------------------------------------
        # ASSISTANT
        # ----------------------------------------------------

        else:

            result = message["result"]


            # ------------------------------------------------
            # Answer
            # ------------------------------------------------

            st.markdown(
                result.answer
            )


            # ------------------------------------------------
            # Grounding
            # ------------------------------------------------

            if result.grounded:

                st.html(
                    """
                    <div class="grounded">
                        ✓ Grounded in company documents
                    </div>
                    """
                )

            else:

                st.html(
                    """
                    <div class="not-grounded">
                        ⚠ Not enough evidence in company documents
                    </div>
                    """
                )


            # ------------------------------------------------
            # Sources
            # ------------------------------------------------

            sources = result.sources.results

            if sources:

                with st.expander(
                    f"📚 Sources · {result.source_count}"
                ):

                    for index, source in enumerate(
                        sources,
                        start=1,
                    ):

                        st.markdown(
                            f"**{index}. 📄 {source.title}**"
                        )

                        st.caption(
                            f"{source.document_id} · "
                            f"Version {source.version} · "
                            f"Page {source.page} · "
                            f"Chunk {source.chunk_id}"
                        )

                        if source.rerank_score is not None:

                            st.caption(
                                f"Semantic relevance: "
                                f"{source.semantic_score:.3f} · "
                                f"Rerank relevance: "
                                f"{source.rerank_score:.3f}"
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


    # ========================================================
    # BUILD CONVERSATION HISTORY
    # ========================================================

    history = []

    for message in st.session_state.messages:

        if message["role"] == "user":

            history.append(
                ConversationMessage(
                    role="user",
                    content=message["content"],
                )
            )

        else:

            history.append(
                ConversationMessage(
                    role="assistant",
                    content=message["result"].answer,
                )
            )


    # ========================================================
    # SAVE USER MESSAGE
    # ========================================================

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )


    # ========================================================
    # DISPLAY USER MESSAGE
    # ========================================================

    with st.chat_message(
        "user",
        avatar="👤",
    ):

        st.markdown(
            prompt
        )


    # ========================================================
    # GENERATE ANSWER
    # ========================================================

    with st.chat_message(
        "assistant",
        avatar="🧠",
    ):

        with st.spinner(
            "Searching your knowledge base..."
        ):

            try:

                result = application.query_service.ask(
                    query=prompt,
                    history=history,
                )


                # ============================================
                # ANSWER
                # ============================================

                st.markdown(
                    result.answer
                )


                # ============================================
                # GROUNDING
                # ============================================

                if result.grounded:

                    st.html(
                        """
                        <div class="grounded">
                            ✓ Grounded in company documents
                        </div>
                        """
                    )

                else:

                    st.html(
                        """
                        <div class="not-grounded">
                            ⚠ Not enough evidence in company documents
                        </div>
                        """
                    )


                # ============================================
                # SOURCES
                # ============================================

                sources = result.sources.results

                if sources:

                    with st.expander(
                        f"📚 Sources · {result.source_count}"
                    ):

                        for index, source in enumerate(
                            sources,
                            start=1,
                        ):

                            st.markdown(
                                f"**{index}. 📄 {source.title}**"
                            )

                            st.caption(
                                f"{source.document_id} · "
                                f"Version {source.version} · "
                                f"Page {source.page} · "
                                f"Chunk {source.chunk_id}"
                            )

                            if source.rerank_score is not None:

                                st.caption(
                                    f"Semantic relevance: "
                                    f"{source.semantic_score:.3f} · "
                                    f"Rerank relevance: "
                                    f"{source.rerank_score:.3f}"
                                )

                            if index < len(sources):

                                st.divider()


                # ============================================
                # SAVE ASSISTANT RESPONSE
                # ============================================

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "result": result,
                    }
                )


            # ================================================
            # ERROR HANDLING
            # ================================================

            except Exception as exc:

                st.error(
                    f"Unexpected error: {exc}"
                )