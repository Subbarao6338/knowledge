# Prompt Engineering Cheatsheet

Prompt Engineering is the practice of structuring text inputs to large language models (LLMs) to maximize response accuracy, reasoning quality, and formatting adherence.

---

## 1. System Prompt vs User Prompt

- **System Prompt:** Sets the persona, boundaries, safety rules, output schemas, and permanent constraints of the agent.
- **User Prompt:** The dynamic user input containing the active question, raw text context, or execution task.

---

## 2. Advanced Prompting Techniques

### Few-Shot Prompting
Provide explicit examples of inputs and desired outputs to guide the model's reasoning style and output schema.

```text
Classify the sentiment of the following technical logs:

Input: "ERROR: Connection timeout to DB at 10:02"
Output: Negative (Severity: High)

Input: "INFO: Batch processed successfully in 2.3s"
Output: Positive (Severity: Low)

Input: "WARN: Memory utilization at 82%"
Output: Neutral (Severity: Medium)

Input: "ERROR: User session authorization failed"
Output:
```

### Chain of Thought (CoT)
Ask the model to break down its reasoning step-by-step before outputting the final answer. This significantly improves accuracy in mathematical, logical, and code-generation tasks.

```text
User: "Calculate the total cloud monthly cost for: 3 EC2 instances at $40/mo each, 1 RDS instance at $80/mo, and a 15% committed use discount applied across the entire bill."
Assistant: "Let's calculate this step-by-step:
1. Find the base cost of EC2 instances: 3 * $40 = $120/mo.
2. Find the base cost of RDS instance: 1 * $80 = $80/mo.
3. Combine the base costs: $120 + $80 = $200/mo.
4. Calculate the 15% discount: 15% of $200 = 0.15 * 200 = $30.
5. Subtract the discount from the base cost: $200 - $30 = $170/mo.
Therefore, the total monthly cloud cost is $170."
```

### Retrieval-Augmented Generation (RAG) Context Format
Inject structured documentation snippets directly into the user prompt to allow the model to answer questions based on private data.

```text
Use the reference context below to answer the user query. Do not assume or extrapolate facts not present in the context.

Context:
[Doc ID: 1] "The recovery time objective (RTO) for the customer payment database is 15 minutes. The recovery point objective (RPO) is 5 minutes using continuous cross-region replication."

Query: "What is the RPO for the customer payment database?"
```
