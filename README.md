# Quant Research Intelligence System

> A multimodal, evidence-grounded quantitative research intelligence system combining structured research-paper ingestion, production chunking, dense and lexical retrieval, hybrid ranking, cross-encoder reranking, knowledge-graph context expansion, grounded RAG, research synthesis, quantitative factor extraction, citation traceability, and systematic evaluation.

## Overview

The **Quant Research Intelligence System** is an end-to-end research platform designed to retrieve, reason over, synthesize, and evaluate information from quantitative-finance research papers.

The central design principle is:

> **Every research insight should remain traceable to the underlying document, page, section, and evidence chunk from which it was derived.**

Instead of flattening research papers into plain text, the system preserves multiple evidence modalities:

- Text
- Tables
- Figures
- Mathematical formulas
- Document and page metadata
- Section hierarchy
- Chunk relationships
- Evidence provenance

The resulting pipeline combines traditional information retrieval with semantic retrieval, lexical retrieval, reranking, graph-aware context expansion, grounded LLM generation, structured research synthesis, and evaluation.

---

## System Architecture

```text
                         QUANT RESEARCH PAPERS
                                  |
                                  v
                    +--------------------------+
                    | Multimodal Ingestion     |
                    | Text / Tables / Figures |
                    | Formulas / Metadata     |
                    +------------+-------------+
                                 |
                                 v
                    +--------------------------+
                    | Production Chunking      |
                    | Semantic Chunks           |
                    | Formula Evidence          |
                    | Table Evidence            |
                    | Figure Evidence           |
                    +------------+-------------+
                                 |
                                 v
                    +--------------------------+
                    | Embedding Generation      |
                    | BAAI/bge-small-en-v1.5   |
                    | 384-dimensional vectors  |
                    +------------+-------------+
                                 |
                  +--------------+--------------+
                  |                             |
                  v                             v
        +-------------------+        +------------------+
        | Dense Retrieval   |        | Lexical Retrieval|
        | FAISS             |        | BM25             |
        +---------+---------+        +--------+---------+
                  |                           |
                  +-------------+-------------+
                                |
                                v
                    +--------------------------+
                    | Hybrid Retrieval         |
                    | Reciprocal Rank Fusion   |
                    +------------+-------------+
                                 |
                                 v
                    +--------------------------+
                    | Cross-Encoder Reranking  |
                    | BAAI/bge-reranker-base   |
                    +------------+-------------+
                                 |
                                 v
                    +--------------------------+
                    | Knowledge Graph           |
                    | Graph-aware Context       |
                    | Expansion                 |
                    +------------+-------------+
                                 |
                                 v
                    +--------------------------+
                    | Grounded RAG              |
                    | Guardrails + Citations    |
                    +------------+-------------+
                                 |
                                 v
                    +--------------------------+
                    | Research Synthesis        |
                    | Findings / Factors        |
                    | Relationships / Limits    |
                    +------------+-------------+
                                 |
                                 v
                    +--------------------------+
                    | Evaluation Framework      |
                    +------------+-------------+
                                 |
                                 v
                    +--------------------------+
                    | Streamlit Research UI    |
                    +--------------------------+
```

---

## Key Objectives

### 1. Multimodal research evidence

Important quantitative information does not always exist in normal paragraphs. It can appear inside:

- Tables
- Figures
- Mathematical formulas
- Captions
- Structured sections

The ingestion pipeline preserves these elements rather than flattening everything into plain text.

### 2. Precision retrieval

Quantitative research queries frequently contain:

- Specialized terminology
- Financial concepts
- Mathematical expressions
- Numerical values
- Model names
- Variables
- Statistical relationships

A single retrieval method is therefore insufficient.

The system combines:

```text
Dense Semantic Retrieval
        +
Lexical BM25 Retrieval
        +
Reciprocal Rank Fusion
        +
Cross-Encoder Reranking
```

### 3. Structural understanding

A research chunk is not treated as an isolated piece of text.

It may be related to:

- Previous chunk
- Next chunk
- Same section
- Figure
- Table
- Formula
- Other evidence from the same document

