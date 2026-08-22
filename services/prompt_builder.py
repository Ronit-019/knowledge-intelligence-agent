from services.evidence_selector import EvidenceSelection


class PromptBuilder:
    """
    Builds grounded prompts for answer generation.
    """

    def build(
        self,
        query: str,
        evidence: EvidenceSelection,
        history=None,
    ) -> str:

        query = query.strip()

        if not query:
            raise ValueError(
                "Query cannot be empty."
            )

        if evidence.count == 0:
            raise ValueError(
                "Cannot build a grounded prompt without evidence."
            )

        evidence_blocks = []

        for index, result in enumerate(
            evidence.results,
            start=1,
        ):
            evidence_blocks.append(
                f"""
[EVIDENCE {index}]
Document: {result.title}
Document ID: {result.document_id}
Version: {result.version}
Status: {result.status}
Page: {result.page}
Chunk ID: {result.chunk_id}

Content:
{result.document.page_content}
""".strip()
            )

        formatted_evidence = "\n\n".join(
            evidence_blocks
        )

        history_text = ""

        if history:
            recent_history = history[-6:]

            history_text = "\n".join(
                f"{message.role.upper()}: {message.content}"
                for message in recent_history
            )

        # IMPORTANT:
        # Prompt must be returned regardless of whether
        # conversation history exists.

        return f"""
You are a knowledge intelligence assistant.

Answer the user's question using ONLY the evidence provided below.

Conversation history is provided only to understand
references and context. Conversation history is NOT evidence.

GROUNDING RULES:
1. Do not use outside knowledge.
2. Do not invent or assume information.
3. If the evidence does not contain enough information to answer the question,
   clearly say that the available documents do not contain enough information.
4. Preserve important numbers, dates, limits, requirements, and conditions
   exactly as supported by the evidence.
5. When the evidence contains conflicting versions, prefer the evidence
   marked as active.
6. Use conversation history only to understand what the user is referring to.
7. Do not treat previous assistant answers as authoritative facts.
8. Give a concise answer directly addressing the user's latest question.

CONVERSATION HISTORY:
{history_text if history_text else "No previous conversation."}

USER'S LATEST QUESTION:
{query}

RETRIEVED EVIDENCE:
{formatted_evidence}

ANSWER:
""".strip()