# Interview

Checkbox: No
Total Tags: 0

Here are some strong, realistic **interview questions and sample answers** tailored to the two job descriptions you shared (AI Engineer focused on GCP/Vertex AI/GenAI + GenAI Engineer with NLP/RAG emphasis). These cover must-have skills like Python, TensorFlow/PyTorch, NLP/ML, GCP services (Vertex AI, BigQuery, etc.), Generative AI (Gemini), prompt engineering, embeddings/vector stores, RAG, Flask/FastAPI endpoints, and Transformer models (e.g., BERT).

I've grouped them into categories for easier preparation. Answers are concise, professional, and demonstrate practical experience.

### Python & Deep Learning Frameworks

**Q1: How do you choose between TensorFlow, PyTorch, and JAX for a project? Give an example from your experience.**

**Sample Answer:**
I choose based on project needs. PyTorch is my go-to for research and rapid prototyping because of its dynamic computation graph and ease of debugging (e.g., I built a custom RAG pipeline with PyTorch for experimenting with different embedding models). TensorFlow shines in production, especially on GCP — I’ve used it with Vertex AI for scalable training and deployment of Gemini-based models, leveraging tf.data for efficient pipelines and TensorFlow Serving/Vertex AI endpoints. JAX is great for high-performance numerical computing and custom gradients (e.g., when I needed fast custom loss functions in a research PoC). In most enterprise GenAI work on GCP, I lean toward TensorFlow + Vertex AI for MLOps integration.

**Q2: Explain how you would implement a simple neural network for text classification using PyTorch or TensorFlow.**

**Sample Answer:**
In PyTorch:

- Load data → tokenize (e.g., with Hugging Face tokenizer) → create Dataset/DataLoader.
- Define model: Embedding → LSTM/Transformer encoder → Linear layer + softmax.
- Use nn.CrossEntropyLoss + Adam optimizer.
- Train loop with torch.autograd.

I prefer PyTorch for flexibility. In TensorFlow/Keras it's more declarative: Sequential model with Embedding, Bidirectional LSTM, Dense. I’ve deployed both to Vertex AI.

### NLP, ML & Transformers

**Q3: What is a Transformer model, and how does BERT work? Why is it useful in NLP?**

**Sample Answer:**
Transformers use self-attention to process sequences in parallel, unlike RNNs. BERT (Bidirectional Encoder Representations from Transformers) is pre-trained with masked language modeling (15% tokens masked, predict them) and next sentence prediction, making it bidirectional. This captures deep context. I’ve fine-tuned BERT variants (e.g., bert-base-uncased) on Vertex AI for classification/similarity tasks, achieving 5-10% better F1 than LSTM baselines.

**Q4: Explain RAG (Retrieval-Augmented Generation). When would you use it instead of fine-tuning?**

**Sample Answer:**
RAG combines retrieval (e.g., from vector store) with generation: retrieve relevant documents via embeddings → augment prompt → generate with LLM (e.g., Gemini). It reduces hallucinations and handles up-to-date/external knowledge without retraining. I use RAG for enterprise search/chatbots (dynamic data) and fine-tuning for domain-specific style/behavior when data is static and labeled. On GCP, I implement RAG with Vertex AI Vector Search + Gemini API.

### GCP & Vertex AI Specific

**Q5: Describe how you would build and deploy a Generative AI application using Vertex AI and Gemini.**

**Sample Answer:**

1. Use Vertex AI Studio to prototype prompts with Gemini 1.5/2.0 Flash/Pro.
2. Generate embeddings (textembedding-gecko or Gemini embedding API).
3. Store in Vertex AI Vector Search or Matching Engine for retrieval.
4. Implement RAG: retrieve chunks → ground prompt → call Gemini generateContent.
5. Deploy as endpoint: Use Vertex AI endpoints or FastAPI/Flask on Cloud Run, triggered via Cloud Functions + Pub/Sub for async.
6. Monitor with Vertex AI Monitoring + BigQuery for logs/metrics.
I’ve delivered similar solutions for internal Q&A bots, reducing latency and cost vs. pure fine-tuning.

**Q6: How do you use BigQuery, Pub/Sub, and Cloud Functions in an AI pipeline on GCP?**

**Sample Answer:**
BigQuery stores structured data (e.g., user queries, metadata) and runs SQL for analytics. Pub/Sub handles event-driven messaging (e.g., new document uploaded → trigger embedding). Cloud Functions for lightweight serverless logic (e.g., preprocess text → call embedding API). Example: Pub/Sub topic receives file upload event → Cloud Function chunks text → generates embeddings → upserts to Vertex AI Vector Search → results logged to BigQuery.

### Prompt Design, Embeddings & Vector Stores

**Q7: What is prompt engineering? Give examples of techniques you’ve used to improve Gemini outputs.**

**Sample Answer:**
Prompt engineering crafts inputs to guide LLMs effectively. Techniques I use:

- Chain-of-Thought (“Think step by step”) for reasoning.
- Few-shot examples for consistency.
- Role-playing (“You are an expert analyst”).
- Structured output (JSON mode in Gemini).
- Grounding with context to reduce hallucinations.
In one project, adding CoT + examples improved accuracy from 72% to 89% on a complex Q&A task.

**Q8: How do embeddings and vector stores work in GenAI applications? Name tools you’ve used.**

**Sample Answer:**
Embeddings convert text to dense vectors capturing semantics (e.g., cosine similarity measures closeness). Vector stores (like Vertex AI Vector Search, Pinecone, FAISS) enable fast approximate nearest-neighbor search. I’ve used Gemini/textembedding-gecko for embeddings, stored in Vertex AI Matching Engine/Vector Search for RAG apps — hybrid search (keyword + vector) often gives best recall.

### Deployment & Practical Experience

**Q9: How would you build and expose an AI endpoint using Flask or FastAPI?**

**Sample Answer:**
I prefer FastAPI for async support and auto OpenAPI docs. Example:

- Load model (e.g., via Vertex AI SDK or local PyTorch).
- Create /predict endpoint accepting JSON (prompt/text).
- Process → call model → return structured response.
- Add auth (API keys), rate limiting, logging.
- Deploy to Cloud Run for scalability, or Vertex AI for managed serving.
I’ve built FastAPI services calling Gemini for real-time inference, integrated with Pub/Sub for batch jobs.

**Q10: Describe a challenging GenAI project you delivered and what you learned.**

**Sample Answer:**
(Behavioral) I built a RAG-based internal knowledge base using Vertex AI + Gemini. Challenge: high latency on large docs. Solution: chunking strategy + hybrid search + caching frequent queries in Memorystore. Reduced response time 60% and hallucinations via grounding. Learned importance of eval metrics (e.g., faithfulness, answer relevance) and iterative prompt tuning.

### Advanced Gemini & Vertex AI (2026 Context)

**Q11: What are the key differences between Gemini 2.5 and Gemini 3 series models on Vertex AI as of early 2026? When would you choose one over the other?**

**Sample Answer:**
As of January 2026, Gemini 3 Flash and 3 Pro (preview/GA) represent Google's frontier models, outperforming 2.5 series in reasoning (e.g., topping LM Arena with 1501 Elo for 3 Pro), multimodal understanding (text+image+audio+video), agentic capabilities (tool use, function calling, Computer Use tool launched Jan 2026), and speed/efficiency. Gemini 3 Flash emphasizes low-latency, cost-effective tasks (everyday reasoning, fast completion), while 3 Pro handles complex, multi-step reasoning and deep thinking modes.
I choose Gemini 3 Flash for production chatbots or real-time apps on Vertex AI to minimize cost/latency. I use 3 Pro for enterprise-grade agents, code generation, or heavy multimodal tasks (e.g., document analysis with images/audio). Both support grounding with Vertex AI Search/Vector Search for RAG. In a recent project, switching to Gemini 3 Flash cut inference cost 40% while maintaining quality on a customer support bot.