The knowledge graph captures these relationships and enables graph-aware context expansion.

### 4. Grounded research generation

The LLM is expected to generate research claims from retrieved evidence rather than unsupported knowledge.

The generation flow is:

```text
Retrieved Evidence
       |
       v
Grounded RAG
       |
       v
Citations
       |
       v
Research Synthesis
```

### 5. Research traceability

Every generated insight should be traceable through:

```text
Document
   |
   v
Page
   |
   v
Section
   |
   v
Chunk
   |
   v
Evidence
```

---

# Research Corpus

The current research corpus contains:

**11 quantitative-finance research PDFs.**

The documents are processed through the multimodal ingestion pipeline before being converted into structured evidence chunks.

| Evidence Type | Count |
|---|---:|
| Total chunks | **1,141** |
| Semantic/Text chunks | **695** |
| Formula-evidence chunks | **301** |
| Figure-evidence chunks | **77** |
| Table-evidence chunks | **68** |

The system therefore treats research documents as a multimodal evidence collection rather than a collection of plain-text paragraphs.

---

# 1. Multimodal Data Ingestion

Notebook:

```text
01_data_ingestion_multimodal.ipynb
```

The first stage converts research PDFs into structured machine-readable evidence.

The ingestion pipeline preserves:

- Document identity
- Page numbers
- Section hierarchy
- Text
- Tables
- Figures
- Formulas
- Element IDs
- Evidence relationships

This metadata becomes important for downstream retrieval, graph construction, and citation traceability.

## Evidence Representation

Extracted research elements retain metadata such as:

```text
source_file
page
section_path
element_id
figure_id
table_id
formula_id
content_type
```

---

# 2. Production Chunking

Notebook:

```text
02_production_chunking.ipynb
```

The chunking stage converts extracted document structure into retrieval-ready evidence units.

The system creates multiple chunk types:

```text
semantic
formula_evidence
table_evidence
figure_evidence
```

This allows queries involving equations, tables, figures, or ordinary textual explanations to be retrieved independently.

## Chunk Metadata

Chunks retain information such as:

```text
chunk_id
source_file
pages
section_path
token_count
text
chunk_type
content_types
previous_chunk_id
next_chunk_id
formula_ids
table_ids
figure_ids
```

The `previous_chunk_id` and `next_chunk_id` relationships are later useful for graph construction and contextual expansion.

---

# 3. Embedding Generation

Notebook:

```text
03_embeddings_production.ipynb
```

Semantic embeddings are generated using:

```text
BAAI/bge-small-en-v1.5
```

Embedding dimensionality:

```text
384
```

The resulting vector collection contains:

```text
1,141 x 384
```

vectors.

These vectors form the basis for dense semantic retrieval.

## Why Embeddings?

Keyword matching can fail when the query and evidence use different wording.

For example:

```text
Query:
How do quantitative investors affect trading behavior?

Evidence:
The increasing adoption of algorithmic investment strategies
changes the trading dynamics of financial institutions.
```

The concepts are related even though the exact words differ.

Semantic embeddings allow the system to retrieve conceptually related evidence.

---

# 4. Dense Retrieval

The dense retrieval layer uses FAISS over the generated embeddings.

```text
User Query
    |
    v
Query Embedding
    |
    v
FAISS Similarity Search
    |
    v
Top-K Semantic Candidates
```

Configured retrieval depth:

```text
Top-20
```

Dense retrieval provides strong semantic matching but can miss exact terminology, numbers, identifiers, or specialized phrases.

This motivates the lexical retrieval channel.

---

# 5. BM25 Lexical Retrieval

Notebook:

```text
04_hybrid_retrieval_updated.ipynb
```

BM25 provides lexical retrieval based on term matching.

The BM25 index contains:

```text
1,132 records
```

BM25 is particularly useful for queries containing:

- Exact terminology
- Model names
- Numerical values
- Specific financial concepts
- Rare words
- Named variables

Configured retrieval depth:

```text
Top-20
```

---

# 6. Hybrid Retrieval with Reciprocal Rank Fusion

