from services.evidence_selector import EvidenceSelection


class PromptBuilder:
    """
    Builds grounded prompts for answer generation.

    The prompt builder is responsible for:
    - Formatting the user's question
    - Formatting retrieved evidence
    - Applying grounding instructions
    - Preventing the LLM from relying on outside knowledge
    """

    def build(
        self,
        query: str,
        evidence: EvidenceSelection,
    ) -> str:
        """
        Build a grounded prompt from a user query
        and selected evidence.
        """

        query = query.strip()

        if not query:
            raise ValueError("Query cannot be empty.")

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
Page: {result.page}
Chunk ID: {result.chunk_id}
Similarity Score: {result.score:.4f}

Content:
{result.document.page_content}
""".strip()
            )

        formatted_evidence = "\n\n".join(
            evidence_blocks
        )

        return f"""
You are a knowledge intelligence assistant.

Answer the user's question using ONLY the evidence provided below.

GROUNDING RULES:
1. Do not use outside knowledge.
2. Do not invent or assume information.
3. If the evidence does not contain enough information to answer the question, clearly say that the available documents do not contain enough information.
4. Preserve important numbers, dates, limits, requirements, and conditions exactly as supported by the evidence.
5. When the evidence contains conflicting versions, prefer the evidence marked as active.
6. Give a concise answer directly addressing the user's question.

USER QUESTION:
{query}

RETRIEVED EVIDENCE:
{formatted_evidence}

ANSWER:
""".strip()