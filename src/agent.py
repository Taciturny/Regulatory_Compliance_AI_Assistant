import os
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
import cohere
import gradio as gr
import re


# Initializing Cohere API
co = cohere.ClientV2(api_key=os.environ.get("COHERE_API_KEY"))

# Original prompt template
prompt_template = """
You are an expert legal assistant specializing in data protection laws and privacy regulations. 
Given the context of data protection laws and regulations, answer the user's question as clearly and accurately as possible.
With focus on the Nigerian Data Protection Act (NDPA)

Also if the user pastes a section of the NDPA, provide a summary of the section and its relevance to the user's question.

Also if user pastes privacy policy, provide a summary of the privacy policy and its relevance to the user's question and identify points that violate the user rights according to NDPA.

Context:
{context}

When answering, follow these steps:
    1. Identify the core issue in the user's question.
    2. Use the provided context to find the most relevant legal guidelines.
    3. Provide a well-structured, easy-to-understand response.
    4. If the query requires clarification or is beyond the given context, politely guide the user towards additional resources.

Check this Examples and use as a Guide in responding
Examples:
    Question:
    Does the NDPA require organizations to notify individuals when collecting their personal data?
    Answer:
    Yes, the NDPA requires organizations to provide individuals with clear notice before collecting their personal data. This includes informing them about the purpose of data collection, their rights, and how the data will be processed and stored. Transparency is a key principle under the NDPA.
    
    Question:
    Here’s a section of the NDPA: “Every data controller shall take appropriate technical and organizational measures to ensure the security and confidentiality of personal data.”
    What does this mean in practice?
    Answer:
    This section emphasizes the responsibility of data controllers to implement safeguards—both technical (like encryption) and organizational (like access control policies)—to protect personal data from unauthorized access, loss, or misuse. It reinforces the NDPA's commitment to privacy and security by design.

Question:
{query}

Answer:
"""

# New prompt template for low score cases
low_score_prompt_template = """
You are a legal assistant specializing in data protection laws and regulations, particularly focusing on the Nigerian Data Protection Act (NDPA).
The user has asked a general or non-specific question, and the context available is not sufficient to retrieve relevant legal information.

Please respond to the user's inquiry in a helpful, polite, and general manner. You should focus on the NDPA and provide a short introduction about the role of data protection laws. If necessary, guide the user towards asking a more specific question.
If the user is being appreciative or greeting, respond in a friendly manner. as brief as possible with small reference to the user chat history

If its entirely new question, respond in a friendly manner and provide a brief overview of the NDPA and its significance.

Caution: 
Be very brief and avoid unnecessary details.
Avoid using the context provided in the conversation history to answer the question.
Avoid unnecessary jargon or complex language.
Just provide a simple and clear response.
Go straight to the point and avoid lengthy explanations.


Check this Examples and use as a Guide in responding
Examples:
    Question:
    Hi, I hope you're doing well! Just wanted to say thanks for the help earlier.
    Answer:
    You're very welcome! I'm glad I could assist. If you have any questions about data protection or the NDPA, feel free to ask.
    Question:
    Can you explain what data protection is?
    Answer:Sure! Data protection refers to laws and practices that safeguard people's personal information from misuse. In Nigeria, the NDPA helps ensure that individuals have control over how their data is collected, used, and shared.

The history is to provide you with knowledge of the user and the context of the conversation, don't use it to answer the question.

Conversation History:
{history}

User Query:
{query}

Answer:
"""

def retrival(query, index_name="regulatoryai", model_name="all-MiniLM-L6-v2"):
    api_key = os.environ.get("PINECONE_API_KEY")
    pc = Pinecone(api_key=api_key)
    cloud = os.environ.get('PINECONE_CLOUD') or 'aws'
    region = os.environ.get('PINECONE_REGION') or 'us-east-1'

    spec = ServerlessSpec(cloud=cloud, region=region)
    model = SentenceTransformer(model_name)
    index = pc.Index(index_name)

    query_vector = model.encode(query).tolist()
    query_result = index.query(vector=query_vector, top_k=3, include_metadata=True)
    return query_result


def extract_pairs(history):
    pairs = []
    i = 0
    while i < len(history) - 1:
        if history[i]["role"] == "user" and history[i+1]["role"] == "assistant":
            pairs.append((history[i]["content"], history[i+1]["content"]))
            i += 2
        else:
            i += 1
    return pairs


def is_greeting_or_thanks(text):
    greetings = [
        r"\bhi\b", r"\bhello\b", r"\bhey\b", r"\bgood (morning|afternoon|evening)\b",
        r"\bthank(s| you)\b", r"\bappreciate\b", r"\bmany thanks\b"
    ]
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in greetings)


def chatbot_with_context(message, history = []):
    history = extract_pairs(history)

    full_conversation = ""
    for user_msg, assistant_msg in history:
        full_conversation += f"User: {user_msg}\nAssistant: {assistant_msg}\n"
    full_conversation += f"User: {message}"

    thought = "🔍 Retrieving relevant sections from the NDPA and related documents..."
    yield thought
    retrieved = retrival(message)

    # Check retrieval confidence
    low_score = all(match['score'] < 0.4 for match in retrieved['matches'])

    if low_score:
        prompt = low_score_prompt_template.format(
            history=full_conversation,
            query=message
        )

        # LLM responds on its own with the new prompt
        thinking = "🤔 Thinking through the legal implications..."
        yield thinking

        response = co.chat(
            model="command-r-plus-08-2024",
            messages=[{"role": "user", "content": prompt}],
        )

        final_response = response.message.content[0].text
        yield final_response
        return

    # Extract context from results
    context_texts = [
        f"Section: {match['metadata'].get('Section', 'Unknown')}\n{match['metadata'].get('Content', '[No content found]')}"
        for match in retrieved['matches']
    ]
    context_combined = "\n\n".join(context_texts)

    # Construct prompt
    prompt = prompt_template.format(context=context_combined, query=full_conversation)

    thinking = "🤔 Thinking through the legal implications..."
    yield thinking

    response = co.chat(
        model="command-r-plus-08-2024",
        messages=[{"role": "user", "content": prompt}],
    )

    final_response = response.message.content[0].text
    yield final_response


app = gr.ChatInterface(
    fn=chatbot_with_context,
    type="messages",
    title="📜 NDPA Legal Assistant",
    description="""
    ### 👩‍⚖️ Ask a Legal Expert About the **Nigerian Data Protection Act (NDPA)**
    Paste a question, a section of the NDPA, or a privacy policy, and let this assistant help you understand:
    - What it means
    - What rights it impacts
    - Whether it complies with NDPA or violates your rights
    """,
    examples=[
        "What does the NDPA say about data subject consent?",
        "Here’s Section 37 of the Constitution, how does it relate to NDPA?",
        "I found this clause in a privacy policy, is it lawful under NDPA?",
    ],
    theme="soft",
    chatbot=gr.Chatbot(
        bubble_full_width=False,
        show_copy_button=True,
        show_label=False,
        avatar_images=("🧑🏾‍💼", "👨🏾‍⚖️"),
    ),
    css=".gradio-container { font-family: 'Segoe UI', sans-serif; font-size: 15px; }",
    save_history=True,
    flagging_mode="manual",
    flagging_options=["Helpful ✅", "Not Accurate ❌", "Biased 🚫", "Other 📝"]
)

app.launch(share=True, pwa=True)
