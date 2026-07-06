from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from config import Config

class RAGEngine:
    def __init__(self):
        self.embeddings = MistralAIEmbeddings(
            model=Config.EMBEDDING_MODEL,
            api_key=Config.MISTRAL_API_KEY
        )
        self.vectorstore = Chroma(
            persist_directory=Config.DB_DIR,
            embedding_function=self.embeddings
        )
        self.retriever = self.vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": Config.RETRIEVER_K,
                "fetch_k": Config.RETRIEVER_FETCH_K,
                "lambda_mult": Config.RETRIEVER_LAMBDA
            }
        )
        self.llm = ChatMistralAI(
            model=Config.LLM_MODEL,
            api_key=Config.MISTRAL_API_KEY
        )
        self.prompt_template = ChatPromptTemplate.from_messages([
            (
                "system",
                """You are a helpful AI assistant.
Only use the information provided in the context to answer the question.

If the answer is not in the context, respond with:
"I don't know based on the given context."
Do not invent or assume information."""
            ),
            (
                "human",
                """Context:
{context}

Question:
{question}"""
            )
        ])

    def ask(self, question: str) -> dict:
        docs = self.retriever.invoke(question)
        context = "\n\n".join([doc.page_content for doc in docs])
        messages = self.prompt_template.format_messages(
            context=context,
            question=question
        )
        result = self.llm.invoke(messages)
        return {
            "answer": result.content if hasattr(result, "content") else str(result),
            "sources": [
                {
                    "content": doc.page_content[:300] + "...",
                    "metadata": doc.metadata
                }
                for doc in docs
            ]
        }

    def get_vectorstore(self):
        return self.vectorstore

    def get_embedding_function(self):
        return self.embeddings