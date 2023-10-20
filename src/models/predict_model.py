from summarizer import TransformerSummarizer
import streamlit as st

st.title("Summarize")
text_input = st.text_area("Enter text to summarize:")

if st.button("Run"):
    if text_input:
        with st.spinner("Summarizing..."):
            model = TransformerSummarizer(transformer_type="XLNet", transformer_model_key="xlnet-base-cased")
            summary = ''.join(model(text_input, min_length=100, max_length=16384))

        st.subheader("Summary:")
        st.write(summary)
    else:
        st.warning("Please enter some text to summarize.")