Dense and lexical retrieval are combined using **Reciprocal Rank Fusion (RRF)**.

```text
                 Query
                   |
          +--------+--------+
          |                 |
          v                 v
       FAISS               BM25
      Top-20              Top-20
          |                 |
          +--------+--------+
                   |
                   v
          Reciprocal Rank
             Fusion
                   |
                   v
                 Top-10
```

Dense retrieval contributes semantic similarity.

BM25 contributes lexical precision.

RRF combines the rankings without requiring the two retrieval systems to produce directly comparable scores.

---

# 7. Cross-Encoder Reranking

Notebook:

```text
05_cross_encoder_reranking.ipynb
```

After hybrid retrieval, candidate evidence is reranked using:

```text
BAAI/bge-reranker-base
```

The cross-encoder evaluates the relationship between:

```text
Query
+
Candidate Evidence
```

The resulting retrieval pipeline is:

```text
FAISS Top-20
      +
BM25 Top-20
      |
      v
    RRF
      |
      v
   Top-10
      |
      v
Cross-Encoder
      |
      v
    Top-5
```

The reranker is primarily used to improve the ordering of relevant evidence.

---

# 8. Retrieval Evaluation

The retrieval benchmark contains:

```text
26 questions
```

The benchmark evaluates retrieval quality using:

- Recall@10
- Mean Reciprocal Rank (MRR)
- nDCG@10

## Retrieval Results

| Retrieval Method | Recall@10 | MRR | nDCG@10 |
|---|---:|---:|---:|
| FAISS | 0.5769 | 0.2949 | 0.3506 |
| BM25 | 0.4231 | 0.1897 | 0.2399 |
| RRF Hybrid | 0.5769 | 0.2540 | 0.3274 |
| Cross-Encoder | **0.5769** | **0.3702** | **0.4066** |

### Main Observation

Cross-encoder reranking does not increase Recall@10 in the current benchmark, but it improves ranking quality.

Compared with hybrid retrieval:

```text
MRR:
0.2540 -> 0.3702

nDCG@10:
0.3274 -> 0.4066
```

This demonstrates the value of reranking the retrieved candidate set.

---

# 9. Knowledge Graph Construction

Notebook:

```text
06_knowledge_graph_graph_aware_context.ipynb
```

The system builds a graph representation of the research corpus.

Current graph scale:

```text
Nodes: 3,426
Edges: 10,111
```

The graph captures structural relationships between research evidence units.

## Graph Relationships

Examples include:

```text
same_section
next_chunk
previous_chunk
figure relationships
table relationships
formula relationships
```

The graph provides a structural representation alongside the vector and lexical retrieval layers.

---

# 10. Graph-Aware Context Expansion

The knowledge graph is used after retrieval to recover structurally related evidence.

```text
Retrieved Chunk
      |
      +-- Previous Chunk
      +-- Next Chunk
      +-- Same Section
      +-- Related Figure
      +-- Related Table
      +-- Related Formula
```

This is useful when an answer requires information distributed across multiple related evidence units.

The knowledge graph therefore acts as a **context expansion mechanism**, rather than replacing initial retrieval.

---

# 11. Grounded RAG Pipeline

Notebook:

```text
07_rag_pipeline.ipynb
```

The RAG layer combines:

```text
Hybrid Retrieval
      |
      v
Cross-Encoder Reranking
      |
      v
Graph-Aware Context
      |
      v
Grounded Context
      |
      v
LLM
      |
      v
Answer + Citations + Traceability
```

The generated answer is grounded in the supplied research evidence.

## Grounding Principle

> **Use the supplied evidence to support research claims and avoid unsupported claims.**

The RAG response maintains:

- Answer
- Citations
- Source document
- Pages
- Section
- Chunk IDs
- Evidence

---

# 12. Citation and Traceability

A key design principle is evidence traceability.

A generated citation such as:

```text
[S5]
```

can be resolved through the evidence metadata to:

```text
[S5]
  |
  v
Source PDF
  |
  v
Page
  |
  v
Section
  |
  v
Chunk ID
  |
  v
Original Evidence
```

