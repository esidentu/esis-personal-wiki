import json
import re
from pathlib import Path

import yaml

from .model import LocalModel
from .retrieval import RetrievalSystem
from .utils import read_source_file, split_text_into_passages, sanitize_filename

CATALOG_PATH = Path("data/source_catalog.yaml")
WIKI_DIR = Path("vault/wiki")
INDEX_PATH = Path("vault/index.md")

INGEST_SYSTEM_PROMPT = """You are a wiki page generator. Given a source document, create structured wiki pages.

For each distinct topic in the source, output a JSON array of page objects. Each object must have:
- "filename": short descriptive name, 2-6 words, Title Case, e.g. "AI Energy Footprint" (no .md extension)
- "category": one of "Concepts", "Courses", "Career" — pick the best fit
- "heading": matches the filename exactly
- "summary": 2-3 sentence overview of the topic
- "details": key facts, figures, and specifics from the source as bullet points in markdown
- "source_ref": the original source filename
- "related": list of other page names this topic connects to (from this source or logically related)

Rules:
- Extract 3-6 distinct pages per source depending on content richness
- Use only facts from the source — do not invent information
- Keep filenames short and descriptive (not sentences or IDs)
- Use Title Case for filenames: "AI Energy Footprint" not "ai-energy-footprint"

Respond with ONLY a valid JSON array. No markdown fencing, no explanation."""


def load_catalog() -> dict:
    if CATALOG_PATH.exists():
        return yaml.safe_load(CATALOG_PATH.read_text(encoding="utf-8")) or {}
    return {}


def save_catalog(catalog: dict):
    CATALOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CATALOG_PATH.write_text(yaml.dump(catalog, default_flow_style=False), encoding="utf-8")


def ingest_source(source_path: Path, model: LocalModel, retrieval: RetrievalSystem, console=None) -> list[str]:
    source_name = source_path.name
    text = read_source_file(source_path)

    if not text.strip():
        if console:
            console.print(f"[yellow]Skipping empty file: {source_name}[/yellow]")
        return []

    catalog = load_catalog()

    # Index passages for retrieval
    passages = split_text_into_passages(text, source_name)
    retrieval.index_passages(passages, clear_source=source_name)
    if console:
        console.print(f"  Indexed {len(passages)} passages for retrieval")

    # Generate wiki pages via Gemma
    if console:
        console.print(f"  Generating wiki pages with Gemma...")

    truncated_text = text[:6000]
    prompt = f"Source document: {source_name}\n\nContent:\n{truncated_text}"

    try:
        response = model.generate(INGEST_SYSTEM_PROMPT, prompt, temperature=0.3)
        pages = _parse_pages_response(response)
    except Exception as e:
        if console:
            console.print(f"[red]Error generating pages: {e}[/red]")
        pages = _fallback_page(source_name, text)

    if not pages:
        pages = _fallback_page(source_name, text)

    created_pages = []
    old_pages = catalog.get(source_name, {}).get("pages", [])

    for page in pages:
        filename = sanitize_filename(page["filename"]) + ".md"
        category = page.get("category", "Concepts")
        category_dir = WIKI_DIR / category
        category_dir.mkdir(parents=True, exist_ok=True)
        filepath = category_dir / filename

        # Build markdown content
        related_links = ""
        if page.get("related"):
            links = [f"- [[{r}]]" for r in page["related"]]
            related_links = "\n## Related Notes\n" + "\n".join(links) + "\n"

        content = f"""# {page['heading']}

{page['summary']}

## Key Details

{page['details']}

## Source

- Original: `{page['source_ref']}`
{related_links}"""

        filepath.write_text(content, encoding="utf-8")
        created_pages.append(str(filepath.relative_to(Path("vault"))))
        if console:
            console.print(f"  Created: [green]{filepath.relative_to(Path('vault'))}[/green]")

    # Remove old pages that are no longer generated (re-ingestion cleanup)
    for old_page in old_pages:
        old_path = Path("vault") / old_page
        if old_path.exists() and str(old_path.relative_to(Path("vault"))) not in created_pages:
            old_path.unlink()
            if console:
                console.print(f"  Removed old page: [dim]{old_page}[/dim]")

    catalog[source_name] = {
        "pages": created_pages,
        "passage_count": len(passages),
    }
    save_catalog(catalog)

    _update_index(catalog)

    return created_pages


def _parse_pages_response(response: str) -> list[dict]:
    response = response.strip()
    # Strip markdown code fences if present
    if response.startswith("```"):
        lines = response.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        response = "\n".join(lines)

    # Find JSON array in response
    match = re.search(r'\[.*\]', response, re.DOTALL)
    if not match:
        return []

    try:
        pages = json.loads(match.group())
        valid = []
        for p in pages:
            if isinstance(p, dict) and "filename" in p and "heading" in p:
                valid.append({
                    "filename": p["filename"],
                    "category": p.get("category", "Concepts"),
                    "heading": p["heading"],
                    "summary": p.get("summary", ""),
                    "details": p.get("details", ""),
                    "source_ref": p.get("source_ref", ""),
                    "related": p.get("related", []),
                })
        return valid
    except (json.JSONDecodeError, TypeError):
        return []


def _fallback_page(source_name: str, text: str) -> list[dict]:
    stem = Path(source_name).stem
    words = stem.replace("-", " ").replace("_", " ").split()
    title = " ".join(w.capitalize() for w in words[:6])
    summary = text[:300].strip().replace("\n", " ")
    return [{
        "filename": title,
        "category": "Concepts",
        "heading": title,
        "summary": summary + "...",
        "details": text[:1000].strip(),
        "source_ref": source_name,
        "related": [],
    }]


def _update_index(catalog: dict):
    categories: dict[str, list[str]] = {}
    for source_name, info in catalog.items():
        for page_path in info.get("pages", []):
            parts = Path(page_path).parts
            if len(parts) >= 2:
                cat = parts[1]  # wiki/Category/Page.md -> Category
                page_name = Path(page_path).stem
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(page_name)

    lines = ["# Esi's Personal Wiki\n"]
    lines.append("Welcome to my personal knowledge base. Browse topics below or use the CLI to search and ask questions.\n")

    for cat in sorted(categories.keys()):
        lines.append(f"\n## {cat}\n")
        for page in sorted(categories[cat]):
            lines.append(f"- [[{page}]]")

    lines.append(f"\n\n---\n*Sources: {len(catalog)} documents indexed*\n")

    INDEX_PATH.write_text("\n".join(lines), encoding="utf-8")
