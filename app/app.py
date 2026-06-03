import streamlit as st
from rag import (
    retrieve,
    build_context,
    generate_answer
)


st.set_page_config(
    page_title="Quant Research Intelligence System",
    layout="wide"
)

st.title("📈 Quant Research Intelligence System")

query = st.text_input(
    "Ask a Quant Finance Research Question"
)

if st.button("Search"):

    if query.strip() == "":
        st.warning("Please enter a question.")
    else:

        st.subheader("Question")
        st.write(query)

        # Retrieve relevant papers/chunks
        results = retrieve(
            query,
            top_k=5
        )

        # Build context
        context = build_context(results)

        # Generate answer
        answer = generate_answer(
            query,
            context
        )

        # Display answer
        st.subheader("Answer")
        st.write(answer)

        # Display sources
        st.subheader("Sources")

        seen = set()

        for result in results:

            title = result["chunk"]["paper_title"]

            if title not in seen:
                seen.add(title)
                st.write(f"• {title}")