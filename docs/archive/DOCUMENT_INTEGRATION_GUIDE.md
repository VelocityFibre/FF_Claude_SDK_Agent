# Document Integration Guide
## RAG (Retrieval-Augmented Generation) for AI Brain

**Version:** 1.0
**Purpose:** Integrate document systems with Superior Agent Brain
**Related:** `docs/COMPLETE_BRAIN_ARCHITECTURE.md` § Document System

---

## Overview

Documents are the **external knowledge base** for the AI brain - like books and references that can be read and recalled when needed.

### What This Enables

```
WITHOUT Documents                    WITH Documents
├── Agent: Limited to training       ├── Agent: Knows project-specific info
├── Answers: Generic                 ├── Answers: Contextual & specific
├── Citations: None                  ├── Citations: Links to source docs
└── Knowledge: Static                └── Knowledge: Updated with docs
```

---

## Architecture

### Document Flow

```
[Documents] → [Ingestion] → [Embeddings] → [Storage] → [Retrieval] → [Context] → [Response]
    │             │              │              │            │            │           │
SharePoint    Parse &        Create         Qdrant +     Semantic     Enhanced    Generated
Local Files   Extract       Vectors          Neon        Search       Prompt      with Citations
Web Docs      Metadata      Index
```

### Components

```
document_rag/
├── document_ingestion.py       # Read and parse documents
├── document_embeddings.py      # Create vector embeddings
├── document_search.py          # Semantic search
├── document_organizer.py       # Categorization & indexing
└── rag_pipeline.py            # Complete RAG flow
```

---

## Implementation

### Step 1: Document Ingestion

**File:** `document_rag/document_ingestion.py`

```python
#!/usr/bin/env python3
"""
Document Ingestion - Read and parse documents from various sources
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime


class DocumentIngestion:
    """
    Handles document ingestion from multiple sources.
    """

    def __init__(self):
        self.supported_formats = ['.md', '.txt', '.pdf', '.json', '.py', '.js', '.ts']

    def ingest_local_files(
        self,
        directory: str,
        file_pattern: str = "*",
        recursive: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Ingest documents from local directory.

        Returns:
            List of document objects with content and metadata
        """
        documents = []
        path = Path(directory)

        if recursive:
            files = path.rglob(file_pattern)
        else:
            files = path.glob(file_pattern)

        for file_path in files:
            if file_path.suffix in self.supported_formats:
                doc = self._read_file(file_path)
                if doc:
                    documents.append(doc)

        return documents

    def ingest_sharepoint(
        self,
        sharepoint_json: str = "sharepoint_sheets.json"
    ) -> List[Dict[str, Any]]:
        """
        Ingest documents from SharePoint export.
        """
        documents = []

        if os.path.exists(sharepoint_json):
            with open(sharepoint_json) as f:
                data = json.load(f)

            for item in data:
                doc = {
                    "id": item.get("id"),
                    "title": item.get("name"),
                    "content": json.dumps(item),  # Or parse structure
                    "source": "sharepoint",
                    "source_url": item.get("webUrl"),
                    "created_at": item.get("createdDateTime"),
                    "modified_at": item.get("lastModifiedDateTime"),
                    "metadata": {
                        "type": "sharepoint_sheet",
                        "parent": item.get("parentReference", {}).get("path")
                    }
                }
                documents.append(doc)

        return documents

    def ingest_markdown_docs(
        self,
        directory: str = "docs"
    ) -> List[Dict[str, Any]]:
        """
        Ingest markdown documentation files.
        """
        return self.ingest_local_files(
            directory=directory,
            file_pattern="*.md",
            recursive=True
        )

    def _read_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Read a single file and extract metadata."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            return {
                "id": str(file_path),
                "title": file_path.stem,
                "content": content,
                "source": "local_file",
                "source_path": str(file_path),
                "file_type": file_path.suffix,
                "size": file_path.stat().st_size,
                "created_at": datetime.fromtimestamp(file_path.stat().st_ctime).isoformat(),
                "modified_at": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                "metadata": {
                    "extension": file_path.suffix,
                    "parent_dir": str(file_path.parent)
                }
            }
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None

    def chunk_document(
        self,
        document: Dict[str, Any],
        chunk_size: int = 1000,
        overlap: int = 200
    ) -> List[Dict[str, Any]]:
        """
        Split large documents into chunks for better retrieval.

        Args:
            document: Document to chunk
            chunk_size: Characters per chunk
            overlap: Overlap between chunks

        Returns:
            List of document chunks
        """
        content = document['content']
        chunks = []

        for i in range(0, len(content), chunk_size - overlap):
            chunk_content = content[i:i + chunk_size]

            chunk = {
                **document,
                "content": chunk_content,
                "chunk_index": len(chunks),
                "chunk_total": -1,  # Set after loop
                "chunk_start": i,
                "chunk_end": min(i + chunk_size, len(content))
            }
            chunks.append(chunk)

        # Update total
        for chunk in chunks:
            chunk['chunk_total'] = len(chunks)

        return chunks


# Usage example
if __name__ == "__main__":
    ingestion = DocumentIngestion()

    # Ingest all markdown docs
    docs = ingestion.ingest_markdown_docs("docs")
    print(f"Ingested {len(docs)} markdown documents")

    # Ingest SharePoint
    sp_docs = ingestion.ingest_sharepoint()
    print(f"Ingested {len(sp_docs)} SharePoint documents")

    # Chunk large documents
    for doc in docs:
        if len(doc['content']) > 2000:
            chunks = ingestion.chunk_document(doc)
            print(f"Split '{doc['title']}' into {len(chunks)} chunks")
```

