from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain_core.prompts import PromptTemplate
from qdrant_client import QdrantClient, models

load_dotenv()

# Set openai chat model and embedding model
openai_chat_model = ChatOpenAI(model="gpt-4o")
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")


# VectorStore

# qdrant_client = QdrantClient(
#     url=
#     api_key=
# )
# qdrant_client.create_collection(
#     collection_name="one-on-ones",
#     vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
# )

# vectorstore = Qdrant(
#     qdrant_client, collection_name="one-on-ones", embeddings=embedding_model
# )

# qdrant_retriever = vectorstore.as_retriever()

RAG_PROMPT_TEMPLATE = """\
<|start_header_id|>system<|end_header_id|>
Generate a sample meeting agenda for a 1:1 between a software engineer and their engineering manager. 

Based on the user input, the agenda should contain one, a few, or all of the following sections:
- Personal updates
- Accomplishments
- Blockers
- Risk to company goals

Add a section for follow up questions that the engineering manager could ask to better faciliate their 1:1 time
.<|eot_id|>

<|start_header_id|>user<|end_header_id|>
User Query:
{query}

Context:
{context}<|eot_id|>

<|start_header_id|>assistant<|end_header_id|>
"""

CONTEXT = """
Current tasks: I am working on an LLM Project called one-on-one. I have a few meetings this week for this project: I had a kickoff meeting to discuss the initial project with my project partner. Then we had another meeting with Greg to get feedback on the initial project idea. After getting Greg's feedback, we had a follow up meeting to finalize the project idea. Some of the tasks for this week were: writing up a PRD (project requirements doc), coming up with an overall TDD (technical design dic), and then getting started on implementing.
Goals for the week: By the end of this week I'd like to have the frontend and backend wired up for the agenda creation part of our project. That way it could set us up well for the next week to start implementing the LLM part of the project.
Blockers: Not too many unknowns.
Personal Update: I'm doing STP or Seattle to Portland, a two day bicycle ride from Seattle to Portland this weekend
"""

rag_prompt = PromptTemplate.from_template(RAG_PROMPT_TEMPLATE)


def invoke_rag_chain(query: str):
    chat_chain = rag_prompt | openai_chat_model
    response = chat_chain.invoke(
        {
            "query": query,
            "context": CONTEXT,
        }
    )

    print(response.content)

    return response.content
