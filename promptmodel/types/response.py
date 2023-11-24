from typing import (
    List,
    Dict,
    Any,
    Optional,
)
from pydantic import BaseModel
from litellm.utils import (
    ModelResponse,
    Usage,
    Message,
    Choices,
    StreamingChoices,
    Delta,
    FunctionCall,
    Function,
    ChatCompletionMessageToolCall,
)
from openai._models import BaseModel as OpenAIObject
from openai.types.chat.chat_completion import *
from openai.types.chat.chat_completion_chunk import (
    ChoiceDeltaFunctionCall,
    ChoiceDeltaToolCall,
    ChoiceDeltaToolCallFunction,
)


class LLMResponse(OpenAIObject):
    api_response: Optional[ModelResponse] = None
    raw_output: Optional[str] = None
    parsed_outputs: Optional[Dict[str, Any]] = None
    error: Optional[bool] = None
    error_log: Optional[str] = None
    function_call: Optional[FunctionCall] = None
    tool_calls: Optional[List[ChatCompletionMessageToolCall]] = None


class LLMStreamResponse(OpenAIObject):
    api_response: Optional[ModelResponse] = None
    raw_output: Optional[str] = None
    parsed_outputs: Optional[Dict[str, Any]] = None
    error: Optional[bool] = None
    error_log: Optional[str] = None
    function_call: Optional[ChoiceDeltaFunctionCall] = None
    tool_calls: Optional[List[ChoiceDeltaToolCall]] = None


class PromptModelConfig:
    def __init__(self, prompts, version_detail) -> None:
        self.prompts = prompts
        self.version_detail = version_detail


class ChatModelConfig:
    def __init__(
        self, prompts, version_detail, message_logs: Optional[Dict] = None
    ) -> None:
        self.prompts = prompts
        self.version_detail = version_detail
        self.message_logs = message_logs if message_logs else prompts


class FunctionSchema(BaseModel):
    """
    {
            "name": str,
            "description": Optional[str],
            "parameters": {
                "type": "object",
                "properties": {
                    "argument_name": {
                        "type": str,
                        "description": Optional[str],
                        "enum": Optional[List[str]]
                    },
                },
                "required": Optional[List[str]],
            },
        }
    """

    class _Parameters(BaseModel):
        class _Properties(BaseModel):
            type: str
            description: Optional[str] = ""
            enum: Optional[List[str]] = []

        type: str = "object"
        properties: Dict[str, _Properties] = {}
        required: Optional[List[str]] = []

    name: str
    description: Optional[str] = None
    parameters: _Parameters