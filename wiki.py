import sys
from pathlib import Path

import click
from rich.console import Console

console = Console()


def _get_model():
    from harness.model import LocalModel
    model = LocalModel()
    if not model.is_available():
        console.print("[red]Error: Ollama is not running.[/red]")
        console.print("Start it with: [bold]ollama serve[/bold]")
        console.print("Then pull the model: [bold]ollama pull gemma3:4b[/bold]")
        sys.exit(1)
    return model


def _get_retrieval():
    from harness.retrieval import RetrievalSystem
    return RetrievalSystem(chroma_dir="data/chroma")


@click.group()
@click.version_option(version="1.0.0", prog_name="Esi's Wiki CLI")
def cli():
    """Esi's Personal Wiki CLI — chat, ask, search your personal knowledge base.

    Uses local Gemma model via Ollama with RAG for grounded answers.
    All modes work offline after initial setup.
    """
    pass


@cli.command()
@click.argument("path", type=click.Path(exists=True))
def ingest(path):
    """Ingest source documents and generate wiki pages.

    Reads files from PATH, splits them into passages for retrieval,
    generates wiki pages via Gemma, and updates the index.

    Example: wiki ingest ./vault/raw
    """
    from harness.ingest import ingest_source

    source_path = Path(path)
    model = _get_model()
    retrieval = _get_retrieval()

    model_info = model.get_model_info()
    console.print(f"[bold]Model:[/bold] {model_info['name']} ({model_info['parameter_size']}, {model_info['quantization']})")
    console.print(f"[bold]Mode:[/bold] local\n")

    if source_path.is_file():
        files = [source_path]
    else:
        files = sorted(source_path.glob("*.txt")) + sorted(source_path.glob("*.md"))

    if not files:
        console.print(f"[yellow]No .txt or .md files found in {path}[/yellow]")
        return

    console.print(f"Found {len(files)} source file(s) to ingest:\n")

    total_pages = []
    for f in files:
        console.print(f"[bold]Ingesting:[/bold] {f.name}")
        pages = ingest_source(f, model, retrieval, console=console)
        total_pages.extend(pages)
        console.print()

    console.print(f"[bold green]Done![/bold green] Created {len(total_pages)} wiki pages.")
    console.print(f"Retrieval index: {retrieval.count()} passages indexed.")
    console.print(f"Open [bold]vault/[/bold] in Obsidian to browse your wiki.")


@cli.command()
@click.argument("query")
@click.option("--top", "-k", default=5, help="Number of results to show")
def search(query, top):
    """Search for matching passages in the wiki (no LLM generation).

    Returns original source passages and their locations.
    Does not require the language model to be running.

    Example: wiki search "pricing strategy"
    """
    from harness.search_mode import run_search
    retrieval = _get_retrieval()
    run_search(query, retrieval, top_k=top)


@cli.command()
@click.argument("question")
@click.option("--save", "-s", default=None, help="Save evidence card to this path")
@click.option("--mode", "-m", default="local", help="Execution mode (local/online)")
def ask(question, save, mode):
    """Ask a factual question and get a cited answer from your wiki.

    Each question is independent — no chat history is used.
    The answer is grounded in retrieved evidence with citations.

    Example: wiki ask "What is the AI policy for MBA courses?"
    """
    from harness.ask_mode import run_ask
    model = _get_model()
    retrieval = _get_retrieval()
    run_ask(question, model, retrieval, save_path=save)


@cli.command()
def chat():
    """Start an interactive chat session with your wiki assistant.

    The assistant uses conversation context for follow-ups and retrieves
    notes when your question references wiki content.

    Type 'quit' to exit, 'clear' to reset conversation.
    """
    from harness.chat_mode import run_chat
    model = _get_model()
    retrieval = _get_retrieval()
    run_chat(model, retrieval)


if __name__ == "__main__":
    cli()
