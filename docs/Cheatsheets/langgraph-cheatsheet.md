---
layout: default
title: "LangGraph Cheatsheet"
---

# LangGraph Cheatsheet

LangGraph is an advanced orchestration framework by LangChain, designed for building stateful, multi-actor, cyclic agent systems using graphs.

---

## 1. Defining State & Graph Schema

The backbone of a LangGraph system is its state schema. The state is represented as a TypedDict or Pydantic model passed from node to node.

```python
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

# Define the central shared state
class AgentState(TypedDict):
    # add_messages appends new messages rather than overwriting the key
    messages: Annotated[list, add_messages]
    sender: str
    is_valid: bool
```

---

## 2. Building Graph Nodes & Edges

Nodes are simple Python functions (synchronous or asynchronous) that accept the state, perform logic, and return an updated slice of the state.

```python
from langgraph.graph import StateGraph, START, END

# Define Node 1: Classifier Agent
def classifier_node(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1].content

    # Simple logic to validate content
    is_valid = "api_key" not in last_message.lower()
    return {
        "messages": [("assistant", "Input validated.")],
        "sender": "classifier",
        "is_valid": is_valid
    }

# Define Node 2: Processor Agent
def processor_node(state: AgentState):
    return {
        "messages": [("assistant", "Processing complete.")],
        "sender": "processor"
    }

# Define Node 3: Error Handler Agent
def error_node(state: AgentState):
    return {
        "messages": [("assistant", "Validation failed! Found sensitive patterns.")],
        "sender": "error_handler"
    }
```

---

## 3. Wiring the StateGraph Pipeline

Assemble nodes, straight edges, and conditional routing paths into a compiled executable pipeline.

```python
# Initialize graph with state schema
workflow = StateGraph(AgentState)

# Add all nodes to graph
workflow.add_node("classifier", classifier_node)
workflow.add_node("processor", processor_node)
workflow.add_node("error_handler", error_node)

# Set starting entry-point
workflow.add_edge(START, "classifier")

# Define conditional routing function
def route_after_classification(state: AgentState):
    if state["is_valid"]:
        return "processor"
    return "error"

# Add conditional edges from 'classifier'
workflow.add_conditional_edges(
    "classifier",
    route_after_classification,
    {
        "processor": "processor",
        "error": "error_handler"
    }
)

# Connect remaining paths to terminal endpoint END
workflow.add_edge("processor", END)
workflow.add_edge("error_handler", END)

# Compile the graph into a runnable application
app = workflow.compile()
```

---

## 4. Execution & Streaming API

Invoke or stream states through the compiled multi-agent network.

### Synchronous Execution (`invoke`)
```python
initial_input = {
    "messages": [("user", "Hello! Process database configuration info: api_key=123")]
}

result = app.invoke(initial_input)
print("Final Sender:", result["sender"])
print("Final Message:", result["messages"][-1].content)
```

### Dynamic Message Streaming (`stream`)
Stream updates page-by-page or step-by-step as nodes execute sequentially.

```python
for event in app.stream(initial_input):
    for node_name, state_update in event.items():
        print(f"--- Node '{node_name}' Finished ---")
        if "messages" in state_update:
            print(f"Update: {state_update['messages'][-1][1]}")
```
