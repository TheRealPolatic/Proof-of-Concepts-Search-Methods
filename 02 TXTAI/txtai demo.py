import os

import streamlit as st

from txtai.embeddings import Embeddings


class Application:
    """
    Main application.
    """

    def __init__(self):
        """
        Creates a new application.
        """

        # Create embeddings model, backed by sentence-transformers & transformers
        self.embeddings = Embeddings({"path": "sentence-transformers/nli-mpnet-base-v2"})

    def run(self):
        """
        Runs a Streamlit application.
        """

        st.title("Similarity Search POC")
        st.markdown("Proof of Concept voor het similarity search onderzoek - Dayo Toirkens")

        data = [
            "US tops 5 million confirmed virus cases",
            "Canada's last fully intact ice shelf has suddenly collapsed, forming a Manhattan-sized iceberg",
            "Beijing mobilises invasion craft along coast as Taiwan tensions escalate",
            "The National Park Service warns against sacrificing slower friends in a bear attack",
            "Maine man wins $1M from $25 lottery ticket",
            "Make huge profits without work, earn up to $100,000 a day",
        ]

        data = st.text_area("Data", value="\n".join(data))
        query = st.text_input("Query")

        data = data.split("\n")

        if query:
            # Get index of best section that best matches query
            similarity = self.embeddings.similarity(query, data)
            uid = similarity[0][0]
            print(self.embeddings.similarity(query, data))
            st.write(data[uid])
            st.write("Similarity: " + str(similarity[0][1]))


@st.cache(allow_output_mutation=True)
def create():
    """
    Creates and caches a Streamlit application.
    Returns:
        Application
    """

    return Application()


if __name__ == "__main__":
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    # Create and run application
    app = create()
    app.run()