This makes generated research outputs auditable.

---

# 13. Research Synthesis

Notebook:

```text
08_research_synthesis_v2.ipynb
```

The research synthesis layer converts grounded RAG evidence into structured quantitative-research insights.

Input:

```text
RAG response
+
Research evidence
```

Output:

```text
Research Theme
Key Findings
Quantitative Factors
Relationships
Limitations
Evidence Mapping
```

## Structured Research Output

The synthesis follows a structure similar to:

```json
{
  "research_theme": "...",
  "key_findings": [
    {
      "finding": "...",
      "evidence": ["S1", "S2"]
    }
  ],
  "factors": [
    {
      "factor_name": "...",
      "definition": "...",
      "economic_intuition": "...",
      "formula": "...",
      "evidence": ["S1"]
    }
  ],
  "relationships": [
    {
      "relationship": "...",
      "evidence": ["S1", "S2"]
    }
  ],
  "limitations": [
    {
      "limitation": "...",
      "evidence": ["S1"]
    }
  ]
}
```

---

# 14. Quantitative Factor Extraction

The synthesis layer explicitly extracts quantitative research factors.

Each factor can contain:

### Factor Name

The name of the quantitative or economic factor.

### Definition

What the factor represents.

### Economic Intuition

Why the factor matters and what relationship it represents.

### Formula

A mathematical representation when supported by the source evidence.

### Evidence

The citations supporting the factor.

This moves the system beyond basic question answering toward structured quantitative research analysis.

---

# 15. Citation Validation

The synthesis pipeline performs citation traceability validation.

The system:

1. Collects valid evidence citations.
2. Extracts citations used by generated synthesis.
3. Compares both sets.
4. Identifies unresolved citations.
5. Flags unsupported citation identifiers.

Conceptually:

```text
Valid Citations
      |
      v
S1 S2 S3 S4 S5

Generated Synthesis
      |
      v
S1 S3 S5

Citation Validation
      |
      v
PASS
```

This provides an additional guardrail against fabricated evidence references.

---

# 16. Evaluation Framework

Evaluation is implemented across multiple notebooks:

```text
09_evaluation(2).ipynb
10_evaluation_matrices_part2(1).ipynb
11_rag_system_evaluation.ipynb
11_rag_system_evaluation_gemini_updated.ipynb
```

The framework evaluates the system at two levels:

```text
Retrieval Evaluation
        +
End-to-End RAG Evaluation
```

---

# 17. Retrieval Evaluation Metrics

## Recall@K

Measures whether relevant evidence appears within the retrieved top-K candidates.

## Mean Reciprocal Rank (MRR)

Measures how high the first relevant evidence appears.

## nDCG@K

Measures ranking quality while considering graded relevance.

These metrics allow retrieval to be evaluated independently of the LLM.

---

# 18. End-to-End RAG Evaluation

The final RAG evaluation focuses on:

1. Answer Correctness
2. Answer Completeness
3. Faithfulness / Groundedness
4. Citation Accuracy

The reported overall score is:

```text
Overall RAG Score =
    40% Correctness
  + 25% Completeness
  + 25% Faithfulness
  + 10% Citation Accuracy
```

Retrieval metrics are evaluated separately from the final RAG score.

---

# 19. RAG Evaluation Results

| Metric | Score |
|---|---:|
| Answer Correctness | **4.50 / 5 — 90.00%** |
| Answer Completeness | **4.35 / 5 — 86.92%** |
| Faithfulness / Groundedness | **4.92 / 5 — 98.46%** |
| Citation Accuracy | **4.58 / 5 — 91.54%** |
| Overall RAG Score | **4.58 / 5 — 91.50%** |

The strongest component is **faithfulness**, indicating strong grounding of generated answers in retrieved evidence.

---

# 20. Reference Answer Comparison

The evaluation framework also compares generated answers against reference answers.

Two complementary metrics are used.

## Semantic Similarity

Embeddings are generated using:

```text
BAAI/bge-small-en-v1.5
```

and compared using cosine similarity.

Reported semantic similarity:

