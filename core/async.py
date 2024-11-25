from typing import Annotated, Any
from dotenv import load_dotenv
import operator
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END

# Load environment variables from a .env file
load_dotenv()


# Define the state model using Pydantic for type validation
class State(BaseModel):
    # 'aggregate' will hold a list of strings, with operator.add handling list concatenation
    aggregate: Annotated[list, operator.add]


# Class to handle node operations
class ReturnNodeValue:

    def __init__(self, node_secret: str):
        """
        Initialize the node with a secret value (node name).
        """
        self._value = node_secret  # Store the node name

    def __call__(self, state: State) -> Any:
        """
        Callable method to execute the node's functionality.
        Prints the node's name and updates the state's aggregate list.
        """
        import time
        time.sleep(1)
        print(f"Adding {self._value} to {state.aggregate}")
        # Append the node's name to the aggregate list in the state
        return {"aggregate": [self._value]}


# Initialize the StateGraph with the defined State model
builder = StateGraph(State)

# Add nodes to the graph with their respective operations
builder.add_node("a", ReturnNodeValue("I'm A"))  # Node A
builder.add_edge(START, "a")  # Connect START to A

builder.add_node("b", ReturnNodeValue("I'm B"))  # Node B
builder.add_node("b2", ReturnNodeValue("I'm B2"))  # Node B2
builder.add_node("c", ReturnNodeValue("I'm C"))  # Node C
builder.add_node("d", ReturnNodeValue("I'm D"))  # Node D

# Define edges to create the graph topology
builder.add_edge("a", "b")  # Connect A to B
builder.add_edge("a", "c")  # Connect A to C
builder.add_edge("b", "b2")  # Connect B to B2
builder.add_edge(["b2", "c"], "d")  # Connect B2 and C to D
builder.add_edge("d", END)  # Connect D to END

# Compile the graph to prepare it for execution
graph = builder.compile()

# Generate a visual representation of the graph and save it as 'async.png'
graph.get_graph().draw_mermaid_png(output_file_path="async2.png")

if __name__ == '__main__':
    # Print a greeting message
    print("Hello Async Graph")

    # Invoke the graph with initial input and configuration
    graph.invoke(
        input={"aggregate": []},  # Initialize 'aggregate' as an empty list
        config={"configurable": {"thread_id": "foo"}}  # Configuration for tracing
    )
