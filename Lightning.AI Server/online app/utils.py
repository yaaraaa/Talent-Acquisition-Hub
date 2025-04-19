# function for retrieved documents post processing
def format_docs(docs):
    formatted_docs = []
    for doc in docs:
        candidate_name = doc.metadata.get('name', 'Unknown Candidate')
        # Include candidate's name and ID in the content
        formatted_doc = f"Candidate Name: {candidate_name}\n{doc.page_content}"
        formatted_docs.append(formatted_doc)
    return "\n\n".join(formatted_docs)
