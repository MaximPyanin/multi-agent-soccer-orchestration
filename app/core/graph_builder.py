from IPython.core.display import Image
from IPython.core.display_functions import display
from langgraph.graph import StateGraph, START, END

from app.domain.models.conversation_state import ConversationState
from app.controllers.agents_controller import AgentsController


class GraphBuilder:
    """
    Main orchestrator for managing chat workflow execution.

    Builds and manages the LangGraph workflow that coordinates
    different agents and processing steps in the chat system.
    """

    def __init__(self, agents_controller: AgentsController) -> None:
        """
        Initialize the workflow orchestrator.

        Args:
            agents_controller: Controller for managing workflow operations
        """
        self._agents_controller = agents_controller
        self._state_graph = StateGraph(ConversationState)
        self._build_workflow_graph()
        self._compiled_workflow = self._state_graph.compile()

    def visualize_workflow(self, *, enable_xray: bool = False):
        """
        Generate and display a visual representation of the workflow.

        Args:
            enable_xray: Whether to enable X-ray view for detailed inspection

        Returns:
            PNG image of the workflow diagram
        """
        return display(Image(self._state_graph.get_graph(xray=True).draw_mermaid_png()))

    def _build_workflow_graph(self) -> StateGraph:
        """
        Build the internal workflow graph structure.

        Returns:
            Configured StateGraph instance
        """

        self._state_graph.add_node(
            "supervisor", self._agents_controller.get_routing_decision
        )
        self._state_graph.add_node("search_agent", self._agents_controller.search_web)
        self._state_graph.add_node(
            "fotmob_agent", self._agents_controller.fetch_football_data
        )
        self._state_graph.add_node(
            "conversational_agent", self._agents_controller.generate_response
        )

        self._state_graph.add_edge(START, "supervisor")
        self._state_graph.add_edge("conversational_agent", END)

        return self._state_graph

    async def execute_workflow(self, initial_state: ConversationState):
        """
        Execute the complete workflow with the given initial state.

        Args:
            initial_state: Starting state for the workflow execution

        Returns:
            Final state after workflow completion
        """
        return await self._compiled_workflow.ainvoke(initial_state)
