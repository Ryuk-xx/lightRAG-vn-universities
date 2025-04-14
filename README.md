# University Info Chatbot with Graph and Chunk Retrieval

This is a university information retrieval chatbot that uses a hybrid method combining Knowledge Graph and Chunk-based Retrieval to answer queries about universities. It can also search the web for additional information if needed.

## 🔍 Features
- Hybrid Retrieval: Uses both knowledge graphs and text chunking for accurate information retrieval.

- Web-enhanced Queries: Falls back to web search if local data does not contain enough relevant information.

- Custom lightRAG Prompt and Pipeline: Built upon a modified version of LightRAG. (Source: https://github.com/HKUDS/LightRAG)


## 📁 Project Structure

```
├── lightrag/                     # Customized LightRAG module
├── web_search_for_more_info/     # Web search module for additional data
├── document.json                 # University data (raw)
├── addressing.json               # University address data
├── indexing/                     # Code for storing processed data into database
├── data_indexing/                # Stored data in knowledge graph and chunks
├── retrieval.py                  # Main script for querying and generating answers
└── test.ipynb                    # Notebook to test the retrieval and generation flow
```


## ⚒️ Setting
### 1. Install requirement libraries
```
pip install -r requirements.txt
```
### 2. Source data
- This data is crawled from a website about VietNamese universities (Source: https://dsdaihoc.com/).
- The data crawling scripts are **not publicly available** in this repository.
- This project only includes the processing, indexing, and retrieval components using pre-collected data (`document.json`).

## 🧠 Core Components
### 1. lightrag/
- This is a customized version of the LightRAG library, modified to fit the hybrid retrieval needs of the chatbot.
### 2. web_search_for_more_info/
- Contains utilities to perform a web search and fetch online content to supplement answers when internal data is insufficient.
### 3. document.json & addressing.json
- document.json: Contains structured data about different universities.
- addressing.json: Contains corresponding address and location information of universities.
### 4.indexing/
- Scripts and utilities that process raw JSON data and store them into a vector store or graph database.
### 5. data_indexing/
  - Pre-processed data in two forms:
    + Knowledge graph format (entities, relations)
    + Chunked text for semantic retrieval
### 6. retrieval.py
  - This script handles:
    + Query processing
    + Running hybrid retrieval
    + Generating final answers using RAG-style techniques
### 7. test.ipynb
  - A Jupyter Notebook for testing the pipeline end-to-end, from input queries to answer generation.
## 🚀 Usage
- You can run the chatbot by invoking the retrieval.py script with your question. For testing, use the test.ipynb notebook to simulate query-answer interactions.
## 🤝 Credits
- Built upon LightRAG
- Web search powered by integrated search APIs
- Source data: https://dsdaihoc.com/
## ✍️ Note
- 🚧 Work in Progress: Please note that this project is still a work in progress. Certain components are under active development and may not yet be fully functional or finalized.
