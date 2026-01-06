def build_rag_prompt(query: str, documents: list[dict]) -> str:
    context = "\n\n".join(
        f"- {doc['title']}: {doc['content']}"
        for doc in documents
    )

    return f"""
You are an AI assistant answering questions using only the context below.
If the answer is not present, say you don't know.

Context:
{context}

Question:
{query}

Answer:
""".strip()
