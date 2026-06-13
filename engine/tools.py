from engine import documents, email_service

TOOL_DECLARATIONS = [
    {
        "name": "search_documents",
        "description": "Search the user's local documents by keyword. Returns matching file names and snippets.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search keywords, e.g. 'resume', 'invoice', 'project report'",
                }
            },
            "required": ["query"],
        },
    },
    {
        "name": "read_document",
        "description": "Read the full text content of a specific document file by its full path.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Full file path returned from search_documents",
                }
            },
            "required": ["path"],
        },
    },
    {
        "name": "send_email",
        "description": (
            "Send an email from the user's Gmail account. "
            "Always set confirmed=false first to get a preview, then confirmed=true only after user says yes."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "to": {"type": "string", "description": "Recipient email address"},
                "subject": {"type": "string", "description": "Email subject line"},
                "body": {"type": "string", "description": "Email body text"},
                "confirmed": {
                    "type": "boolean",
                    "description": "Set true only after user explicitly confirms sending",
                },
            },
            "required": ["to", "subject", "body"],
        },
    },
]


def execute_tool(name: str, args: dict) -> str:
    try:
        if name == "search_documents":
            results = documents.search_documents(args.get("query", ""))
            if not results:
                return "No documents found matching that query."
            lines = [f"- {r['name']} ({r['path']}): {r['snippet'][:150]}" for r in results]
            return "Found documents:\n" + "\n".join(lines)

        if name == "read_document":
            return documents.read_document(args.get("path", ""))

        if name == "send_email":
            result = email_service.send_email(
                to=args.get("to", ""),
                subject=args.get("subject", ""),
                body=args.get("body", ""),
                confirmed=args.get("confirmed", False),
            )
            return result.get("message", str(result))

        return f"Unknown tool: {name}"
    except Exception as e:
        return f"Tool error: {e}"
