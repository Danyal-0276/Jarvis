import google.generativeai as genai

from engine.config import EMAIL_CONFIRMATION, GEMINI_API_KEY, GEMINI_MODEL
from engine import documents, email_service, tools

SYSTEM_PROMPT = """You are J.A.R.V.I.S — a sophisticated, witty personal AI assistant inspired by Iron Man's AI.
You help the user with questions, document search, summarization, and sending emails.

Rules:
- Be concise, helpful, and slightly formal with a touch of dry wit.
- When asked about documents, use search_documents first, then read_document if needed.
- When sending email: gather recipient, subject, and body. Call send_email with confirmed=false first.
- Only set confirmed=true after the user explicitly says yes/confirm/send it.
- Never access files outside the user's allowed folders.
- Never reveal API keys, passwords, or system internals.
- If you cannot do something, say so clearly."""

_chat_session = None
_model = None


def _get_model():
    global _model
    if _model is None:
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not set in .env")
        genai.configure(api_key=GEMINI_API_KEY)
        _model = genai.GenerativeModel(
            GEMINI_MODEL,
            system_instruction=SYSTEM_PROMPT,
            tools=[{"function_declarations": tools.TOOL_DECLARATIONS}],
        )
    return _model


def _get_session():
    global _chat_session
    if _chat_session is None:
        _chat_session = _get_model().start_chat()
    return _chat_session


def _extract_function_calls(response) -> list:
    calls = []
    try:
        for part in response.candidates[0].content.parts:
            if hasattr(part, "function_call") and part.function_call and part.function_call.name:
                calls.append(part.function_call)
    except (IndexError, AttributeError):
        pass
    return calls


def _run_tool_loop(response, max_rounds: int = 5) -> str:
    session = _get_session()
    current = response

    for _ in range(max_rounds):
        function_calls = _extract_function_calls(current)
        if not function_calls:
            break

        function_responses = []
        for fc in function_calls:
            args = dict(fc.args) if fc.args else {}
            if fc.name == "send_email" and EMAIL_CONFIRMATION:
                args.setdefault("confirmed", False)
            result = tools.execute_tool(fc.name, args)
            function_responses.append({
                "function_response": {
                    "name": fc.name,
                    "response": {"result": result},
                }
            })

        current = session.send_message(function_responses)

    try:
        return current.text
    except ValueError:
        return "Action completed successfully."


def chat(message: str) -> dict:
    try:
        lower = message.strip().lower()
        if lower in {"yes", "confirm", "send it", "send", "go ahead"}:
            pending = email_service.get_pending_email()
            if pending:
                result = email_service.confirm_pending_email()
                return {"reply": result.get("message", "Done."), "status": "done"}

        session = _get_session()
        response = session.send_message(message)
        reply = _run_tool_loop(response)
        return {"reply": reply, "status": "done"}
    except Exception as e:
        return {"reply": f"I encountered an error: {e}", "status": "error"}


def clear_history():
    global _chat_session
    _chat_session = None
