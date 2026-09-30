# Esi's Personal Wiki CLI

A personal knowledge base CLI powered by local Gemma via Ollama with RAG (Retrieval Augmented Generation). Built as a standalone harness that manages chat, ask, and search modes — all working offline after initial setup.

## Purpose and Sources

This wiki organizes personal knowledge from MBA coursework, career experience, and AI research into a browsable, searchable knowledge base. The CLI uses a local language model to generate wiki pages, answer questions with citations, and provide a conversational assistant.

**Sources (4 documents):**

| Source | Description |
|--------|-------------|
| `AI & Sustainability.txt` | Academic paper on the AI sustainability paradox — energy, water, agriculture, smart cities |
| `CLAUDIA ESI DENTU RESUME.txt` | Professional background — product management at MTN & Telecel, Berkeley Haas MBA |
| `Data and Decisions Syllabus.txt` | FTMBA 200S statistics course — sampling, regression, ML, AI policy |
| `FTMBA 201A Economic Analysis Syllabus.txt` | Microeconomics course — costs, pricing, game theory, oligopoly |

Original sources are preserved unchanged in `vault/raw/`. Generated wiki pages live in `vault/wiki/` with short descriptive filenames, matching headings, source references, and internal links.

## Device Specs

| Spec | Value |
|------|-------|
| OS | Windows 11 Pro |
| CPU | AMD Ryzen 7 PRO 7840U |
| RAM | 14.7 GB total |
| GPU | AMD Radeon 780M (integrated, shares system RAM) |
| Free Disk | ~352 GB |

