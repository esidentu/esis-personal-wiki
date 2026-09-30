from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .retrieval import RetrievalSystem


def run_search(query: str, retrieval: RetrievalSystem, top_k: int = 5):
    console = Console()

    if retrieval.count() == 0:
        console.print("[yellow]No passages indexed yet. Run 'wiki ingest' first.[/yellow]")
        return

    console.print(f"\n[bold]Searching for:[/bold] {query}\n")

    results = retrieval.search(query, top_k=top_k)

    if not results:
        console.print("[yellow]No matching passages found.[/yellow]")
        return

    console.print(f"[dim]Found {len(results)} passages:[/dim]\n")

    for i, result in enumerate(results, 1):
        score_pct = f"{result['score']:.0%}"
        header = f"[{i}] {result['source_path']} — {result['section']} (relevance: {score_pct})"

        passage_text = result["text"]
        if len(passage_text) > 500:
            passage_text = passage_text[:500] + "..."

        console.print(Panel(
            passage_text,
            title=header,
            title_align="left",
            border_style="blue",
        ))
