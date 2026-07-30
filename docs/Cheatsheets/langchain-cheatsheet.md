---
layout: default
title: "LangChain Cheatsheet"
---

# LangChain Cheatsheet

A production-ready master reference for **LangChain**, the modular framework for building applications powered by Large Language Models (LLMs).

---

## 1. LLMs vs. Chat Models

LangChain differentiates between raw completion models (string-in, string-out) and modern instruction-tuned Chat Models (structured message arrays).

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# Initialize Chat Model
chat = ChatOpenAI(
    model="gpt-4o",
    temperature=0.3,
    max_tokens=500
)

# Call with explicit message arrays
messages = [
    SystemMessage(content="You are a helpful automation script engineer."),
    HumanMessage(content="Explain relative links in Markdown.")
]

response = chat.invoke(messages)
print("AI Response:", response.content)
```

---

## 2. Prompt Templates

PromptTemplates help translate raw user configurations into beautifully formatted model inputs.

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 1. Standard template structure
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a professional translator. Translate all user inputs to {language}."),
    ("human", "My text: {text}")
])

# Format the message array
messages = prompt.format_messages(language="Spanish", text="I love building automated test vaults.")

# 2. Template with history placeholder
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly AI companion."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])
```

---

## 3. LangChain Expression Language (LCEL)

LCEL is a declarative language to easily chain components together using the pipe operator (`|`). It natively supports streaming, async calls, and parallel batch operations.

```python
from langchain_core.output_parsers import StrOutputParser

# Define standard sequence: prompt -> chat model -> string parser
chain = prompt | chat | StrOutputParser()

# Invoke the synchronous pipeline
result = chain.invoke({"language": "German", "text": "Hello, world!"})
print("Result:", result)

# Stream the output chunks in real-time
for chunk in chain.stream({"language": "French", "text": "Stream this content!"}):
    print(chunk, end="", flush=True)
```

---

## 4. Retrieval Augmented Generation (RAG)

Standard pipelines to load local text directories, chunk documents, compute vectors, and fetch semantic matches.

```python
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# 1. Ingest raw files
loader = DirectoryLoader("./my_docs", glob="*.md", loader_cls=TextLoader)
documents = loader.load()

# 2. Chunk documents into logical split sizes
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
    separators=["\n\n", "\n", " ", ""]
)
chunks = splitter.split_documents(documents)

# 3. Create Vector Index & Store Embedding Matrix
embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(chunks, embeddings)

# 4. Use Vector DB as semantic Retriver
retriever = db.as_retriever(search_kwargs={"k": 3})
retrieved_docs = retriever.invoke("How does local vault sorting work?")
```

---

## 5. Structured Outputs

Enforce LLM outputs to adhere to exact JSON schemas using Pydantic validation structures.

```python
from pydantic import BaseModel, Field
from typing import List

class ExtractionSchema(BaseModel):
    summary: str = Field(description="A concise summary of the article input")
    keywords: List[str] = Field(description="List of core keywords mentioned")
    sentiment: str = Field(description="Is the overall article sentiment positive, negative, or neutral?")

# Configure model to strictly return the structured output scheme
structured_llm = chat.with_structured_output(ExtractionSchema)

result = structured_llm.invoke("Today I resolved multiple long-running automation test suites in python.")
print("Parsed JSON Structure:", result.model_dump_json(indent=2))
```
