# UI Integration Guide
## Connecting User Interface to Superior Agent Brain

**Version:** 1.0
**Purpose:** Integrate web UI with Superior Agent Brain
**Related:** `docs/COMPLETE_BRAIN_ARCHITECTURE.md` § UI Communication Layer

---

## Overview

The UI is the **sensory input/output system** - how the brain communicates with humans.

```
Human Senses → AI Equivalent
├── Eyes (visual)     → Web UI, dashboard
├── Ears (audio)      → Voice interface
├── Mouth (speech)    → Text/voice responses
└── Touch (interact)  → Button clicks, API calls
```

---

## Current Implementation

### Existing Files

```
ui-module/
├── unified_chat.html           # Web chat interface
├── unified_agent_api.py        # Backend API
├── dual_agent.py               # Dual database agent
└── orchestrated_agent_api.py   # Orchestrated API
```

### Current Flow

```
User → unified_chat.html → unified_agent_api.py → dual_agent.py → Databases
```

### What's Missing

- ❌ Integration with Superior Brain
- ❌ Memory persistence across sessions
- ❌ Document context in responses
- ❌ Learning from interactions
- ❌ Similar past query suggestions

---

## Enhanced Architecture

### New Flow with Brain Integration

```
User Input (Web UI)
    ↓
unified_chat.html
    ↓ [WebSocket/HTTP]
enhanced_agent_api.py (NEW)
    ↓
SuperiorAgentBrain
    ├─→ Recall similar queries (Vector Memory)
    ├─→ Find relevant docs (Document RAG)
    ├─→ Route to specialist (Orchestrator)
    ├─→ Generate response (LLM)
    ├─→ Learn from interaction (Meta-Learner)
    └─→ Store for future (Persistent Memory)
    ↓
Response with:
├── Answer
├── Sources cited
├── Similar past queries
└── Agent used
    ↓
Display in UI
```

---

## Implementation

### Step 1: Enhanced Backend API

**File:** `ui-module/enhanced_agent_api.py`