```text
91.92%
```

## Lexical F1

Token-level comparison measures lexical overlap.

Reported lexical F1:

```text
51.89%
```

Together, these metrics provide both semantic and surface-level comparison.

---

# 21. Evaluation Dataset Design

The benchmark is designed around multiple evidence modalities and reasoning requirements.

Categories include:

```text
Semantic / factual
Formula / quantitative
Table-based
Figure-based
Multi-chunk reasoning
Cross-document
Difficult retrieval
```

This prevents evaluation from being limited to simple paragraph retrieval.

---

# 22. Streamlit Research Application

Notebook:

```text
12_streamlit_app.ipynb
```

The project includes a Streamlit-based research interface.

The application provides a user-facing layer over the research pipeline.

The intended workflow is:

```text
Research Question
      |
      v
Retrieval
      |
      v
Reranking
      |
      v
Graph Context
      |
      v
Grounded RAG
      |
      v
Citations
      |
      v
Research Synthesis
```

The interface allows the research intelligence system to be used interactively rather than only through notebooks.

---

# 23. Notebook Pipeline

The notebooks represent the system development pipeline in sequential stages:

```text
01_data_ingestion_multimodal.ipynb
        |
        v
02_production_chunking.ipynb
        |
        v
03_embeddings_production.ipynb
        |
        v
04_hybrid_retrieval_updated.ipynb
        |
        v
05_cross_encoder_reranking.ipynb
        |
        v
06_knowledge_graph_graph_aware_context.ipynb
        |
        v
07_rag_pipeline.ipynb
        |
        v
08_research_synthesis_v2.ipynb
        |
        v
09_evaluation(2).ipynb
        |
        v
10_evaluation_matrices_part2(1).ipynb
        |
        v
11_rag_system_evaluation.ipynb
        |
        v
11_rag_system_evaluation_gemini_updated.ipynb
        |
        v
12_streamlit_app.ipynb
```

---

# 24. Technology Stack

## Programming

- Python
- Jupyter Notebook

## Document Processing

- Docling
- PDF processing
- Multimodal document parsing

## Embeddings

- Sentence Transformers
- `BAAI/bge-small-en-v1.5`

## Vector Retrieval

- FAISS

## Lexical Retrieval

- BM25

## Hybrid Retrieval

- Reciprocal Rank Fusion

## Reranking

- `BAAI/bge-reranker-base`

## Knowledge Graph

- Graph-based document relationships
- Graph-aware context expansion

## LLM

- Google Gemini

The synthesis pipeline uses the Gemini API and reads model configuration through:

```text
GEMINI_MODEL
```

with the configured default:

```text
gemini-3.5-flash-lite
```

## Application

- Streamlit

## Evaluation

- Recall@K
- MRR
- nDCG@K
- Cosine Similarity
- Lexical F1
- Correctness
- Completeness
- Faithfulness
- Citation Accuracy

---

# 25. Configuration

The system expects environment configuration for the Gemini API.

Example:

```env
GEMINI_API_KEY=your_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
```

Never commit API keys to Git.

Use:

```text
.env
```

and include it in:

```text
.gitignore
```

---

# 26. Core Design Decisions

## Why Hybrid Retrieval?

Dense retrieval understands semantic similarity.

BM25 handles exact lexical matching.

Quantitative research requires both.

Therefore:

```text
FAISS + BM25
```

provides complementary retrieval signals.

---

## Why Reranking?

Initial retrieval is optimized for candidate coverage.

The cross-encoder then improves ordering and relevance of the retrieved candidates.

Therefore:

```text
Retrieve Broadly
      |
      v
Rerank Precisely
```

---

## Why a Knowledge Graph?

Vector similarity does not explicitly represent document structure.

The graph captures relationships such as:

```text
previous / next
same section
figure
table
formula
```

This enables structurally informed context expansion.

---

## Why Multimodal Evidence?

Important quantitative information can occur in:

```text
Paragraphs
Tables
Figures
Equations
```

Flattening these into plain text can lose useful retrieval signals.

The system therefore preserves multimodal evidence separately.