**Q12: How do you implement agentic workflows using Vertex AI Agent Builder or Gemini tools in 2026?**

**Sample Answer:**
Vertex AI Agent Builder (GA by 2026) lets me create agents with LLM (Gemini 3 Pro/Flash), tools (custom functions, APIs, grounding), memory (short-term context + long-term via Vector Search/BigQuery), and orchestration (ReAct-style reasoning loop).
Steps:

1. Define agent goal and instructions in Agent Builder UI/SDK.
2. Add tools (e.g., BigQuery query tool, Pub/Sub publish, custom FastAPI endpoints).
3. Enable grounding with enterprise data via Vertex AI Search.
4. Use long-term memory (embed past interactions → retrieve for context).
5. Deploy as endpoint or integrate with Cloud Run/Functions.
Example: Built a procurement agent that reasons over policies (RAG), queries inventory via BigQuery tool, and places orders via API — reduced manual steps 70%. Gemini 3's Computer Use tool (preview Jan 2026) adds browser/screen interaction for more autonomous agents.

### Advanced RAG & Retrieval Techniques

**Q13: What are common failure modes in naïve RAG, and how do you address them with advanced techniques?**

**Sample Answer:**
Naïve RAG failures:

- Poor retrieval (irrelevant chunks due to bad embeddings/chunking).
- Lost context (chunk misses key info).
- Hallucinations despite retrieval.
- Latency on large corpora.

Advanced fixes I use:

- **Chunking**: Semantic (LLM-based) or hierarchical (small chunks + summaries) instead of fixed-size.
- **Multi-query / Hypothetical Document Embeddings (HyDE)**: Generate query variations or hypothetical answers → better recall.
- **Reranking**: Retrieve top-50 → rerank with cross-encoder or Gemini reranker API.
- **Hybrid search**: Combine BM25 keyword + vector similarity (Vertex AI Vector Search supports this natively).
- **Query transformation / routing**: Classify query type → route to different indexes (e.g., structured vs unstructured).
- **Self-query / metadata filtering**: Add filters (date, source) to retrieval.
In one enterprise search app, adding HyDE + reranking boosted NDCG@10 from 0.68 to 0.89.

**Q14: Explain Modular / Advanced RAG patterns like Corrective RAG (CRAG), Self-RAG, or Adaptive RAG. When do you apply them?**

**Sample Answer:**

- **Corrective RAG (CRAG)**: After retrieval, evaluate chunk quality (Gemini judges relevance/accuracy) → correct (web search if low quality), refine, or reject. Reduces noise/hallucinations.
- **Self-RAG**: LLM reflects on its own generation — retrieves/refines if needed mid-response (iterative self-correction).
- **Adaptive RAG**: Dynamically decides retrieval necessity (e.g., simple queries skip RAG, complex ones retrieve). Saves cost.

I apply CRAG for high-stakes domains (legal/medical) where faithfulness is critical. Self-RAG for long-form reasoning. Adaptive RAG for cost-sensitive apps (e.g., high-volume chat). On Vertex AI, I implement these via prompt chaining or custom FastAPI logic calling Gemini multiple times.

### LLMOps, Monitoring & Production

**Q15: How do you handle model drift, monitoring, and retraining in a Vertex AI GenAI pipeline?**

**Sample Answer:**
Vertex AI Model Monitoring tracks prediction drift, data skew, and feature attribution. For GenAI:

- Log inputs/outputs to BigQuery.
- Compute metrics: faithfulness (ground truth vs generation), answer relevance, retrieval recall.
- Use Vertex AI Experiments to compare prompt versions/models.
- Set alerts for drift (e.g., embedding distribution shift via TensorFlow Data Validation).
- Retraining: Fine-tune Gemini on new labeled data (Vertex AI tuning) or refresh vector index periodically.
In production, I built dashboards in Looker Studio + BigQuery ML for hallucination rate — triggered retraining when >5% threshold breach.

**Q16: How do you optimize cost and latency for a high-traffic Gemini-based application on GCP?**

**Sample Answer:**
Strategies:

- Use Gemini 3 Flash (cheaper/faster than Pro) for most traffic.
- Caching: Cache frequent prompts/responses in Memorystore or Cloud CDN.
- Batching: Batch requests via Pub/Sub + Cloud Functions.
- Prompt compression / distillation: Shorten prompts or distill to smaller model.
- Retrieval optimization: Smaller chunks, approximate nearest neighbors, hybrid search.
- Autoscaling: Deploy on Vertex AI endpoints or Cloud Run with min instances=0.
- Quota-aware routing: Fallback to lighter model if rate-limited.
Reduced monthly cost 55% on a Q&A app by combining Flash + intelligent caching + adaptive retrieval.

### Behavioral / Project Deep-Dive

**Q17: Describe a time you debugged a production GenAI issue (e.g., hallucinations, poor retrieval, high cost). What root cause did you find and how did you fix it?**

**Sample Answer:**
(Behavioral – use STAR)
Situation: Internal RAG chatbot hallucinated policy details, frustrating users.
Task: Reduce hallucinations below 3% while keeping <2s latency.
Action: Analyzed logs in BigQuery → found retrieval missed nuanced sections due to poor chunk overlap. Switched to parent-document retriever (small chunks for embedding + larger context chunks). Added CRAG step (Gemini scores retrieved chunks → web fallback if low). Tuned prompt with strict grounding instructions.
Result: Hallucinations dropped to 1.2%, latency stable, user satisfaction up 35% per NPS.

**Q18: How would you design a scalable GenAI endpoint for 10k+ QPS using FastAPI/Flask on GCP?**

**Sample Answer:**
Use FastAPI (async, type-safe) on Cloud Run (auto-scales to zero).

- Load balancer → API Gateway for auth/rate limiting.
- Async calls to Vertex AI Gemini API (batching via SDK).
- Redis/Memorystore for caching + rate limiting.
- Pub/Sub for async heavy tasks (e.g., long generations).
- Monitoring: Cloud Monitoring + Vertex AI metrics.
- CI/CD: Cloud Build + Artifact Registry.
For 10k+ QPS: Horizontal scaling + sharding vector indexes if RAG-heavy. I've deployed similar for enterprise search handling peak loads.

Here are **additional interview questions and sample answers** focused on **LangChain**, **LangGraph**, **LLMs**, **RAG**, **vector stores**, models, agents, and related concepts. These reflect production realities as of January 2026 (e.g., LangGraph as the go-to for stateful agents, LangChain v1+ stable with LCEL patterns, advanced RAG patterns like CRAG/Adaptive via LangGraph, agentic workflows, evaluation with Ragas/LangSmith, and hybrid setups).

I've grouped them into categories. Answers are practical, code-aware where relevant, and emphasize trade-offs, debugging, and production best practices.

### LangChain Fundamentals & LCEL

**Q1: What is LangChain, and how has its architecture evolved by 2026? Compare LCEL vs legacy chains.**

**Sample Answer:**
LangChain is an open-source framework for building LLM-powered applications by composing modular components: prompts, models, retrievers, tools, memory, and chains/agents. By 2026, legacy sequential chains (e.g., LLMChain) are deprecated in favor of **LangChain Expression Language (LCEL)** — a declarative, composable syntax using the pipe operator () for chaining runnables. LCEL is more debuggable, supports streaming, parallelism (RunnableParallel), fallbacks, and config injection.
Example LCEL RAG chain:

Python

`retriever = vectorstore.as_retriever()
prompt = ChatPromptTemplate.from_template("Answer using context: {context}\nQuestion: {question}")
chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | llm | StrOutputParser()`