**Cross-Ref:** Used by `rag_pipeline.py`

---

### Step 2: Document Embeddings

**File:** `document_rag/document_embeddings.py`

```python
#!/usr/bin/env python3
"""
Document Embeddings - Create and store vector embeddings
"""

from typing import List, Dict, Any
from memory.vector_memory import VectorMemory, EmbeddingService


class DocumentEmbeddings:
    """
    Creates and manages document embeddings.
    """

    def __init__(self, collection_name: str = "document_embeddings"):
        self.vector_memory = VectorMemory(collection_name=collection_name)
        self.embedder = EmbeddingService(provider="simple")  # Use "voyage" or "openai" in production

    def embed_documents(
        self,
        documents: List[Dict[str, Any]]
    ) -> int:
        """
        Create embeddings for documents and store in Qdrant.

        Args:
            documents: List of document objects

        Returns:
            Number of documents embedded
        """
        count = 0

        for doc in documents:
            # Store in vector memory
            self.vector_memory.store_interaction(
                query=doc['title'],
                response=doc['content'],
                agent_id="document_system",
                metadata={
                    "doc_id": doc['id'],
                    "source": doc['source'],
                    "source_path": doc.get('source_path', ''),
                    "file_type": doc.get('file_type', ''),
                    "created_at": doc.get('created_at', ''),
                    **doc.get('metadata', {})
                },
                success=True
            )
            count += 1

        return count

    def search_documents(
        self,
        query: str,
        limit: int = 5,
        source_filter: str = None
    ) -> List[Dict[str, Any]]:
        """
        Search for documents similar to query.

        Args:
            query: Search query
            limit: Max results
            source_filter: Filter by source type

        Returns:
            Similar documents with scores
        """
        results = self.vector_memory.recall_similar(
            query=query,
            limit=limit,
            min_score=0.5
        )

        # Filter by source if specified
        if source_filter:
            results = [
                r for r in results
                if r.get('metadata', {}).get('source') == source_filter
            ]

        return results


# Usage
if __name__ == "__main__":
    embedder = DocumentEmbeddings()

    # Embed sample documents
    docs = [
        {
            "id": "doc1",
            "title": "Setup Guide",
            "content": "Follow these steps to set up the system...",
            "source": "local_file",
            "source_path": "docs/SETUP.md"
        }
    ]

    count = embedder.embed_documents(docs)
    print(f"Embedded {count} documents")

    # Search
    results = embedder.search_documents("how to install", limit=3)
    for r in results:
        print(f"Found: {r['query']} (score: {r['score']:.2f})")
```

**Cross-Ref:**
- Uses: `memory/vector_memory.py`
- Used by: `rag_pipeline.py`

---

### Step 3: Document Search

**File:** `document_rag/document_search.py`