```python
#!/usr/bin/env python3
"""
Enhanced Agent API - Superior Brain Integration
Replaces unified_agent_api.py with full brain capabilities
"""

import os
import sys
from pathlib import Path
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import json
import uvicorn

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from superior_agent_brain import SuperiorAgentBrain
from document_rag.rag_pipeline import RAGPipeline

# Initialize FastAPI
app = FastAPI(title="Enhanced Agent API", version="2.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize brain (singleton)
brain = None
rag = None

@app.on_event("startup")
async def startup():
    """Initialize brain on startup."""
    global brain, rag

    print("\n🧠 Initializing Superior Agent Brain...")

    brain = SuperiorAgentBrain(
        enable_vector_memory=True,
        enable_persistent_memory=True,
        enable_meta_learning=True,
        enable_knowledge_graph=True,
        enable_orchestration=True
    )

    # Initialize RAG
    try:
        rag = RAGPipeline()
        print("✅ Document RAG enabled")
    except Exception as e:
        print(f"⚠️  Document RAG disabled: {e}")
        rag = None

    print("✅ Brain ready for connections\n")

@app.on_event("shutdown")
async def shutdown():
    """Save session and cleanup on shutdown."""
    global brain

    if brain:
        print("\n💾 Saving session...")
        brain.save_session(summary="UI session ended")
        brain.close()
        print("✅ Brain shutdown complete\n")


# Request/Response models
class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = "default_user"
    session_id: Optional[str] = None
    use_documents: bool = True
    use_memory: bool = True


class ChatResponse(BaseModel):
    response: str
    metadata: Dict[str, Any]
    sources: Optional[List[Dict[str, Any]]] = None
    similar_queries: Optional[List[Dict[str, Any]]] = None


# API Endpoints

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Enhanced chat endpoint with full brain integration.
    """
    if not brain:
        raise HTTPException(status_code=500, detail="Brain not initialized")

    try:
        # Get query
        query = request.message
        user_id = request.user_id

        # Enhance with documents if enabled
        sources = []
        if request.use_documents and rag:
            rag_result = rag.process_query_with_rag(query)
            query = rag_result['enhanced_query']
            sources = rag_result.get('sources', [])

        # Process through brain
        result = brain.process_query(
            query=query,
            user_id=user_id,
            use_memory=request.use_memory
        )

        # Get similar past queries
        similar_queries = []
        if request.use_memory and brain.vector_memory:
            similar = brain.vector_memory.recall_similar(
                query=request.message,
                limit=3,
                min_score=0.7
            )
            similar_queries = [
                {
                    "query": s['query'],
                    "response_preview": s['response'][:100],
                    "similarity": s['score']
                }
                for s in similar
            ]

        return ChatResponse(
            response=result['response'],
            metadata=result['metadata'],
            sources=sources if request.use_documents else None,
            similar_queries=similar_queries if request.use_memory else None
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/status")
async def get_status():
    """Get brain status and statistics."""
    if not brain:
        return {"status": "not_initialized"}

    status = brain.get_brain_status()
    status['api_version'] = "2.0"
    status['features'] = {
        "vector_memory": brain.vector_memory is not None,
        "persistent_memory": brain.persistent_memory is not None,
        "meta_learning": brain.meta_learner is not None,
        "knowledge_graph": brain.knowledge_graph is not None,
        "document_rag": rag is not None,
        "orchestration": brain.orchestrator is not None
    }

    return status


@app.post("/save_session")
async def save_session(summary: Optional[str] = None):
    """Manually save current session."""
    if not brain:
        raise HTTPException(status_code=500, detail="Brain not initialized")

    brain.save_session(summary=summary or "Manual save")
    return {"status": "saved"}


@app.post("/reset_conversation")
async def reset_conversation():
    """Reset conversation (clear working memory)."""
    if not brain:
        raise HTTPException(status_code=500, detail="Brain not initialized")

    brain.reset_conversation()
    return {"status": "reset"}


@app.post("/consolidate_memory")
async def consolidate_memory():
    """Run memory consolidation (like sleep)."""
    if not brain:
        raise HTTPException(status_code=500, detail="Brain not initialized")

    results = brain.sleep(conversation_days=7, performance_days=14)
    return results


@app.get("/agents")
async def list_agents():
    """List available agents."""
    if not brain or not brain.orchestrator:
        raise HTTPException(status_code=500, detail="Orchestrator not available")

    agents = brain.orchestrator.list_agents()
    return {"agents": agents, "total": len(agents)}


@app.post("/reindex_documents")
async def reindex_documents():
    """Re-index all documents."""
    if not rag:
        raise HTTPException(status_code=500, detail="RAG not enabled")

    counts = rag.ingest_all_documents()
    return {"status": "indexed", "counts": counts}


# WebSocket for real-time chat
@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket endpoint for real-time chat."""
    await websocket.accept()

    user_id = None

    try:
        while True:
            # Receive message
            data = await websocket.receive_json()
            message = data.get('message')
            user_id = data.get('user_id', 'ws_user')

            if not message:
                continue

            # Process
            request = ChatRequest(
                message=message,
                user_id=user_id,
                use_documents=data.get('use_documents', True),
                use_memory=data.get('use_memory', True)
            )

            # Get response
            response = await chat(request)

            # Send back
            await websocket.send_json(response.dict())

    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        if user_id and brain:
            # Save session on disconnect
            brain.save_session(summary=f"WebSocket session for {user_id}")


if __name__ == "__main__":
    uvicorn.run(
        "enhanced_agent_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
```

**Cross-Ref:**
- Uses: `superior_agent_brain.py`
- Uses: `document_rag/rag_pipeline.py`
- Replaces: `ui-module/unified_agent_api.py`

---

### Step 2: Enhanced Frontend

