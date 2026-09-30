import chromadb

COLLECTION_NAME = "wiki_passages"


class RetrievalSystem:
    def __init__(self, chroma_dir: str = "data/chroma"):
        self._chroma_client = chromadb.PersistentClient(path=chroma_dir)
        self._collection = self._chroma_client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )

    def index_passages(self, passages: list[dict], clear_source: str | None = None):
        if clear_source:
            existing = self._collection.get(where={"source_path": clear_source})
            if existing["ids"]:
                self._collection.delete(ids=existing["ids"])

        if not passages:
            return

        texts = [p["text"] for p in passages]
        ids = [f"{p['source_path']}::{i}::{p['section']}::{p['chunk_index']}" for i, p in enumerate(passages)]
        metadatas = [
            {"source_path": p["source_path"], "section": p["section"], "chunk_index": p["chunk_index"]}
            for p in passages
        ]

        batch_size = 100
        for i in range(0, len(ids), batch_size):
            end = min(i + batch_size, len(ids))
            self._collection.add(
                ids=ids[i:end],
                documents=texts[i:end],
                metadatas=metadatas[i:end],
            )

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        if self._collection.count() == 0:
            return []

        results = self._collection.query(
            query_texts=[query],
            n_results=min(top_k, self._collection.count()),
        )

        passages = []
        for i in range(len(results["ids"][0])):
            passages.append({
                "text": results["documents"][0][i],
                "source_path": results["metadatas"][0][i]["source_path"],
                "section": results["metadatas"][0][i]["section"],
                "score": 1 - results["distances"][0][i],
            })
        return passages

    def count(self) -> int:
        return self._collection.count()

    def clear_all(self):
        self._chroma_client.delete_collection(COLLECTION_NAME)
        self._collection = self._chroma_client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
