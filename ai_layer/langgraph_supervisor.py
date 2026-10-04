import operator
from collections.abc import Sequence
from typing import Annotated, Literal, TypedDict

from langchain_core.messages import AIMessage, BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next_node: str
    requires_human_approval: bool
    risk_level: Literal["low", "medium", "high"]
    artifacts: dict


class Supervisor:
    def __init__(self):
        self.primary_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    async def __call__(self, state: AgentState):
        system_prompt = (
            "You are the supervisor coordinating specialized worker nodes. "
            "Choose next worker: 'researcher', 'action_worker', 'human_gate', or 'FINISH'."
        )
        messages = [{"role": "system", "content": system_prompt}] + list(state["messages"])
        response = await self.primary_llm.ainvoke(messages)
        content = response.content.strip().lower()

        if "research" in content:
            next_step = "researcher"
        elif "action" in content or "execute" in content:
            next_step = "action_worker"
        elif "human" in content or state.get("risk_level") == "high":
            next_step = "human_gate"
        else:
            next_step = "FINISH"

        return {"next_node": next_step}


async def researcher_node(state: AgentState):
    return {
        "messages": [
            AIMessage(content="[Researcher]: Extracted relevant facts from vector context.")
        ],
        "risk_level": "low",
    }


async def action_worker_node(state: AgentState):
    return {
        "messages": [AIMessage(content="[ActionWorker]: Executed isolated FastMCP tool call.")],
        "risk_level": "low",
    }


async def human_gate_node(state: AgentState):
    return {"requires_human_approval": False}


def build_supervisor_graph(checkpointer=None):
    workflow = StateGraph(AgentState)
    supervisor = Supervisor()

    workflow.add_node("supervisor", supervisor)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("action_worker", action_worker_node)
    workflow.add_node("human_gate", human_gate_node)

    workflow.add_edge(START, "supervisor")

    def route_decision(state: AgentState) -> str:
        if state["next_node"] == "FINISH":
            return END
        return state["next_node"]

    workflow.add_conditional_edges(
        "supervisor",
        route_decision,
        {
            "researcher": "researcher",
            "action_worker": "action_worker",
            "human_gate": "human_gate",
            END: END,
        },
    )

    workflow.add_edge("researcher", "supervisor")
    workflow.add_edge("action_worker", "supervisor")
    workflow.add_edge("human_gate", "supervisor")

    return workflow.compile(
        checkpointer=checkpointer,
        interrupt_before=["human_gate"],  # Halts before sensitive actions
    )
