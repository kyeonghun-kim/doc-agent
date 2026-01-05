# src/agent/chat_agent.py
from __future__ import annotations

from typing import TypedDict, List, Annotated, Dict
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

load_dotenv()


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

    # 만들어진 문서
    docs: Dict
