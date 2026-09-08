from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_pages(
    page_documents: list[dict],
    chunk_size: int = 200,
    overlap: int = 50
) -> list[dict]:

    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base",
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = []

    for doc in page_documents:

        pieces = splitter.split_text(doc["text"])

        for piece in pieces:
            chunks.append({
                "text": piece,
                "meta": {
                    "page": doc["page"]
                }
            })

    return chunks