## Setup

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) for Windows
- [Obsidian](https://obsidian.md) (for browsing the wiki)

### 1. Install Ollama and Pull Gemma

```bash
# Download and install Ollama from https://ollama.com
# Then pull the model:
ollama pull gemma3:4b
```

### 2. Create Python Environment

```bash
cd "Esi's Wiki"
python -m venv .venv

# Windows:
.venv\Scripts\activate

# Install dependencies:
pip install -r requirements.txt
```

### 3. Download Embedding Model (while online)

ChromaDB uses its built-in ONNX embedding model (all-MiniLM-L6-v2) which downloads automatically on first use (~80 MB). Run a quick test to cache it:

```bash
python -c "import chromadb; c = chromadb.Client(); col = c.get_or_create_collection('test'); col.add(ids=['1'], documents=['test']); print('Embedding model cached.')"
```

Confirm the model is downloaded before going offline.

### 4. Verify Setup

```bash
# Check Ollama is running:
ollama list

# Test the CLI:
python wiki.py --help
```

## Model Choice

| Setting | Value |
|---------|-------|
| Model | Gemma 3 4B Instruct (gemma3:4b) |
| Quantization | Q4_0 (~4.5 GB) |
| Runtime | Ollama |
| Embedding | all-MiniLM-L6-v2 (ChromaDB built-in ONNX, ~80 MB) |
| Vector Store | ChromaDB (persistent, local) |

**Why Gemma 3 4B?** With 14.7 GB total RAM on an integrated AMD APU, the 4B model (~4.5 GB at Q4) leaves sufficient headroom for the OS, runtime, embedding model, and ChromaDB. It provides better response quality than the 1B model while staying within memory limits. The 26B MoE model requires ~14.4 GB at Q4 which would exceed available memory.

**Measured performance:** Ingestion of 4 sources (82 passages, 21 wiki pages) takes ~3-5 minutes. Ask-mode queries return answers in ~5-10 seconds. Search mode is near-instant (no LLM). Chat mode responses take ~5-15 seconds depending on whether retrieval is triggered.

## CLI Commands

```bash
# Ingest sources and generate wiki pages:
python wiki.py ingest ./vault/raw

# Search for passages (no LLM needed):
python wiki.py search "pricing strategy"

# Ask a factual question with citations:
python wiki.py ask "What is the AI policy for MBA courses?"

# Save evidence card:
python wiki.py ask "How is the Economic Analysis course graded?" --save data/evidence/test2.md

# Start interactive chat:
python wiki.py chat

# Show help:
python wiki.py --help
```

## Architecture

```
User Command
    │
    ▼
┌─────────────────────────────────────────────────┐
│  CLI (wiki.py)                                  │
│  Parses command, selects mode                   │
└──────────┬──────────┬──────────┬────────────────┘
           │          │          │
     ┌─────▼──┐  ┌────▼───┐  ┌──▼─────┐
     │  Chat  │  │  Ask   │  │ Search │
     │  Mode  │  │  Mode  │  │  Mode  │
     └───┬────┘  └───┬────┘  └───┬────┘
         │           │           │
         ▼           ▼           ▼
┌─────────────┐ ┌─────────┐ ┌──────────────┐
│ Personality │ │ Research│ │ Passages     │
│ + Context   │ │ Rules   │ │ Only         │
│ + Optional  │ │ + RAG   │ │ (No LLM)     │
│   Retrieval │ │ Always  │ │              │
└──────┬──────┘ └────┬────┘ └──────┬───────┘
       │             │             │
       ▼             ▼             │
┌──────────────────────────┐       │
│  Model (harness/model.py)│       │
│  Ollama → Gemma 3 4B     │       │
└──────────────────────────┘       │
       │             │             │
       ▼             ▼             ▼
┌──────────────────────────────────────┐
│  Retrieval (harness/retrieval.py)    │
│  ChromaDB (ONNX embeddings)         │
└──────────────────────────────────────┘
```

### How It Works

1. **Mode selection:** The CLI (`wiki.py`) parses the user's command and routes to the appropriate mode handler.

2. **Chat mode** loads personality from `config/persona.md`, maintains conversation history in memory, and retrieves wiki passages only when the message references wiki topics (detected via keyword matching). Follow-ups like "make that shorter" use conversation context. Citations are added for claims from notes; suggestions are labeled as such.

3. **Ask mode** loads research rules from `config/wiki-instructions.md`. Each question is standalone (no chat history). It always retrieves the top-5 passages, builds a prompt with evidence, and generates a neutral answer with citations. If evidence is insufficient, it says so.

4. **Search mode** queries ChromaDB directly and displays matching passages with source paths and relevance scores. No model generation — works without Ollama running.

5. **Ingestion** reads source files from `vault/raw/`, splits text into ~1500-character passages with overlap, indexes them in ChromaDB, then sends source text to Gemma to generate wiki pages. Pages get short descriptive filenames, matching headings, source references, and related-note links. A source catalog (`data/source_catalog.yaml`) tracks what was generated, preventing duplicates on re-ingestion.

### Design Choices

| Choice | Decision | Rationale |
|--------|----------|-----------|
| Passage size | ~1500 chars, 200 overlap | Balances context richness with retrieval precision |
| Retrieval top-k | 5 passages | Enough context for multi-source answers without overwhelming the model |
| Chat retrieval | Keyword-triggered | Avoids unnecessary lookups for casual conversation |
| Chat history | Last 20 messages | Keeps context manageable for the 4B model's window |
| Wiki filenames | 2-6 word Title Case | Readable in Obsidian graph and file list |
| Instructions | Separate files | `persona.md` for chat, `wiki-instructions.md` for ask — keeps modes distinct |
| Index structure | `vault/index.md` | Topic-organized landing page with wiki links |
| Chunks storage | `data/chroma/` outside vault | Keeps retrieval artifacts out of Obsidian |

## Evidence

### Ask-Mode Test Questions

| Test | Question | Expected Source | Evidence Card |
|------|----------|-----------------|---------------|
| 1 | "What is the estimated global data-center electricity demand by 2030?" | AI & Sustainability.txt | [test1.md](data/evidence/test1.md) |
| 2 | "How is the Economic Analysis course graded?" | FTMBA 201A Syllabus | [test2.md](data/evidence/test2.md) |
| 3 | "What is the AI usage policy for MBA courses at Berkeley Haas?" | Both syllabi | [test3.md](data/evidence/test3.md) |
| 4 | "What is Esi's GPA at Berkeley Haas?" | None (unsupported) | [test4.md](data/evidence/test4.md) |

### Mode Checks

- [Chat mode check](data/evidence/chat_check.md) — "what can you help me with?" + follow-up draft
- [Search mode check](data/evidence/search_check.md) — search "pricing" for raw passages

### Offline Demonstration

All components run locally after initial setup. The system requires no internet connection once Ollama and the embedding model are cached:

- **Ollama + Gemma 3 4B:** Runs entirely on local CPU/GPU, no API calls
- **ChromaDB + ONNX embeddings:** Embedding model cached locally (~80 MB), vector store persisted to `data/chroma/`
- **Search mode:** Works without even Ollama running (queries ChromaDB directly)

To verify: disconnect from the internet, then run `python wiki.py search "pricing"` and `python wiki.py ask "What is the AI policy?"` — both produce results without network access.

## Obsidian Screenshots

To view the wiki in Obsidian:

1. Open Obsidian and select "Open folder as vault" → choose the `vault/` directory
2. Browse `index.md` for topic-organized navigation
3. Open any wiki page to see source references and `[[related note]]` links
4. Use Graph View (filter: `path:wiki/`) to see readable labels and connections

## Reflection

### Limitation

The 4B model struggles with **cross-source evidence conflation**. In Test 2, the model was asked about Economic Analysis grading and returned the Data & Decisions grading breakdown (10%/50%/40%) while citing the Economic Analysis syllabus. When multiple sources appear in the retrieved passages, the small model sometimes mixes facts between them rather than correctly attributing each detail to its source. This also appeared in Test 3, where the model answered using only one syllabus's AI policy instead of synthesizing both. The limited parameter count means the model cannot always distinguish which passage each fact came from when multiple sources are interleaved in the prompt.

### Proposed Improvement

**Source-separated prompting:** Instead of presenting all retrieved passages in a single block, group them by source document and label each group clearly (e.g., "=== Source: FTMBA 201A ==="). This structural separation in the prompt would help the 4B model maintain source boundaries when generating answers. Additionally, a **re-ranking step** using a lightweight cross-encoder could score passage-question relevance more precisely than cosine similarity alone, filtering out marginally relevant passages from unrelated sources before they reach the model.

## Project Structure

```
Esi's Wiki/
├── wiki.py                    # CLI entry point
├── harness/
│   ├── __init__.py
│   ├── model.py               # Ollama interface
│   ├── retrieval.py           # Embedding + vector search
│   ├── chat_mode.py           # Chat mode logic
│   ├── ask_mode.py            # Ask mode logic
│   ├── search_mode.py         # Search mode logic
│   ├── ingest.py              # Ingestion pipeline
│   └── utils.py               # Text splitting utilities
├── config/
│   ├── persona.md             # Chat personality
│   └── wiki-instructions.md   # Research rules
├── vault/                     # Obsidian vault root
│   ├── raw/                   # Original sources (unchanged)
│   ├── wiki/                  # Generated wiki pages
│   │   ├── Concepts/
│   │   ├── Courses/
│   │   └── Career/
│   └── index.md               # Landing page
├── data/
│   ├── chroma/                # Vector store (gitignored)
│   ├── source_catalog.yaml    # Source → page mapping
│   └── evidence/              # Test results
├── requirements.txt
└── README.md
```