---

## Why Citation Traceability?

Financial research requires auditability.

A generated claim should not be accepted simply because an LLM produced it.

The system therefore maintains:

```text
Claim
 |
 v
Citation
 |
 v
Evidence Chunk
 |
 v
Page
 |
 v
Source PDF
```

---

# 27. End-to-End Query Flow

A complete user query follows this process:

```text
1. User enters a quantitative research question.
                    |
                    v
2. Query is prepared for retrieval.
                    |
                    v
3. FAISS performs dense semantic retrieval.
                    |
                    v
4. BM25 performs lexical retrieval.
                    |
                    v
5. Results are merged using RRF.
                    |
                    v
6. Top candidates are reranked with the BGE cross-encoder.
                    |
                    v
7. Related graph context is identified.
                    |
                    v
8. Graph-aware evidence context is assembled.
                    |
                    v
9. Grounded RAG generates an answer.
                    |
                    v
10. Citations and traceability metadata are attached.
                    |
                    v
11. Evidence is passed to research synthesis.
                    |
                    v
12. Key findings and quantitative factors are extracted.
                    |
                    v
13. Citation traceability is validated.
                    |
                    v
14. Final research output is presented.
```

---

# 28. Research Output Structure

The system can transform raw research evidence into structured intelligence:

```text
Research Theme
|
+-- Key Findings
|
+-- Quantitative Factors
|     |
|     +-- Factor Name
|     +-- Definition
|     +-- Economic Intuition
|     +-- Formula
|     +-- Evidence
|
+-- Relationships
|
+-- Limitations
```

This makes the system more suitable for quantitative research workflows than a conventional question-answering chatbot.

---

# 29. Current System Scale

| Component | Current Scale |
|---|---:|
| Research PDFs | **11** |
| Total chunks | **1,141** |
| Semantic chunks | **695** |
| Formula chunks | **301** |
| Figure chunks | **77** |
| Table chunks | **68** |
| Embedding dimension | **384** |
| FAISS vectors | **1,141** |
| BM25 records | **1,132** |
| Graph nodes | **3,426** |
| Graph edges | **10,111** |
| Evaluation questions | **26** |

---

# 30. Retrieval Performance

```text
FAISS
Recall@10 = 0.5769
MRR       = 0.2949
nDCG@10   = 0.3506

BM25
Recall@10 = 0.4231
MRR       = 0.1897
nDCG@10   = 0.2399

RRF Hybrid
Recall@10 = 0.5769
MRR       = 0.2540
nDCG@10   = 0.3274

Cross-Encoder
Recall@10 = 0.5769
MRR       = 0.3702
nDCG@10   = 0.4066
```

The primary measured benefit of reranking in the current benchmark is improved ranking quality.

---

# 31. End-to-End RAG Performance

```text
Correctness       = 90.00%
Completeness      = 86.92%
Faithfulness      = 98.46%
Citation Accuracy = 91.54%

Overall RAG Score = 91.50%
```

These results indicate strong grounding and citation performance while leaving room for improvement in answer completeness and retrieval coverage.

---

# 32. Limitations

### Reference-answer limitation

Reference answers are generated from frozen gold chunks using Gemini and are not necessarily human-verified unless manually reviewed.

### Retrieval limitation

The current benchmark reports the same Recall@10 for FAISS, RRF, and Cross-Encoder, meaning the largest measured improvement from reranking is ranking quality rather than retrieval coverage.

### Evaluation scope

The benchmark currently contains 26 questions. The reported metrics therefore represent the current research corpus and benchmark rather than a universal performance guarantee.

### LLM dependency

Research synthesis depends on the configured Gemini API and requires valid credentials and API availability.

---

# 33. Future Improvements

Potential extensions include:

- Larger research corpus
- Larger and more diverse evaluation benchmark
- Human-verified reference answers
- Query expansion
- Learned retrieval weighting
- Better mathematical-expression retrieval
- Multimodal figure understanding
- Table-aware retrieval
- More advanced graph reasoning
- Agentic research workflows
- Persistent research memory
- Portfolio and factor comparison
- Automated research report generation
- Time-series and market-data integration
- Backtesting integration
- Research-to-signal pipelines

