import re
from pathlib import Path


def split_text_into_passages(text: str, source_path: str, max_chars: int = 1500, overlap_chars: int = 200) -> list[dict]:
    sections = _split_by_headings(text)
    passages = []
    for section_title, section_text in sections:
        chunks = _split_by_size(section_text, max_chars, overlap_chars)
        for i, chunk in enumerate(chunks):
            if chunk.strip():
                passages.append({
                    "text": chunk.strip(),
                    "source_path": source_path,
                    "section": section_title or "Main",
                    "chunk_index": i,
                })
    return passages


def _split_by_headings(text: str) -> list[tuple[str, str]]:
    heading_pattern = re.compile(r'^(#{1,3})\s+(.+)$|^([A-Z][A-Za-z\s&:,\-]+)$', re.MULTILINE)
    matches = list(heading_pattern.finditer(text))

    if not matches:
        return [("", text)]

    sections = []
    if matches[0].start() > 0:
        preamble = text[:matches[0].start()].strip()
        if preamble:
            sections.append(("", preamble))

    for i, match in enumerate(matches):
        title = match.group(2) or match.group(3)
        title = title.strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        if body:
            sections.append((title, body))

    return sections if sections else [("", text)]


def _split_by_size(text: str, max_chars: int, overlap_chars: int) -> list[str]:
    if len(text) <= max_chars:
        return [text]

    paragraphs = text.split('\n\n')
    chunks = []
    current = ""

    for para in paragraphs:
        if len(current) + len(para) + 2 > max_chars and current:
            chunks.append(current)
            overlap_text = current[-overlap_chars:] if len(current) > overlap_chars else current
            current = overlap_text + "\n\n" + para
        else:
            current = current + "\n\n" + para if current else para

    if current.strip():
        chunks.append(current)

    return chunks


def read_source_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def sanitize_filename(name: str) -> str:
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = name.strip('. ')
    return name