I prefer LCEL for production — it's more flexible and integrates seamlessly with LangGraph for stateful flows.

**Q2: Explain key LangChain components and when you'd use each.**

**Sample Answer:**

- **Document Loaders** → Ingest PDFs, web pages, CSVs, etc.
- **Text Splitters** → Chunk docs (RecursiveCharacter, SemanticChunker for better context).
- **Embeddings** → OpenAI, HuggingFace, Voyage, etc.
- **Vector Stores** → Chroma (local), Pinecone/Weaviate (cloud), FAISS (fast in-memory).
- **Retrievers** → VectorStoreRetriever, MultiQueryRetriever, ContextualCompressionRetriever.
- **LLMs/Chat Models** → Unified API for OpenAI, Anthropic, Gemini, local via Ollama.
- **Prompt Templates** → Few-shot, structured output (with tools).
- **Output Parsers** → JsonOutputParser, Pydantic for reliable structured responses.
- **Memory** → ConversationBuffer, Summary, Entity memory.
Use vector stores for RAG, retrievers for advanced search, and memory for chatbots.

### RAG Implementation in LangChain

**Q3: Walk through a production-ready RAG pipeline in LangChain. What optimizations do you apply?**

**Sample Answer:**
Standard flow:

1. Load → split documents (e.g., RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)).
2. Embed with strong model (text-embedding-3-large or voyage-3).
3. Index in vector store (e.g., Chroma with HNSW or Pinecone serverless).
4. Retrieve: Use hybrid (dense + BM25 via EnsembleRetriever) or rerank (Cohere Rerank / flashrank).
5. Augment prompt with context (limit tokens via compression or top-k).
6. Generate with grounding instructions ("Use only provided context").
7. Parse + evaluate (Ragas for faithfulness, answer relevance).

Optimizations: Parent-document retriever (small chunks embed, large return context), HyDE (hypothetical answers for query), multi-query decomposition, caching (Redis), async retrieval. In production, I add LangSmith tracing and human-in-the-loop fallbacks.

**Q4: What are common RAG failure modes in LangChain apps, and how do you fix them?**

**Sample Answer:**

- Irrelevant retrieval → Fix: Better embeddings, hybrid search, metadata filtering, query transformation.
- Lost context in chunks → Parent-document or hierarchical indexing.
- Hallucinations → Grounding prompts, CRAG (Corrective RAG via LangGraph: retrieve → score relevance → correct/reject/web fallback).
- Noisy context → Contextual compression (LLM reranker), MMR diversity.
- Cost/latency → Adaptive RAG (route simple queries to no-retrieval), caching, smaller models (Gemini Flash).
I use LangGraph to implement CRAG/Adaptive as a stateful graph with conditional edges.

### LangGraph & Agents

**Q5: What is LangGraph, and why is it preferred over plain LangChain chains for agents in 2026?**

**Sample Answer:**
LangGraph is a graph-based orchestration library (built on LangChain) for stateful, controllable agent workflows. Unlike linear chains, it models agents as graphs: nodes (actions/tools/LLM calls), edges (conditional routing), persistent state (checkpointer for resuming).
Key advantages in 2026: Durable execution (persistence via Postgres/Redis), human-in-the-loop (interrupt_before/after), time-travel debugging, multi-agent supervision, cycles/loops for ReAct-style reasoning.
LangGraph is now the recommended path for production agents (LangChain blog/State of Agent Engineering 2026). Example: Research agent with planner → retriever → critic → generator nodes.

**Q6: How do you build a stateful ReAct agent in LangGraph? Include key concepts like checkpointer and persistence.**

**Sample Answer:**
Use StateGraph with TypedDict state (messages, intermediate steps).

- Add nodes: agent (LLM + tool binding), tools node.
- Conditional edge: route based on tool calls vs final answer.
- Compile with checkpointer (MemorySaver for dev, PostgresSaver for prod).

Python

`from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import StateGraph

workflow = StateGraph(state_schema=AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)
workflow.add_conditional_edges("agent", should_continue)
graph = workflow.compile(checkpointer=PostgresSaver(...))`

Persistence allows resuming after crashes; human approval via interrupt; memory for multi-turn.

### Vector Stores, Models & Advanced Patterns

**Q7: Compare vector stores you've used in LangChain (e.g., Chroma vs Pinecone vs Weaviate). When to choose which?**

**Sample Answer:**

- **Chroma** — Local/dev, easy, in-memory or persistent disk, great for PoCs.
- **Pinecone serverless** — Scalable, hybrid sparse-dense, podless in 2026, cost-effective at scale.
- **Weaviate** — GraphQL API, modular (BM25 + vector), auto-schema, great metadata filtering.
- **FAISS** — Fastest local approximate search, but manual scaling.
Choose Pinecone/Weaviate for prod (high QPS, filtering); Chroma for quick iteration. In LangChain: vectorstore = Pinecone.from_documents(docs, embedding, index_name=...).

**Q8: How do you evaluate and debug RAG/agent systems in LangChain/LangGraph?**

**Sample Answer:**

- **Metrics**: Ragas (faithfulness, answer relevancy, context precision/recall), DeepEval, custom LLM-as-judge.
- **Tracing**: LangSmith (traces every step, A/B test prompts, datasets for offline eval).
- **Debugging**: LangGraph Studio (visualize graph, time-travel to past states), interrupt for inspection.
- **Production**: Monitor drift in embeddings, hallucination rate via LangSmith + BigQuery dashboards. Trigger retraining/index refresh on thresholds.

**Q9: LangChain vs LlamaIndex in 2026 — when to use each or both?**

**Sample Answer:**
LangChain excels at orchestration: chains, agents, tools, memory, multi-step logic (especially with LangGraph for stateful agents).
LlamaIndex focuses on data-centric RAG: advanced indexing (knowledge graphs, document hierarchies), query engines, better out-of-box retrieval quality.
In 2026, many teams use both — LlamaIndex for ingestion/retrieval → LangChain/LangGraph for agentic workflows/tools. If pure RAG/search, LlamaIndex; if agents/tools/reasoning, LangChain+LangGraph.

**Q10: Describe a complex agentic RAG system you've built or would build using LangGraph.**

**Sample Answer:**
Multi-agent research system: Supervisor (Gemini 2.0 Pro) routes to sub-agents (Researcher → RAG tool, Critic → faithfulness check, Writer → synthesize).
State includes query, retrieved docs, critiques, drafts.
Persistence for long sessions.
Tools: web search, code execution, custom APIs.
Evaluation: Ragas per sub-task + end-to-end accuracy.
Deploy: LangGraph Platform (GA 2026) for hosted graphs, observability, scaling.

### LangGraph Advanced Patterns & Production

**Q11: What new features in LangGraph (as of January 2026) improve agent robustness and developer experience? How do they help in production?**

**Sample Answer:**
January 2026 updates (v0.4.x series + LangChain JS v1.2.13) include:

- Simplified functional API with less boilerplate and improved TypeScript inference for state schemas.
- Enhanced persistence backends (e.g., better Postgres/Redis checkpointers for durable state).
- Resumable streams on remote graphs and recovery from hallucinated tool calls.
- Dynamic tools and better streaming error signals.

These help production by enabling reliable long-running agents (e.g., resume after crashes via checkpointer), easier debugging (time-travel in LangGraph Studio), and safer tool usage (auto-recovery from bad calls). In a multi-turn research agent, I use resumable streams to handle interruptions without losing context, cutting failure rates 60%.

**Q12: Explain human-in-the-loop (HITL) in LangGraph. How do you implement approval flows or interrupts?**

**Sample Answer:**
HITL adds human oversight to agent loops for high-stakes decisions. LangGraph supports via interrupt_before/interrupt_after nodes (e.g., before tool execution or after generation).
Implementation:

- Compile graph with interrupt_before=["tools"] → pauses on tool calls.
- Use checkpointer to persist state.
- Resume via graph.update_state(thread_id, values) after human approval (e.g., via LangSmith UI or custom API).
Example: In a financial analysis agent, interrupt after draft report → human reviews/edits → resume. This ensures compliance and reduces hallucinations in regulated domains.

**Q13: How do you build a multi-agent system in LangGraph? Describe supervisor + worker pattern with subgraphs.**

**Sample Answer:**
Use hierarchical multi-agent: Supervisor node (LLM decides routing) + worker subgraphs (specialized agents).

- Define state with shared fields (e.g., messages, next_agent).
- Supervisor node: LLM + prompt to choose worker or FINISH.
- Add subgraphs (e.g., Researcher subgraph with RAG tools, Critic subgraph for review).
- Conditional edges route based on supervisor output.
- Use add_subgraph or separate StateGraph for modularity.
In 2026 projects, I built a content creation system: Supervisor → Researcher (RAG + web tools) → Writer → Editor (self-critique). Subgraphs keep code clean and reusable.

### RAG & Evaluation in 2026

**Q14: How has RAG evaluation improved in 2026 with LangChain/LangSmith tools? Name metrics and workflows.**

**Sample Answer:**
LangSmith now offers pairwise annotation queues (Dec 2025+) for A/B comparison of agent/RAG outputs, custom code evaluators, and Align Evals integration.
Key metrics:

- Ragas: faithfulness, answer relevance, context precision/recall.
- LLM-as-judge (Gemini/Claude judges).
- Custom: hallucination rate, latency, cost per query.
Workflow: Create datasets in LangSmith → run chains/graphs → trace → evaluate offline → iterate prompts/tools. For production, monitor drift via embeddings + set alerts for >10% faithfulness drop.

**Q15: Compare LangChain vs LlamaIndex in early 2026. When do you use both together?**

**Sample Answer:**
LangChain (orchestration focus): excels at chains, agents, tools, memory, LangGraph for complex/stateful flows. Strong for multi-step reasoning, tool integration, and production agents (Agent Builder GA Jan 2026).
LlamaIndex (data focus): superior indexing/retrieval — advanced query engines, document hierarchies, knowledge graphs, better default RAG accuracy/latency (e.g., 92% vs 85% retrieval in benchmarks).
In 2026: Use LlamaIndex for ingestion + retrieval → feed to LangChain/LangGraph for agentic orchestration/tools. Hybrid wins for enterprise RAG agents (e.g., LlamaIndex vector store + LangGraph supervisor routing to tools/critics).

### Agents, Tools & Edge Cases

**Q16: How do you handle tool hallucinations or invalid calls in production LangGraph agents?**

**Sample Answer:**
2026 LangGraph/JS improvements auto-recover from hallucinated calls (retry with correction prompt). Manual fixes:

- Bind tools with strict schemas (Pydantic/JSON mode).
- Add validation node: parse tool call → try/except → re-prompt if invalid.
- Use conditional edge: if tool fail → route to recovery LLM call.
- Tracing in LangSmith to spot patterns (e.g., bad JSON).
In a production travel agent, added a "tool_validator" node — reduced invalid calls from 18% to <2%.

**Q17: Describe integrating a traditional ML model (e.g., regression for prediction) into a LangGraph agent workflow.**

**Sample Answer:**
Treat ML model as a tool:

- Create custom tool @tool that loads model (e.g., scikit-learn joblib or ONNX).
- Input: features from query/context.
- Output: prediction + confidence.
- In graph: Agent decides when to call (e.g., weather query → fetch data tool → ML predict tool → summarize).
For inconsistent data (e.g., global temperature): Agent clusters locations → routes to region-specific lightweight models (stored in vector DB by metadata) → fallback to global if low data. Avoids massive training; uses retrieval + small models per zone.

**Q18: What security considerations apply to RAG/agents in LangChain when handling sensitive data?**

**Sample Answer:**