```python
#!/usr/bin/env python3
"""
Document Search - Semantic search with ranking
"""

from typing import List, Dict, Any
from document_embeddings import DocumentEmbeddings


class DocumentSearch:
    """
    Advanced document search with ranking and filtering.
    """

    def __init__(self):
        self.embedder = DocumentEmbeddings()

    def search(
        self,
        query: str,
        top_k: int = 5,
        filters: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Search documents with optional filters.

        Args:
            query: Search query
            top_k: Number of results
            filters: Optional filters (source, file_type, etc.)

        Returns:
            Ranked document results
        """
        # Get raw results
        results = self.embedder.search_documents(
            query=query,
            limit=top_k * 2  # Get more, then filter/rank
        )

        # Apply filters
        if filters:
            results = self._apply_filters(results, filters)

        # Rank results
        ranked = self._rank_results(results, query)

        return ranked[:top_k]

    def _apply_filters(
        self,
        results: List[Dict],
        filters: Dict[str, Any]
    ) -> List[Dict]:
        """Apply filters to results."""
        filtered = results

        if 'source' in filters:
            filtered = [
                r for r in filtered
                if r.get('metadata', {}).get('source') == filters['source']
            ]

        if 'file_type' in filters:
            filtered = [
                r for r in filtered
                if r.get('metadata', {}).get('file_type') == filters['file_type']
            ]

        return filtered

    def _rank_results(
        self,
        results: List[Dict],
        query: str
    ) -> List[Dict]:
        """
        Re-rank results based on multiple factors.

        Factors:
        - Semantic similarity (score)
        - Recency (newer = better)
        - Document type priority
        """
        # Simple ranking: already sorted by score
        # Can add more sophisticated ranking here
        return sorted(results, key=lambda x: x['score'], reverse=True)

    def get_context_for_query(
        self,
        query: str,
        max_tokens: int = 4000
    ) -> str:
        """
        Get formatted context from top documents.

        Args:
            query: User query
            max_tokens: Max context length

        Returns:
            Formatted context string
        """
        results = self.search(query, top_k=5)

        context = "## Relevant Documentation:\n\n"
        total_chars = 0
        max_chars = max_tokens * 4  # Rough estimate

        for i, doc in enumerate(results, 1):
            doc_text = f"### Document {i}: {doc['query']}\n"
            doc_text += f"**Source:** {doc.get('metadata', {}).get('source_path', 'Unknown')}\n"
            doc_text += f"**Relevance:** {doc['score']:.1%}\n\n"
            doc_text += f"{doc['response'][:500]}...\n\n"

            if total_chars + len(doc_text) > max_chars:
                break

            context += doc_text
            total_chars += len(doc_text)

        return context


# Usage
if __name__ == "__main__":
    search = DocumentSearch()

    # Search
    results = search.search("how to set up Qdrant", top_k=3)

    for i, doc in enumerate(results, 1):
        print(f"{i}. {doc['query']} (score: {doc['score']:.2f})")
        print(f"   Source: {doc.get('metadata', {}).get('source_path')}\n")

    # Get context
    context = search.get_context_for_query("deployment steps")
    print(f"\nContext length: {len(context)} characters")
```

**Cross-Ref:**
- Uses: `document_embeddings.py`
- Used by: `rag_pipeline.py`, `superior_agent_brain.py`

---

### Step 4: Complete RAG Pipeline

**File:** `document_rag/rag_pipeline.py`

```python
#!/usr/bin/env python3
"""
RAG Pipeline - Complete Retrieval-Augmented Generation flow
"""

from typing import Dict, Any, List
from document_ingestion import DocumentIngestion
from document_embeddings import DocumentEmbeddings
from document_search import DocumentSearch


class RAGPipeline:
    """
    Complete RAG pipeline for document-enhanced responses.
    """

    def __init__(self):
        self.ingestion = DocumentIngestion()
        self.embedder = DocumentEmbeddings()
        self.search = DocumentSearch()

    def ingest_all_documents(self) -> Dict[str, int]:
        """
        Ingest all available documents.

        Returns:
            Count of documents by source
        """
        counts = {}

        # Ingest markdown docs
        md_docs = self.ingestion.ingest_markdown_docs("docs")
        self.embedder.embed_documents(md_docs)
        counts['markdown'] = len(md_docs)

        # Ingest SharePoint
        sp_docs = self.ingestion.ingest_sharepoint()
        self.embedder.embed_documents(sp_docs)
        counts['sharepoint'] = len(sp_docs)

        # Ingest project files
        project_docs = self.ingestion.ingest_local_files(
            directory=".",
            file_pattern="*.md",
            recursive=False
        )
        self.embedder.embed_documents(project_docs)
        counts['project'] = len(project_docs)

        return counts

    def enhance_query_with_context(
        self,
        query: str,
        max_context_tokens: int = 4000
    ) -> str:
        """
        Enhance a query with relevant document context.

        Args:
            query: User's query
            max_context_tokens: Max context length

        Returns:
            Enhanced query with document context
        """
        # Search for relevant docs
        context = self.search.get_context_for_query(
            query=query,
            max_tokens=max_context_tokens
        )

        # Build enhanced query
        enhanced = f"{context}\n\n---\n\n**User Query:** {query}"

        return enhanced

    def process_query_with_rag(
        self,
        query: str,
        include_sources: bool = True
    ) -> Dict[str, Any]:
        """
        Process query with RAG pipeline.

        Args:
            query: User query
            include_sources: Whether to include source citations

        Returns:
            Enhanced query and metadata
        """
        # Get relevant documents
        docs = self.search.search(query, top_k=5)

        # Build context
        context = self.search.get_context_for_query(query)

        # Enhanced query
        enhanced_query = f"{context}\n\n---\n\n**User Query:** {query}"

        result = {
            "original_query": query,
            "enhanced_query": enhanced_query,
            "documents_found": len(docs),
            "sources": []
        }

        if include_sources:
            result["sources"] = [
                {
                    "title": doc['query'],
                    "path": doc.get('metadata', {}).get('source_path'),
                    "relevance": doc['score'],
                    "excerpt": doc['response'][:200]
                }
                for doc in docs
            ]

        return result


# Usage
if __name__ == "__main__":
    rag = RAGPipeline()

    # Ingest all documents
    print("Ingesting documents...")
    counts = rag.ingest_all_documents()
    print(f"Ingested: {counts}")

    # Process query with RAG
    print("\nProcessing query...")
    result = rag.process_query_with_rag("How do I set up the Superior Brain?")

    print(f"\nFound {result['documents_found']} relevant documents")
    print("\nSources:")
    for src in result['sources']:
        print(f"  - {src['title']} ({src['relevance']:.1%})")
```

