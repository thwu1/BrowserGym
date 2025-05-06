from abc import ABC, abstractmethod
import contextvars
import types
import asyncio
from browsergym.async_core.action.functions import (
    page_ctx,
    send_message_to_user_ctx,
    report_infeasible_instructions_ctx,
    retry_with_force_ctx,
    demo_mode_ctx,
)
import playwright.async_api
import textwrap
from . import get_global_demo_mode

_ACTION_EXEC_MODULE = None


class AbstractActionSet(ABC):
    def __init__(self, strict: bool = False):
        self.strict = strict

    @abstractmethod
    def describe(self, with_long_description: bool = True, with_examples: bool = True) -> str:
        """
        Returns a textual description of this action space.
        """

    @abstractmethod
    def example_action(self, abstract: bool) -> str:
        """
        Returns an example action as a string.
        """

    @abstractmethod
    def to_python_code(self, action) -> str:
        """
        Converts the given action to browsergym-compatible python code.

        Args:
            action: the action to convert.

        Returns:
            Executable python code that performs the action in a browsergym environment.
        """


async def execute_python_code(
    code: str,
    page: playwright.async_api.Page,
    send_message_to_user: callable,
    report_infeasible_instructions: callable,
):
    """
    Executes Python code in a new context with proper global variable handling.

    Args:
        code: the Python code to execute, as a string.
        page: the playwright page that will be made accessible to the code.
        send_message_to_user: utility function for sending messages to the user.
        report_infeasible_instructions: utility function for reporting infeasible instructions.
    """
    global _ACTION_EXEC_MODULE

    # Initialize the module cache once (for efficiency)
    if _ACTION_EXEC_MODULE is None:
        _ACTION_EXEC_MODULE = types.ModuleType("action_exec_module")

        # Add function references to the module - these point to the contextvars-based functions
        import browsergym.async_core.action.functions as functions
        import browsergym.async_core.action.utils as utils

        for module in [functions, utils]:
            for name, value in module.__dict__.items():
                if (
                    callable(value)
                    and not name.startswith("_")
                    and not isinstance(value, contextvars.ContextVar)
                ):
                    setattr(_ACTION_EXEC_MODULE, name, value)

        # Add essential utilities
        _ACTION_EXEC_MODULE.asyncio = asyncio

    # Determine values for this execution context
    retry_with_force = "OVERRIDE_RETRY_WITH_FORCE=True" in code
    demo_mode = "default" if get_global_demo_mode() else "off"

    # Create a context for this execution
    ctx = contextvars.copy_context()

    # Define the function that will run in the copied context
    # This time all variables are properly captured
    async def run_in_context():
        # Set all context variables
        page_ctx.set(page)
        send_message_to_user_ctx.set(send_message_to_user)
        report_infeasible_instructions_ctx.set(report_infeasible_instructions)
        retry_with_force_ctx.set(retry_with_force)
        demo_mode_ctx.set(demo_mode)

        # Continue with execution...
        namespace = _ACTION_EXEC_MODULE.__dict__.copy()
        wrapped_code = f"""
async def __user_code_main__():
{textwrap.indent(code, '    ')}

# Store for later execution
__user_code_result__ = __user_code_main__()
"""
        exec(wrapped_code, namespace)
        await namespace["__user_code_result__"]

    # Run the execution in the isolated context
    await ctx.run(run_in_context)
