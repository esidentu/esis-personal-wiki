from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from .model import LocalModel
from .retrieval import RetrievalSystem

ASK_INSTRUCTIONS = None


def _load_instructions() -> str:
    global ASK_INSTRUCTIONS
    if ASK_INSTRUCTIONS is None:
        path = Path("config/wiki-instructions.md")
        if path.exists():
            ASK_INSTRUCTIONS = path.read_text(encoding="utf-8")
        else:
            ASK_INSTRUCTIONS = (
                "You are a factual research assistant. Answer ONLY from the provided evidence. "
                "Cite sources with [Source: filename, section]. "
                "If the evidence does not support the answer, say: "
                "'The wiki does not contain sufficient evidence to answer this question.'"
            )
    return ASK_INSTRUCTIONS


def run_ask(question: str, model: LocalModel, retrieval: RetrievalSystem, save_path: str | None = None):
    console = Console()

    if retrieval.count() == 0:
        console.print("[yellow]No passages indexed yet. Run 'wiki ingest' first.[/yellow]")
        return

    console.print(f"\n[bold]Question:[/bold] {question}\n")

    # Retrieve relevant passages
    results = retrieval.search(question, top_k=5)

    if not results:
        console.print("[yellow]No relevant passages found in the wiki.[/yellow]")
        return

    # Show retrieved passages
    console.print("[dim]Retrieved passages:[/dim]")
    for i, r in enumerate(results, 1):
        score_pct = f"{r['score']:.0%}"
        console.print(f"  [{i}] {r['source_path']} — {r['section']} ({score_pct})")

    console.print()

    # Group passages by source to prevent cross-source conflation
    from collections import OrderedDict
    grouped = OrderedDict()
    for i, r in enumerate(results, 1):
        src = r["source_path"]
        if src not in grouped:
            grouped[src] = []
        grouped[src].append((i, r))

    evidence_block = ""
    for src, passages_in_src in grouped.items():
        evidence_block += f"\n=== Source: {src} ===\n"
        for i, r in passages_in_src:
            evidence_block += f"\n--- Passage {i} (Section: {r['section']}) ---\n{r['text']}\n"

    # Build prompt
    instructions = _load_instructions()
    user_prompt = f"""Evidence passages (grouped by source document — do NOT mix facts between sources):
{evidence_block}

Question: {question}

Answer the question using ONLY the evidence above. Cite each claim with [Source: filename, section]. If the evidence does not contain the answer, state that clearly."""

    # Generate answer
    console.print("[dim]Generating answer...[/dim]\n")
    try:
        answer = model.generate(instructions, user_prompt, temperature=0.2)
    except Exception as e:
        console.print(f"[red]Error generating answer: {e}[/red]")
        console.print("[yellow]Is Ollama running? Start it with: ollama serve[/yellow]")
        return

    # Display answer
    model_info = model.get_model_info()
    console.print(Panel(
        Markdown(answer),
        title="Answer",
        subtitle=f"Model: {model_info['name']} | Mode: local",
        border_style="green",
    ))

    # Save evidence card if requested
    if save_path:
        _save_evidence(save_path, question, results, answer, model_info)
        console.print(f"\n[dim]Evidence saved to: {save_path}[/dim]")


def _save_evidence(path: str, question: str, passages: list[dict], answer: str, model_info: dict):
    lines = [
        f"# Evidence Card\n",
        f"## Question\n{question}\n",
        f"## Model\n- Name: {model_info['name']}",
        f"- Parameters: {model_info['parameter_size']}",
        f"- Quantization: {model_info['quantization']}",
        f"- Mode: local\n",
        f"## Retrieved Passages\n",
    ]

    for i, p in enumerate(passages, 1):
        lines.append(f"### Passage {i}")
        lines.append(f"- Source: `{p['source_path']}`")
        lines.append(f"- Section: {p['section']}")
        lines.append(f"- Relevance: {p['score']:.0%}")
        lines.append(f"\n> {p['text'][:300]}{'...' if len(p['text']) > 300 else ''}\n")

    lines.append(f"## Answer\n{answer}\n")
    lines.append(f"## Assessment\n*[To be filled: Does the answer match the evidence? Are citations accurate?]*\n")

    Path(path).write_text("\n".join(lines), encoding="utf-8")
