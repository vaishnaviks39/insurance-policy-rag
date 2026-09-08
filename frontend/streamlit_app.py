import streamlit as st
import requests

BACKEND_URL = "http://backend:8000"

st.set_page_config(page_title="Insurance Policy RAG")
st.title("Insurance Policy RAG")
st.caption("Upload a policy PDF, then ask questions about it.")

if "doc_id" not in st.session_state:
    st.session_state.doc_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

uploaded_file = st.file_uploader("Upload a policy PDF", type=["pdf"], key=st.session_state.uploader_key)

if uploaded_file is not None and st.session_state.doc_id is None:
    with st.spinner("Extracting, chunking, and indexing..."):
        try:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            resp = requests.post(f"{BACKEND_URL}/upload", files=files, timeout=120)
            resp.raise_for_status()
            data = resp.json()
            st.session_state.doc_id = data["doc_id"]
            st.success(f"Indexed {data['num_chunks']} chunks from {uploaded_file.name}")
            st.rerun()
        except requests.exceptions.RequestException as e:
            st.error(f"Upload failed: {e}")

if st.session_state.doc_id:
    if st.button("Upload a different document"):
        st.session_state.doc_id = None
        st.session_state.messages = []
        st.session_state.uploader_key += 1
        st.rerun()

    st.divider()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if msg.get("sources"):
                with st.expander("Sources"):
                    for src in msg["sources"]:
                        st.write(f"**Page {src['page']}:** {src['text']}...")

    question = st.chat_input("Ask a question about this policy")

    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            with st.spinner("Searching and generating..."):
                try:
                    resp = requests.post(
                        f"{BACKEND_URL}/chat",
                        params={"doc_id": st.session_state.doc_id, "question": question},
                        timeout=120,
                    )
                    resp.raise_for_status()
                    data = resp.json()

                    if "error" in data:
                        st.error(data["error"])
                    else:
                        st.write(data["answer"])
                        if data.get("sources"):
                            with st.expander("Sources"):
                                for src in data["sources"]:
                                    st.write(f"**Page {src['page']}:** {src['text']}...")
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": data["answer"],
                            "sources": data.get("sources", []),
                        })
                except requests.exceptions.RequestException as e:
                    st.error(f"Request failed: {e}")
else:
    st.info("Upload a PDF above to get started.")