- Data isolation: Use private vector stores (e.g., self-hosted Chroma/Weaviate) or encrypted embeddings.
- Access control: Metadata filtering + row-level security in vector DB.
- Prompt injection defense: Sanitize inputs, use guards (NeMo Guardrails or LangChain's moderation chain).
- Secrets: Never hardcode; use LangChain's secret management or env vars.
- Logging: Mask PII in LangSmith traces.
- Compliance: Audit trails via checkpoints; self-hosted LangSmith for air-gapped environments.
For sensitive enterprise RAG, combine with GCP Vertex AI private endpoints + encrypted BigQuery.

### Basic Chains & LCEL

**Q1: Implement a simple question-answering chain using LCEL that takes a user question, formats a prompt, calls an LLM, and parses the output as JSON. Use few-shot examples.**

**Sample Solution (LCEL style):**

Python

`from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

parser = JsonOutputParser()

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant. Answer in JSON: {{"answer": "your response", "confidence": 0-100 integer}}.
Examples:
Question: What is the capital of Japan?
{{"answer": "Tokyo", "confidence": 100}}"""),
    ("human", "Question: {question}")
])

chain = (
    {"question": RunnablePassthrough()}
    | prompt
    | llm
    | parser
)

# Usage
result = chain.invoke("What is the boiling point of water in Celsius?")
print(result)  # {'answer': '100', 'confidence': 100}`

**Interview talking points:**

- Why LCEL? Composable, streaming support, better error handling than legacy LLMChain.
- Few-shot in prompt → improves consistency.
- JsonOutputParser → enforces structured output (add PydanticOutputParser for schemas).
- Pitfall: Temperature=0 for deterministic JSON.

### RAG Implementation

**Q2: Build a basic RAG chain: load text documents, split them, embed with OpenAI, store in Chroma vector store, retrieve top-3 chunks with MMR diversity, and generate an answer grounded in context.**

**Sample Solution:**

Python

`from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 1. Load & split
loader = TextLoader("your_company_policy.txt")
docs = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
chunks = splitter.split_documents(docs)

# 2. Embed & store
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(chunks, embeddings, collection_name="policies")

# 3. Retriever with MMR
retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 3, "fetch_k": 20})

# 4. Prompt & chain
prompt = ChatPromptTemplate.from_template(
    """Answer ONLY using this context. If unsure, say "I don't know".
Context: {context}
Question: {question}
Answer:"""
)

llm = ChatOpenAI(model="gpt-4o-mini")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

print(rag_chain.invoke("What is the vacation policy?"))`

**Interview talking points:**

- Chunk overlap prevents context loss at boundaries.
- MMR → diversity, avoids redundant chunks.
- Format docs function → clean context injection.
- Production: Add compression (ContextualCompressionRetriever), hybrid search, or parent-document retriever.

### Agents & Custom Tools

**Q3: Create a ReAct-style agent with two custom tools: one multiplies numbers, one searches Wikipedia (mock it). Bind tools to LLM, run agent executor, and handle multi-turn reasoning.**

**Sample Solution:**

Python

`from langchain_core.tools import tool
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor

@tool
def multiply(a: float, b: float) -> float:
    """Multiplies two numbers."""
    return a * b

@tool
def wikipedia_search(query: str) -> str:
    """Searches Wikipedia and returns summary (mock)."""
    # In real: use WikipediaAPIWrapper
    return f"Mock Wikipedia result for '{query}': Some info here."

tools = [multiply, wikipedia_search]

llm = ChatOpenAI(model="gpt-4o", temperature=0)
prompt = hub.pull("hwchase17/openai-functions-agent")  # or custom ReAct prompt

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_executor.invoke({"input": "What is 15 times the number of moons around Mars? First search how many moons Mars has."})`

**Interview talking points:**

- Tool calling (2026 standard) vs legacy ReAct parsing.
- Verbose=True for debugging traces.
- Add memory: Wrap in RunnableWithMessageHistory.
- Pitfall: LLM hallucinates tool args → use strict schemas + validation.

### LangGraph Stateful Agent

**Q4: Build a simple LangGraph agent that: retrieves from vector store OR searches web (conditional), generates answer, and includes human approval before final output.**

**Sample Solution (simplified):**

Python

`from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AnyMessage, AIMessage
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], "operator.add"]

llm = ChatOpenAI(model="gpt-4o-mini")

def call_model(state: AgentState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

def should_retrieve(state: AgentState):
    last_msg = state["messages"][-1].content
    if "retrieve" in last_msg.lower():
        return "retrieve_node"
    return END

# Dummy nodes
def retrieve_node(state):
    return {"messages": [AIMessage(content="Retrieved context: dummy data")]}

workflow = StateGraph(state_schema=AgentState)
workflow.add_node("model", call_model)
workflow.add_node("retrieve", retrieve_node)

workflow.add_edge(START, "model")
workflow.add_conditional_edges("model", should_retrieve, {"retrieve_node": "retrieve", END: END})
workflow.add_edge("retrieve", "model")  # loop back

graph = workflow.compile(checkpointer=MemorySaver())

# Run with thread
config = {"configurable": {"thread_id": "1"}}
result = graph.invoke({"messages": [{"role": "user", "content": "Tell me about Paris, retrieve facts first."}]}, config)
print(result["messages"][-1].content)`

**Interview talking points:**

- State persistence via checkpointer → resumable, multi-turn.
- Conditional edges → routing logic.
- Human-in-loop: Add interrupt_before=["final_node"].
- Scale: Use PostgresSaver for production.

### Optimization / Debugging

**Q5: Your RAG chain hallucinates despite retrieval. Write code to add a corrective step (CRAG-like): retrieve → LLM judges relevance → if low, web search fallback → regenerate.**

**Interview talking points (sketch code structure):**

- After retriever: Add node that calls LLM with "Rate relevance 1-10 + reason".
- Conditional: If <6 → route to web search tool.
- Use LangGraph for this branching logic.

### Easy / Junior Level (syntax, data structures, basic algorithms)

**Q1: Two Sum**
Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. You may assume exactly one solution and you may not use the same element twice.

**Expected:** O(n) time, O(n) space

**Solution:**

Python

`def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []  # no solution (though problem guarantees one)

# Example
print(two_sum([2, 7, 11, 15], 9))  # [0, 1]`

**Talking points:** Hash map for O(1) lookups beats O(n²) brute force. Follow-up: What if multiple solutions allowed? What if sorted array?

**Q2: Valid Parentheses**
Given a string s containing just '(', ')', '{', '}', '[' and ']', determine if the input string is valid (properly nested and closed).

**Expected:** O(n) time, O(n) space

**Solution:**

Python

`def is_valid(s: str) -> bool:
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}
    
    for char in s:
        if char in mapping:          # closing
            if not stack or stack.pop() != mapping[char]:
                return False
        else:                        # opening
            stack.append(char)
    
    return len(stack) == 0

print(is_valid("()[]{}"))  # True
print(is_valid("(]"))      # False`

**Talking points:** Stack is natural for matching. Edge cases: empty string, single char, odd length.

**Q3: Reverse a Linked List** (very common even in 2026)

**Solution (iterative – preferred):**

Python

`class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head: ListNode) -> ListNode:
    prev = None
    current = head
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    return prev`

**Talking points:** Iterative vs recursive (stack overflow risk on long lists). Follow-up: reverse in groups of k?

### Medium / Mid-Level (frequent in 2026 interviews)

**Q4: Longest Substring Without Repeating Characters**
Given a string s, find the length of the longest substring without repeating characters.

**Expected:** O(n) time, O(min(m, n)) space (m = charset size)

**Solution (sliding window):**

Python

`def length_of_longest_substring(s: str) -> int:
    char_index = {}
    left = max_length = 0
    
    for right, char in enumerate(s):
        if char in char_index and char_index[char] >= left:
            left = char_index[char] + 1
        else:
            max_length = max(max_length, right - left + 1)
        char_index[char] = right
    
    return max_length

print(length_of_longest_substring("abcabcbb"))  # 3 ("abc")
print(length_of_longest_substring("pwwkew"))   # 3 ("wke")`

**Talking points:** Two pointers + dict for last seen index. Alternative: set + remove from left.

**Q5: Group Anagrams**
Given an array of strings strs, group the anagrams together.

**Expected:** O(n * k log k) time (k = max word length), or O(n * k) with counting sort

**Solution:**

Python

`from collections import defaultdict

def group_anagrams(strs: list[str]) -> list[list[str]]:
    groups = defaultdict(list)
    
    for word in strs:
        # sorted tuple as key (immutable)
        key = tuple(sorted(word))
        groups[key].append(word)
    
    return list(groups.values())

# Example
print(group_anagrams(["eat","tea","tan","ate","nat","bat"]))
# [['eat','tea','ate'], ['tan','nat'], ['bat']]`

**Talking points:** Why tuple(sorted())? Why not ''.join(sorted())? Follow-up: What if very long strings → use char count array (26 letters) as key.

**Q6: LRU Cache** (design question – implement or explain)

**Solution (using OrderedDict – clean & Pythonic):**

Python

`from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity
    
    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)  # most recently used
        return self.cache[key]
    
    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # remove LRU (first item)`

**Talking points:** OrderedDict maintains insertion order + move_to_end. Alternative: dict + doubly linked list (more code). Follow-up: thread-safe version?

### Senior / Advanced Level (2026 trends: concurrency, performance, idioms)

**Q7: Implement a thread-safe Singleton (or explain why controversial in Python)**

**Talking points first:** Python modules are singletons by nature; use module-level variables or functools.lru_cache on class method. Classic double-checked locking is overkill due to GIL in many cases.

**Simple modern way:**

Python

`from functools import lru_cache

@lru_cache(maxsize=1)
class Singleton:
    def __init__(self):
        print("Initialized only once")`

**Q8: Merge k Sorted Lists** (heapq is very common)

**Solution:**

Python

`import heapq
from typing import List, Optional

class ListNode: ...

def merge_k_lists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    heap = []
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst.val, i, lst))
    
    dummy = ListNode(0)
    tail = dummy
    
    while heap:
        val, i, node = heapq.heappop(heap)
        tail.next = node
        tail = tail.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    
    return dummy.next`

**Talking points:** Min-heap keeps smallest heads. Time: O(N log k), N=total nodes.

**Q9: Find median from data stream** (two heaps – senior favorite)

Use max-heap (left) + min-heap (right) to balance.

**Q10: Async file downloader** (concurrent.futures or asyncio)

**Talking points:** asyncio.gather() for I/O-bound, ThreadPoolExecutor for mixed.

### Core Language & Internals

1. **Explain the Global Interpreter Lock (GIL) in detail. In 2026, what is the status of PEP 703 (optional/no-GIL builds) and what are the main trade-offs / compatibility issues when using free-threaded Python?**
The GIL is a mutex in CPython that allows only one thread to execute Python bytecode at a time, protecting reference counting and memory management from race conditions. It simplifies the interpreter but prevents true CPU-bound parallelism in threads.
As of early 2026, PEP 703 is accepted and implemented: Python 3.13 added experimental --disable-gil builds; 3.14 significantly improved free-threaded mode (better single-thread performance via adaptive specializing interpreter, fewer workarounds). Free-threading is still **optional/experimental** in official releases — not default. You build with special flags or use third-party no-GIL forks.
Trade-offs: ~10–30% slower single-threaded code in many cases (though mitigated in 3.14), many C extensions crash or silently disable free-threading unless updated (need thread-safety markers), higher memory usage possible. Compatibility issues remain the biggest blocker — major libraries (NumPy, Pandas, some ORMs) are still adapting. Use it for I/O-heavy or carefully tested CPU-parallel workloads; stick to standard builds for production stability.
2. **Walk through Python's memory management — reference counting + cyclic garbage collector. When does the GC run? What are common memory leaks in long-running Python processes?**
Primary: reference counting — every object has a refcount; when it hits zero, memory is freed immediately.
Secondary: cyclic GC (generational, via gc module) detects cycles (e.g., two objects referencing each other) that refcounting misses. It runs automatically when thresholds are hit (e.g., after many allocations), or manually via gc.collect().
Common leaks: unclosed files/connections, cached large objects without expiry, circular references in long-lived structures (e.g., caches, event listeners), global/module-level mutable objects growing indefinitely, C extensions leaking memory.
3. **Descriptors — explain how they work (get, set, delete). Show how @property is actually implemented using descriptors.**
Descriptors are objects implementing __get__, __set__, and/or __delete__ that live in a class and customize attribute access.
Data descriptors (have __set__/__delete__) take precedence over instance attributes; non-data only over lookup.
@property is syntactic sugar:
    
    Python
    
    `class Property:
        def __init__(self, fget=None, fset=None, fdel=None):
            self.fget = fget
            self.fset = fset
            self.fdel = fdel
        def __get__(self, obj, objtype=None):
            return self.fget(obj) if obj else self
        def __set__(self, obj, value):
            self.fset(obj, value)
    # Usage equivalent to @property`
    
4. **What are metaclasses? Give a realistic use-case and explain why most teams avoid writing custom metaclasses in application code.**
Metaclasses are "classes of classes" — they control class creation (__new__, __init__ of the metaclass run when the class is defined).
Realistic use: ORMs (Django models auto-register fields), auto-register plugins, enforce coding standards (e.g., all methods must be documented).
Avoid in app code: they make code hard to read/debug, break introspection tools, increase complexity. Prefer class decorators, __init_subclass__, or ABCs instead.
5. **Explain Method Resolution Order (MRO) and C3 linearization. How do you inspect it?**
MRO defines the search order for methods/attributes in multiple inheritance. Python uses C3 linearization (consistent, monotonic, respects base order).
Inspect with ClassName.mro() or ClassName.__mro__.
Example conflict: diamond inheritance solved by preferring the first-listed base's path.
6. **slots — when and why would you use them? Benefits vs drawbacks?**__slots__ replaces __dict__ with fixed array for attributes → saves memory (~30–50% for many small instances) and speeds attribute access.
Use: millions of small objects (e.g., data points, namedtuples replacement).
Drawbacks: no __dict__ (can't add arbitrary attributes), inheritance more restrictive, pickle/debug harder.
7. **Monkey patching — what is it, how is it done, and when is it acceptable vs harmful?**
Dynamically modifying classes/modules at runtime (e.g., module.func = new_func).
Acceptable: testing (mocking), emergency production fixes, extending third-party libs without forks.
Harmful: breaks expectations, hard to debug, conflicts with other patches, breaks in future versions.

### Concurrency & Async

1. **Compare threading, multiprocessing, and asyncio. When to choose each?**
    - **threading**: shared memory, lightweight, GIL limits CPU work → best for I/O (network, files).
    - **multiprocessing**: separate processes, no GIL, true parallelism → CPU-bound tasks, but high memory/startup cost.
    - **asyncio**: single-threaded cooperative concurrency → high-concurrency I/O (web servers, APIs), clean code with async/await.
2. **Explain how asyncio works under the hood. Difference between create_task(), ensure_future(), and await?**
Event loop schedules coroutines/tasks. await suspends until future completes.
asyncio.create_task() schedules immediately (preferred in 3.7+). ensure_future() wraps legacy futures/coroutines (older name). Use create_task() for new code.
3. **What problems does async/await solve vs older styles? Common anti-patterns?**
Solves callback hell, makes async code look synchronous.
Anti-patterns: blocking calls in async functions (e.g., time.sleep() instead of asyncio.sleep()), running CPU-bound work without offloading, large asyncio.gather() without timeouts/error handling.
4. **In Python 3.11+, explain asyncio.TaskGroup and why it's preferred.**async with asyncio.TaskGroup() as tg: auto-cancels remaining tasks on exception, collects results cleanly, better than manual asyncio.gather() + try/except.
5. **How would you debug a hanging asyncio application?**
Use asyncio.get_event_loop().set_debug(True), uvloop + debug mode, aiomonitor, log pending tasks with asyncio.all_tasks(), profile with asyncio debug + py-spy, check for blocking code.

### Advanced Functions & Patterns

1. **Explain decorators with arguments. Write a timed + logged decorator preserving signature/docstring.**
Decorator factory returns decorator. Use functools.wraps:
    
    Python
    
    `import time, functools, logging
    def timed_logged(level=logging.INFO):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start = time.perf_counter()
                result = func(*args, **kwargs)
                elapsed = time.perf_counter() - start
                logging.log(level, f"{func.__name__} took {elapsed:.4f}s")
                return result
            return wrapper
        return decorator`
    
2. **Generators vs coroutines vs native coroutines (async def). When would you still use yield from vs await?**
    - **Generators** (def + yield): produce sequences lazily (e.g., infinite streams, data pipelines).
    - **Coroutines** (pre-3.5 style): generators enhanced with .send(), .throw(), .close() for two-way communication.
    - **Native coroutines** (async def + await): modern async I/O style; they are awaitables, scheduled by an event loop.
    Use yield from (or yield in async generators) when delegating to sub-generators or sub-coroutines in generator context. Use await in async def functions for cleaner, more readable async code. yield from is still needed in async generators (async def + yield) or when bridging old/new styles.
3. **Context managers — implement one with both class-based and generator-based approaches. When is each better?**
Class-based (more control, e.g., __aenter__/__aexit__ for async):
    
    Python
    
    `class DatabaseConnection:
        def __init__(self, db_url):
            self.db_url = db_url
        def __enter__(self):
            self.conn = connect(self.db_url)
            return self.conn
        def __exit__(self, exc_type, exc_val, exc_tb):
            self.conn.close()`
    
    Generator-based (simpler, using @contextmanager):
    
    Python
    
    `from contextlib import contextmanager
    @contextmanager
    def temp_file(content):
        path = write_temp(content)
        try:
            yield path
        finally:
            os.remove(path)`
    
    Class-based → complex state, inheritance, async support. Generator-based → concise, readable for simple acquire/release patterns.
    
4. **What are dataclasses (from 3.7+), and how do they compare to NamedTuple, attrs, pydantic models in production code?**dataclasses.dataclass auto-generates __init__, __repr__, __eq__, etc., for simple data holders.
    - **NamedTuple**: immutable, tuple-like, fast, hashable by default → good for value objects.
    - **dataclasses**: mutable by default, flexible (field defaults, post-init), type hints friendly → default for internal data classes.
    - **attrs**: more features (validators, converters, slots support), battle-tested → prefer over dataclasses if you need advanced customization.
    - **pydantic**: runtime validation, serialization (JSON), aliases → best for APIs, configs, external data (FastAPI standard).
    In 2026 production: dataclasses for simple internal models; pydantic v2+ for anything touching the outside world.

### Performance & Optimization

1. **How would you profile a slow Python application? Mention tools.**
    - **cProfile** / **profile**: built-in, call counts + cumulative time (good starting point).
    - **line_profiler** / **kernprof**: line-by-line timing (decorate functions with @profile).
    - **py-spy** / **Scalene**: sampling profilers — low overhead, works on production, shows CPU + memory.
    - **memory_profiler**: track memory line-by-line.
    - **objgraph** / **heapy** / **pympler**: for memory leaks.
    - **asyncio**specific: debug mode + aioprofiler.
    Approach: start with py-spy (non-intrusive), drill down with Scalene/line_profiler, check GC with gc.get_stats().
2. **Explain the difference between shallow copy vs deep copy vs what copy.copy() vs copy.deepcopy() actually do. When does it matter with nested objects?**
    - **Shallow copy** (copy.copy(), list[:]): copies the object but references the same nested objects → fast, but shared mutables cause side effects.
    - **Deep copy** (copy.deepcopy()): recursively copies everything → independent tree, but expensive (time + memory), doesn't handle cycles by default without care.
    Matters when: nested lists/dicts are mutated — shallow copy leads to bugs (e.g., modifying one instance affects others). Use shallow for performance when nesting is immutable (e.g., tuples/strings); deep for full isolation.
3. **When should you prefer list vs array.array vs numpy.ndarray vs deque vs collections.Counter?**
    - **list**: general-purpose, dynamic, heterogeneous → default sequence.
    - **array.array**: homogeneous primitives (ints/floats), compact memory → when memory matters more than numpy overhead.
    - **numpy.ndarray**: vectorized ops, numerical computing, broadcasting → scientific/ML data (huge perf win).
    - **deque**: O(1) append/pop from both ends → queues, sliding windows, breadth-first search.
    - **Counter**: dict subclass for counting hashables → frequency tables, multisets.
4. **How can you speed up pure-Python numerical code without rewriting everything in Rust/C++?**
    - Vectorization (numpy/pandas ops instead of loops).
    - **numba**@jit / @njit (LLVM compilation, huge gains on numerical loops).
    - **Cython** (static typing + compile to C).
    - Polars (faster than pandas for large data).
    - Avoid globals, use locals/slots, minimize function calls.
    numba is often the quickest win for existing loops.

### Design & Architecture Questions (senior+ level)

1. **Design a rate limiter (token bucket or sliding window) in Python — thread-safe / async-safe version.**
Token bucket (simple, common):
    
    Python
    
    `import time
    from threading import Lock
    class TokenBucket:
        def __init__(self, capacity: float, refill_rate: float):
            self.capacity = capacity
            self.tokens = capacity
            self.refill_rate = refill_rate
            self.last_refill = time.time()
            self.lock = Lock()
        def acquire(self) -> bool:
            with self.lock:
                now = time.time()
                self.tokens += (now - self.last_refill) * self.refill_rate
                self.tokens = min(self.tokens, self.capacity)
                self.last_refill = now
                if self.tokens >= 1:
                    self.tokens -= 1
                    return True
                return False`
    
    For async: replace Lock with asyncio.Lock, use asyncio.sleep if waiting. Sliding window log alternative for burst control.
    
2. **How would you implement a simple dependency injection container in Python?**
Use a dict of factories + lazy resolution:
    
    Python
    
    `class Container:
        def __init__(self):
            self.factories = {}
            self.instances = {}
        def register(self, key, factory):
            self.factories[key] = factory
        def get(self, key):
            if key not in self.instances:
                factory = self.factories.get(key)
                if factory is None:
                    raise KeyError(key)
                self.instances[key] = factory(self)  # pass container for deps
            return self.instances[key]`
    
    Modern: use injector, dependency-injector, or FastAPI's Depends.
    

1. **Explain trade-offs between FastAPI, Flask, and Django in 2026 for a high-throughput API service.**
    - **FastAPI** (Starlette + Pydantic v2+): async-first, type-hint driven, automatic OpenAPI docs/Swagger, excellent performance (UVLoop + Uvicorn/Hypercorn), dependency injection via Depends, WebSocket/SSE native. → Best for high-throughput, modern microservices/APIs, especially with async DBs (SQLAlchemy 2 async, asyncpg, Tortoise-ORM). Minimal boilerplate, great for teams using type checkers (mypy/pyright).
    - **Flask**: lightweight, synchronous by default (but extensions like Flask-Asyncio exist), extreme flexibility, huge ecosystem. → Good for simple/internal APIs, rapid prototyping, or when you want full control and minimal magic. Performance lower than FastAPI for high concurrency unless you add async/greenlet hacks.
    - **Django** (+ Django REST Framework): batteries-included (ORM, admin, auth, migrations), synchronous core (async views/ORM in 3.1+, improving in 3.14 era). → Ideal for full-stack monolithic apps, enterprise CRUD with complex business logic, when admin panel + security defaults matter. Heavier, slower startup/scaling for pure APIs vs FastAPI.
    2026 choice for high-throughput API: **FastAPI** (dominant in new projects); Django if you need its ecosystem; Flask if you hate magic and want tiny services.
2. **How do you structure a large, long-lived Python monorepo (packaging, dependency management, testing, CI/CD)?**
    - **Tooling (2026 standard)**: uv (Astral's fast Rust-based replacement for pip/poetry, handles workspaces/lockfiles/sync), or Poetry + pdm for legacy.
    - **Layout**: src/ layout (flat packages), multiple sub-packages in one repo (e.g., libs/core, libs/utils, services/api, services/worker). Use pyproject.toml per package + workspace mode.
    - **Dependency mgmt**: central uv.lock or poetry.lock at root, uv sync --frozen in CI, version constraints with ^ / ~= for libs.
    - **Testing**: pytest + pytest-xdist + pytest-asyncio, coverage via coverage.py + pytest-cov, mypy/pyright in pre-commit/CI, Ruff for linting/formatting.
    - **Build/CI**: GitHub Actions / GitLab CI with matrix for Python versions (3.11–3.14), cache uv/venv, semantic-release or bump-my-version for versioning. Deploy via Docker + uv-based images.
    - **Extras**: Pants or Bazel for very large monorepos (faster incremental builds), Hatch for publishing if needed.
3. **What strategies do you use to make Python services observable? (structured logging, metrics, tracing)**
    - **Structured logging**: structlog (JSON + processors for context, request_id, exc_info) or logging + python-json-logger. Bind request/trace IDs via contextvars/middleware.
    - **Metrics**: Prometheus client (prometheus_client), expose /metrics endpoint (FastAPI/Django middleware). Key counters: requests_total, latency histograms, error rates, queue sizes, GC stats.
    - **Distributed tracing**: OpenTelemetry (OTel) Python SDK → auto-instrument (FastAPI, SQLAlchemy, httpx), manual spans for business logic. Export to Jaeger/Zipkin/Tempo or cloud (Datadog, New Relic, Grafana Cloud).
    - **Other**: Sentry for errors (with breadcrumbs/context), health checks (/health, /ready), logging correlation via traceparent header, asyncio task naming for better stacks.
    Goal: full request flow visibility (entry → DB → external → response) with low overhead.
4. **How do you handle backwards compatibility when maintaining a widely-used internal library?**
    - Semantic Versioning (SemVer) strictly: major for breaking changes.
    - Deprecation cycle: add warnings.warn(..., DeprecationWarning) + alternative docs for 2–3 minor releases before removal.
    - Feature flags: internal env var or config to toggle old/new behavior during transition.
    - Dual support: type overloads + typing.TYPE_CHECKING branches, conditional imports for old/new deps.
    - Testing: pin old/new versions in CI matrix, integration tests against consumer services.
    - Changelog + migration guide per release.
    - Tools: packaging for version checks, towncrier for news fragments.

### Bonus Hard / Tricky Questions

1. **Why can def f(a, b=[]): be dangerous? Explain mutable default arguments in detail.**
Defaults evaluated **once** at function definition time → b is the same list instance across all calls. Appending mutates shared state → unexpected side effects (e.g., accumulating across calls).
Fix: def f(a, b=None): b = b if b is not None else [] (sentinel pattern).
2. **What is the difference between is and ==? When can two different objects return True for is?**is checks **identity** (same memory address); == checks **equality** (value via __eq__).
Interning: small ints (-5 to 256), some strings (identifiers), True/False/None are singletons → 256 is 256 is True, but 257 is 257 may be False depending on context. Custom types can override __eq__ but not identity.
3. **Explain __new__ vs __init__. When would you override __new__?**__new__ is static method called to **create** the instance (returns object); __init__ initializes existing instance.
Override __new__ for: singletons (return existing instance), immutable types (e.g., custom str/int), metaclasses, allocating different subclass based on args.
4. **In Python 3.10+ match-case structural pattern matching — give a non-trivial example (e.g., parsing nested JSON or command handling).**
    
    Python
    
    `def handle_event(event: dict):
        match event:
            case {"type": "user_login", "user": {"id": uid, "name": name}, "timestamp": ts}:
                log_login(uid, name, ts)
            case {"type": "order", "items": [*items], "total": total} if total > 1000:
                process_large_order(items, total)
            case {"type": "error", "code": code, "message": msg}:
                alert_error(code, msg)
            case _:
                logger.warning(f"Unknown event: {event}")`
    
    Powerful for nested destructuring, guards (if), class patterns, sequence/star captures — cleaner than nested if/try/except chains.
    

**Preparation tip**: Be ready to code small snippets live (e.g., custom descriptor, async context manager, rate limiter with asyncio.Lock, decorator with args). Explain **trade-offs** (performance vs readability, sync vs async, when to use free-threading). Discuss production war stories (GIL contention, memory leaks, async deadlocks).

### Basic Python Concepts

1. **What is Python? What are its key features and benefits?**
Python is a high-level, interpreted, general-purpose programming language known for readability (uses indentation instead of braces).
Key features: dynamically typed, garbage-collected, extensive standard library, multi-paradigm (procedural, OOP, functional), huge ecosystem (data science, web, automation).
Benefits: fast prototyping, readable code, cross-platform, vast community/packages (pip), beginner-friendly yet powerful for production.
2. **What is the difference between a list and a tuple?**
    - **List**: mutable (can change elements), defined with [], slower for fixed data.
    - **Tuple**: immutable (cannot change after creation), defined with () or just commas, faster, hashable (can be dict keys).
    Use tuple when data shouldn't change (e.g., coordinates); list when you need to modify.
3. **Explain mutable vs immutable objects in Python with examples.**
Immutable: value can't change after creation (int, float, str, tuple, frozenset). Re-assignment creates new object.
Mutable: can be changed in place (list, dict, set, bytearray).
Example:
    
    Python
    
    `a = [1, 2]     # mutable
    b = a
    a.append(3)    # b also becomes [1,2,3]
    x = "hello"    # immutable
    y = x
    x += " world"  # x is new string, y remains "hello"`
    
4. **What is the difference between == and is?**== checks value equality (calls __eq__).
is checks identity (same memory address).
Common gotcha: small integers (-5 to 256) and some strings are interned → 257 == 257 True, but 257 is 257 may be False in different contexts.
5. **Explain *args and **kwargs.**args: collects positional arguments into a tuple.
**kwargs: collects keyword arguments into a dict.
    
    Python
    
    `def func(*args, **kwargs):
        print(args)     # (1, 2, 3)
        print(kwargs)   # {'a': 10, 'b': 20}
    func(1, 2, 3, a=10, b=20)`
    
6. **What are list comprehensions? Give an example.**
Concise way to create lists.
    
    Python
    
    `squares = [x**2 for x in range(10) if x % 2 == 0]  # [0, 4, 16, 36, 64]`
    

### Intermediate Concepts & Patterns

1. **What is a dictionary? How do you handle missing keys safely?**
Key-value store, unordered (insertion order since 3.7+), keys must be hashable.
Safe access: dict.get(key, default), or collections.defaultdict.
    
    Python
    
    `d = {'a': 1}
    print(d.get('b', 0))          # 0
    from collections import defaultdict
    dd = defaultdict(int)
    dd['b'] += 1                   # auto 1`
    
2. **Explain the difference between shallow copy and deep copy.**
Shallow (copy.copy() or list[:]): copies top-level, nested objects shared.
Deep (copy.deepcopy()): recursive copy, fully independent.
Matters with nested mutables:
    
    Python
    
    `import copy
    original = [[1,2], [3,4]]
    shallow = copy.copy(original)
    shallow[0][0] = 99   # original also changed`
    
3. **What are generators? How do they differ from normal functions?**
Functions that use yield to produce values lazily (memory efficient for large/ infinite sequences).
    
    Python
    
    `def fib(n):
        a, b = 0, 1
        for _ in range(n):
            yield a
            a, b = b, a + b
    list(fib(5))  # [0, 1, 1, 2, 3]`
    
4. **What is a decorator? Write a simple one.**
Function that wraps another function to extend behavior (e.g., timing, logging).
    
    Python
    
    `import time
    def timer(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            print(f"{func.__name__} took {time.time() - start:.4f}s")
            return result
        return wrapper
    
    @timer
    def slow():
        time.sleep(1)
    slow()  # prints timing`
    
5. **Explain __init__ and self in classes.**__init__ is the constructor called after object creation.
self refers to the instance (like this in other languages).
    
    Python
    
    `class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age
        def greet(self):
            return f"Hi, I'm {self.name}"`
    
6. **What is inheritance? Give a simple example.**
Child class inherits attributes/methods from parent.
    
    Python
    
    `class Animal:
        def speak(self):
            return "Sound"
    class Dog(Animal):
        def speak(self):
            return "Woof"
    d = Dog()
    print(d.speak())  # Woof`
    

### Common Coding Problems (Easy-Medium)

1. **Reverse a string.**
    
    Python
    
    `s = "hello"
    reversed_s = s[::-1]          # easiest
    # or
    reversed_s = "".join(reversed(s))`
    
2. **Check if a string is a palindrome (ignore case/spaces).**
    
    Python
    
    `def is_palindrome(s):
        cleaned = ''.join(c.lower() for c in s if c.isalnum())
        return cleaned == cleaned[::-1]`
    
3. **Find duplicates in a list.**
    
    Python
    
    `def find_duplicates(lst):
        seen = set()
        duplicates = set()
        for num in lst:
            if num in seen:
                duplicates.add(num)
            seen.add(num)
        return list(duplicates)`
    
4. **FizzBuzz (1 to n: "Fizz" for 3, "Buzz" for 5, "FizzBuzz" for both).**
    
    Python
    
    `def fizzbuzz(n):
        for i in range(1, n+1):
            if i % 15 == 0:
                print("FizzBuzz")
            elif i % 3 == 0:
                print("Fizz")
            elif i % 5 == 0:
                print("Buzz")
            else:
                print(i)`
    
5. **Two Sum: return indices of two numbers that add to target.**
(Classic LeetCode easy)
    
    Python
    
    `def two_sum(nums, target):
        seen = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
        return []`
    
6. **Merge two sorted lists into one sorted list.**
    
    Python
    
    `def merge_sorted(a, b):
        result = []
        i = j = 0
        while i < len(a) and j < len(b):
            if a[i] < b[j]:
                result.append(a[i])
                i += 1
            else:
                result.append(b[j])
                j += 1
        result.extend(a[i:])
        result.extend(b[j:])
        return result`
    

**Tips for basic-mid interviews (2026)**:

- Know PEP 8 style basics (indent 4 spaces, snake_case).
- Be comfortable with list/dict/set comprehensions, slicing, enumerate.
- Practice explaining time/space complexity (O(n), O(1), etc.).
- Use built-ins wisely (sorted(), len(), range(), zip(), etc.).
- For coding rounds: talk through your thought process, handle edge cases (empty input, negatives, duplicates).