---

# 34. Project Positioning

The system represents a progression from traditional RAG toward a **Quantitative Research Intelligence System**.

```text
Traditional RAG
    |
    +-- Text Retrieval
    +-- LLM Generation
    |
    v
Hybrid RAG
    |
    +-- Dense Retrieval
    +-- BM25
    +-- Reranking
    |
    v
Graph-Aware RAG
    |
    +-- Knowledge Graph
    +-- Structural Context
    |
    v
Research Intelligence
    |
    +-- Grounded Synthesis
    +-- Quantitative Factor Extraction
    +-- Citation Traceability
    +-- Systematic Evaluation
```

The objective is not merely to answer questions about papers, but to transform quantitative-finance literature into **structured, traceable, and evaluable research intelligence**.

---

# 35. Quick Start

Clone the repository:

```bash
git clone https://github.com/mdrajaistekhar786/Quant_Research_Intelligence_System.git
cd Quant_Research_Intelligence_System
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate on Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure environment variables:

```env
GEMINI_API_KEY=your_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
```

Run the notebooks sequentially:

```text
01 -> 02 -> 03 -> 04 -> 05 -> 06
 -> 07 -> 08 -> 09 -> 10 -> 11 -> 12
```

For the Streamlit application, run the actual Streamlit entry-point present in the repository, for example:

```bash
streamlit run <streamlit_entry_file>.py
```

---

# 36. Notebook Reference

| Notebook | Purpose |
|---|---|
| `01_data_ingestion_multimodal.ipynb` | Multimodal PDF ingestion and structured evidence extraction |
| `02_production_chunking.ipynb` | Production chunk creation and metadata preservation |
| `03_embeddings_production.ipynb` | Embedding generation and vector preparation |
| `04_hybrid_retrieval_updated.ipynb` | FAISS + BM25 + RRF retrieval |
| `05_cross_encoder_reranking.ipynb` | Cross-encoder candidate reranking |
| `06_knowledge_graph_graph_aware_context.ipynb` | Knowledge graph construction and graph-aware context |
| `07_rag_pipeline.ipynb` | Grounded RAG pipeline |
| `08_research_synthesis_v2.ipynb` | Research synthesis and quantitative factor extraction |
| `09_evaluation(2).ipynb` | Retrieval/evaluation experiments |
| `10_evaluation_matrices_part2(1).ipynb` | Evaluation matrices and analysis |
| `11_rag_system_evaluation.ipynb` | End-to-end RAG evaluation |
| `11_rag_system_evaluation_gemini_updated.ipynb` | Updated Gemini-based evaluation |
| `12_streamlit_app.ipynb` | Streamlit research application |

---

# 37. Summary

The **Quant Research Intelligence System** combines:

- Multimodal document intelligence
- Structured evidence extraction
- Production chunking
- Dense retrieval
- BM25 lexical retrieval
- Reciprocal Rank Fusion
- Cross-encoder reranking
- Knowledge-graph context expansion
- Grounded RAG
- Citation traceability
- Research synthesis
- Quantitative factor extraction
- Systematic evaluation
- Interactive Streamlit interface

The core architecture is:

```text
Multimodal Evidence
        |
        v
Structured Chunks
        |
        v
Dense + Lexical Retrieval
        |
        v
Cross-Encoder Reranking
        |
        v
Knowledge Graph Context
        |
        v
Grounded RAG
        |
        v
Traceable Research Synthesis
        |
        v
Quantitative Factors
        |
        v
Evaluation
```

With the current research corpus, the system processes **11 PDFs**, **1,141 evidence chunks**, **1,141 384-dimensional embeddings**, and a knowledge graph containing **3,426 nodes and 10,111 edges**.

The evaluated RAG pipeline achieves a reported overall score of **91.50%**, including **98.46% faithfulness** and **91.54% citation accuracy**.

The resulting system provides a foundation for an auditable, AI-powered quantitative research workflow where research claims remain connected to their underlying evidence.
