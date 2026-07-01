from react_nodes import ThinkNode
from base_nodes import Flow

class Agent:
    def __init__(self, llm):
        """
        Initializes the agent by setting up the LLM, defining the execution 
        workflow (starting with a thought process), and creating a shared 
        dictionary to track state, memory, and limits across steps.
        """
        self._llm = llm
        think_node = ThinkNode()
        self.flow = Flow(start=think_node)
        
    def run(self, messages):
        """
        Executes the agent's logic for a given input: logs the user's message, 
        increments the step counter, runs the defined workflow through the shared 
        state, and returns the final generated response text.
        """
        shared = {
            "llm": self._llm,
            "messages": messages.copy(),
            "iterations": 1,
            "max_iterations": 8,
            "last_thought": None,
        }

        self.flow.run(shared)

        return shared["messages"][-1]["content"]