**Cross-Ref:**
- Uses: All other `document_rag/*` files
- Used by: `superior_agent_brain.py`

---

## Integration with Superior Brain

### Modify `superior_agent_brain.py`

```python
# Add to imports
from document_rag.rag_pipeline import RAGPipeline

# Add to __init__
class SuperiorAgentBrain:
    def __init__(self, ...):
        # ... existing init ...

        # Document RAG system
        self.rag = None
        if enable_document_rag:
            try:
                self.rag = RAGPipeline()
                print(f"✅ Document RAG: Enabled")
            except Exception as e:
                print(f"⚠️  Document RAG: Disabled ({e})")

    # Modify process_query
    def process_query(self, query: str, ...):
        # ... existing code ...

        # ENHANCE with documents
        if self.rag:
            rag_result = self.rag.process_query_with_rag(query)
            enhanced_query = rag_result['enhanced_query']

            # Add sources to metadata
            sources = rag_result.get('sources', [])
        else:
            enhanced_query = query
            sources = []

        # Use enhanced_query instead of query for LLM
        # ...
```

---

## Usage Patterns

### Pattern 1: Initial Document Load

```python
from document_rag.rag_pipeline import RAGPipeline

rag = RAGPipeline()

# One-time ingestion
counts = rag.ingest_all_documents()
print(f"Ingested {sum(counts.values())} documents")
```

### Pattern 2: Query Enhancement

```python
# User asks question
user_query = "How do I deploy to Hostinger?"

# Enhance with documents
result = rag.process_query_with_rag(user_query)

# Pass enhanced query to LLM
response = brain.chat(result['enhanced_query'])

# Show sources to user
print("\nSources:")
for src in result['sources']:
    print(f"- {src['title']}")
```

### Pattern 3: Continuous Updates

```python
# Watch for new documents
import time
from watchdog.observers import Observer

def on_new_document(file_path):
    docs = ingestion.ingest_local_files(directory=file_path)
    embedder.embed_documents(docs)
    print(f"Indexed new document: {file_path}")

# Set up file watcher
observer = Observer()
observer.schedule(handler, path="docs", recursive=True)
observer.start()
```

---

## Maintenance

### Re-indexing Documents

```bash
# Re-index all documents
python -c "
from document_rag.rag_pipeline import RAGPipeline

rag = RAGPipeline()
counts = rag.ingest_all_documents()
print(f'Re-indexed {sum(counts.values())} documents')
"
```

### Document Statistics

```python
from memory.vector_memory import VectorMemory

memory = VectorMemory(collection_name="document_embeddings")
stats = memory.get_stats()

print(f"Total documents: {stats['total_memories']}")
```

---

## Best Practices

1. **Chunk Large Documents**: Split docs >2KB for better retrieval
2. **Update Regularly**: Re-index when docs change
3. **Use Filters**: Filter by source/type for precision
4. **Monitor Performance**: Track search latency
5. **Cite Sources**: Always show users where info came from

---

**Status:** Implementation Ready
**Next:** Create `document_rag/` directory and implement files above
**Related:** `docs/COMPLETE_BRAIN_ARCHITECTURE.md`, `docs/MASTER_INDEX.md`
