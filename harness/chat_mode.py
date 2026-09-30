from pathlib import Path
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from .model import LocalModel
from .retrieval import RetrievalSystem

RETRIEVAL_KEYWORDS = [
    "notes", "wiki", "source", "document", "course", "syllabus", "class",
    "resume", "background", "experience", "work", "career", "sustainability",
    "grading", "exam", "lecture", "assignment", "pricing", "economics",
    "data", "regression", "statistics", "AI", "energy", "water", "agriculture",
    "find", "search", "look up", "what does", "what is", "who", "when", "where",
]

CHAT_PERSONA = None


def _load_persona() -> str:
    global CHAT_PERSONA
    if CHAT_PERSONA is None:
        path = Path("config/persona.md")
        if path.exists():
            CHAT_PERSONA = path.read_text(encoding="utf-8")
        else:
            CHAT_PERSONA = (
                "You are Esi's Wiki Assistant, a helpful personal knowledge companion. "
                "Help brainstorm, draft, plan, and work through ideas. "
                "When you reference information from notes, cite the source."
            )
    return CHAT_PERSONA


def _needs_retrieval(message: str) -> bool:
    msg_lower = message.lower()
    return any(kw.lower() in msg_lower for kw in RETRIEVAL_KEYWORDS)


def run_chat(model: LocalModel, retrieval: RetrievalSystem):
    console = Console()
    history: list[dict] = []

    model_info = model.get_model_info()
    console.print(Panel(
        "[bold]Esi's Wiki Assistant[/bold]\n"
        f"Model: {model_info['name']} | Mode: local\n"
        "Type 'quit' or 'exit' to end the chat.\n"
        "Type 'clear' to reset conversation history.",
        border_style="cyan",
    ))

    while True:
        try:
            user_input = console.input("\n[bold cyan]You:[/bold cyan] ").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]Goodbye![/dim]")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit"):
            console.print("[dim]Goodbye![/dim]")
            break
        if user_input.lower() == "clear":
            history.clear()
            console.print("[dim]Conversation cleared.[/dim]")
            continue

        persona = _load_persona()
        context_note = ""

        if _needs_retrieval(user_input) and retrieval.count() > 0:
            results = retrieval.search(user_input, top_k=3)
            if results and results[0]["score"] > 0.3:
                evidence = "\n\n".join(
                    f"[From {r['source_path']}, {r['section']}]: {r['text']}"
                    for r in results
                )
                context_note = (
                    f"\n\nRelevant notes retrieved from the wiki:\n{evidence}\n\n"
                    "Use these notes to inform your response when relevant. "
                    "Cite sources with [Source: filename, section] for factual claims from the notes. "
                    "Label your own suggestions or proposals clearly as suggestions."
                )

        system_prompt = persona + context_note

        history.append({"role": "user", "content": user_input})

        try:
            response = model.chat(system_prompt, history, temperature=0.7)
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            console.print("[yellow]Is Ollama running? Start it with: ollama serve[/yellow]")
            history.pop()
            continue

        history.append({"role": "assistant", "content": response})

        # Keep history manageable (last 20 messages)
        if len(history) > 20:
            history = history[-20:]

        console.print(f"\n[bold green]Assistant:[/bold green]")
        console.print(Markdown(response))