**File:** `ui-module/enhanced_chat.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Superior Agent Brain - Chat</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .container {
            width: 90%;
            max-width: 900px;
            height: 90vh;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }

        .header h1 {
            font-size: 24px;
            margin-bottom: 5px;
        }

        .status {
            font-size: 12px;
            opacity: 0.9;
        }

        .chat-area {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            background: #f5f5f5;
        }

        .message {
            margin-bottom: 20px;
            display: flex;
            flex-direction: column;
        }

        .message.user {
            align-items: flex-end;
        }

        .message.assistant {
            align-items: flex-start;
        }

        .message-content {
            max-width: 70%;
            padding: 12px 16px;
            border-radius: 12px;
            word-wrap: break-word;
        }

        .message.user .message-content {
            background: #667eea;
            color: white;
        }

        .message.assistant .message-content {
            background: white;
            border: 1px solid #e0e0e0;
        }

        .message-metadata {
            font-size: 11px;
            color: #666;
            margin-top: 5px;
            padding: 0 5px;
        }

        .sources {
            margin-top: 10px;
            padding: 10px;
            background: #f9f9f9;
            border-left: 3px solid #667eea;
            font-size: 12px;
        }

        .sources-title {
            font-weight: bold;
            margin-bottom: 5px;
        }

        .source-item {
            margin: 3px 0;
            padding-left: 10px;
        }

        .similar-queries {
            margin-top: 10px;
            padding: 10px;
            background: #fff3cd;
            border-left: 3px solid #ffc107;
            font-size: 12px;
        }

        .input-area {
            padding: 20px;
            background: white;
            border-top: 1px solid #e0e0e0;
            display: flex;
            gap: 10px;
        }

        #messageInput {
            flex: 1;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            font-size: 14px;
            outline: none;
            transition: border 0.3s;
        }

        #messageInput:focus {
            border-color: #667eea;
        }

        #sendButton {
            padding: 12px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
            transition: transform 0.2s;
        }

        #sendButton:hover {
            transform: scale(1.05);
        }

        #sendButton:active {
            transform: scale(0.95);
        }

        .loading {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #667eea;
            animation: pulse 1s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }

        .controls {
            display: flex;
            gap: 10px;
            margin-bottom: 10px;
            font-size: 12px;
        }

        .checkbox-label {
            display: flex;
            align-items: center;
            gap: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 Superior Agent Brain</h1>
            <div class="status" id="status">Initializing...</div>
        </div>

        <div class="chat-area" id="chatArea">
            <div class="message assistant">
                <div class="message-content">
                    Hello! I'm the Superior Agent Brain. I can remember our conversations, search documents, and learn from our interactions. How can I help you today?
                </div>
            </div>
        </div>

        <div class="input-area">
            <div style="flex: 1;">
                <div class="controls">
                    <label class="checkbox-label">
                        <input type="checkbox" id="useMemory" checked>
                        <span>Use Memory</span>
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" id="useDocs" checked>
                        <span>Search Documents</span>
                    </label>
                </div>
                <input
                    type="text"
                    id="messageInput"
                    placeholder="Ask me anything..."
                    autocomplete="off"
                >
            </div>
            <button id="sendButton" onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        const API_URL = 'http://localhost:8000';
        let userId = 'user_' + Math.random().toString(36).substr(2, 9);

        // Check status on load
        async function checkStatus() {
            try {
                const response = await fetch(`${API_URL}/status`);
                const status = await response.json();

                document.getElementById('status').textContent =
                    `Ready | Session: ${status.session_id} | Memory: ${status.components.vector_memory ? '✓' : '✗'} | Docs: ${status.features.document_rag ? '✓' : '✗'}`;
            } catch (e) {
                document.getElementById('status').textContent = 'Error connecting to brain';
            }
        }

        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();

            if (!message) return;

            const useMemory = document.getElementById('useMemory').checked;
            const useDocs = document.getElementById('useDocs').checked;

            // Clear input
            input.value = '';

            // Add user message to UI
            addMessage('user', message);

            // Show loading
            const loadingId = addMessage('assistant', '<span class="loading"></span><span class="loading"></span><span class="loading"></span>');

            try {
                // Send to API
                const response = await fetch(`${API_URL}/chat`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        message: message,
                        user_id: userId,
                        use_memory: useMemory,
                        use_documents: useDocs
                    })
                });

                const data = await response.json();

                // Remove loading
                document.getElementById(loadingId).remove();

                // Add response
                addMessage('assistant', data.response, {
                    metadata: data.metadata,
                    sources: data.sources,
                    similar_queries: data.similar_queries
                });

            } catch (e) {
                document.getElementById(loadingId).remove();
                addMessage('assistant', `Error: ${e.message}`);
            }
        }

        function addMessage(role, content, extras = {}) {
            const chatArea = document.getElementById('chatArea');
            const messageId = 'msg_' + Date.now();

            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${role}`;
            messageDiv.id = messageId;

            let html = `<div class="message-content">${content}</div>`;

            // Add metadata
            if (extras.metadata) {
                const meta = extras.metadata;
                html += `<div class="message-metadata">`;
                if (meta.selected_agent) {
                    html += `Agent: ${meta.selected_agent} | `;
                }
                html += `Time: ${meta.execution_time_seconds?.toFixed(2)}s`;
                if (meta.similar_experiences_found > 0) {
                    html += ` | Found ${meta.similar_experiences_found} similar past query(ies)`;
                }
                html += `</div>`;
            }

            // Add sources
            if (extras.sources && extras.sources.length > 0) {
                html += `<div class="sources">
                    <div class="sources-title">📄 Sources:</div>`;
                extras.sources.forEach(src => {
                    html += `<div class="source-item">• ${src.title} (${(src.relevance * 100).toFixed(0)}%)</div>`;
                });
                html += `</div>`;
            }

            // Add similar queries
            if (extras.similar_queries && extras.similar_queries.length > 0) {
                html += `<div class="similar-queries">
                    <div class="sources-title">💡 Similar past queries:</div>`;
                extras.similar_queries.forEach(q => {
                    html += `<div class="source-item">• "${q.query}" (${(q.similarity * 100).toFixed(0)}% similar)</div>`;
                });
                html += `</div>`;
            }

            messageDiv.innerHTML = html;
            chatArea.appendChild(messageDiv);

            // Scroll to bottom
            chatArea.scrollTop = chatArea.scrollHeight;

            return messageId;
        }

        // Enter to send
        document.getElementById('messageInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });

        // Check status on load
        checkStatus();
        setInterval(checkStatus, 30000); // Update every 30s
    </script>
</body>
</html>
```

**Features:**
- ✅ Memory toggle
- ✅ Document search toggle
- ✅ Shows sources
- ✅ Shows similar past queries
- ✅ Shows agent used
- ✅ Execution time display

**Cross-Ref:**
- Calls: `enhanced_agent_api.py`
- Replaces: `ui-module/unified_chat.html`

---

## Deployment

### Local Development

```bash
# Terminal 1: Start Qdrant
docker run -d -p 6333:6333 qdrant/qdrant

# Terminal 2: Start API
cd ui-module
python enhanced_agent_api.py

# Terminal 3: Serve Frontend
python -m http.server 8080

# Open browser
open http://localhost:8080/enhanced_chat.html
```

### Production Deployment

See `ui-module/HOSTINGER_DEPLOYMENT.md` for production setup.

---

## Features Comparison

| Feature | Old UI | Enhanced UI |
|---------|--------|-------------|
| **Chat** | ✅ | ✅ |
| **Database Query** | ✅ | ✅ |
| **Memory Recall** | ❌ | ✅ |
| **Document Search** | ❌ | ✅ |
| **Source Citations** | ❌ | ✅ |
| **Similar Queries** | ❌ | ✅ |
| **Agent Routing** | ❌ | ✅ |
| **Learning** | ❌ | ✅ |
| **Session Persistence** | ❌ | ✅ |

---

## API Endpoints Reference

```
POST /chat
    - Main chat endpoint
    - Request: { message, user_id, use_memory, use_documents }
    - Response: { response, metadata, sources, similar_queries }

GET /status
    - Get brain status
    - Response: { session_id, components, features, stats }

POST /save_session
    - Manually save session
    - Request: { summary }

POST /reset_conversation
    - Clear working memory

POST /consolidate_memory
    - Run memory consolidation

GET /agents
    - List available agents

POST /reindex_documents
    - Re-index all documents

WebSocket /ws/chat
    - Real-time chat
    - Send: { message, user_id, use_memory, use_documents }
    - Receive: { response, metadata, sources, similar_queries }
```

---

## Next Steps

1. **Test Locally**: Run enhanced API and test features
2. **Migrate Data**: Move from old UI to new
3. **Deploy**: Push to production
4. **Monitor**: Track usage and performance
5. **Iterate**: Add features based on feedback

---

**Status:** Implementation Ready
**Related:** `docs/COMPLETE_BRAIN_ARCHITECTURE.md`, `superior_agent_brain.py`
**Next:** Deploy and test enhanced UI
