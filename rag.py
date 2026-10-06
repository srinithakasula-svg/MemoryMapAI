import os
import pickle

import numpy as np

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer


# Load .env
load_dotenv()


# Embedding model
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "all-MiniLM-L6-v2"
)


# Local storage file
INDEX_FILE = "memorymap_index.pkl"


# Load embedding model
model = SentenceTransformer(
    EMBEDDING_MODEL
)


# Stored note chunks
documents = []


def cosine_similarity(
    query_embedding,
    document_embeddings
):
    """
    Calculate cosine similarity.
    """

    query_embedding = (
        query_embedding /
        (np.linalg.norm(query_embedding) + 1e-10)
    )

    document_embeddings = (
        document_embeddings /
        (
            np.linalg.norm(
                document_embeddings,
                axis=1,
                keepdims=True
            ) + 1e-10
        )
    )

    return np.dot(
        document_embeddings,
        query_embedding
    )


def save_documents(
    chunks,
    document_name
):
    """
    Convert chunks into embeddings
    and save them locally.
    """

    global documents

    # Remove previous version of same document
    documents = [
        item
        for item in documents
        if item["source"] != document_name
    ]

    # Create embeddings
    embeddings = model.encode(
        chunks,
        convert_to_numpy=True,
        show_progress_bar=False
    )

    # Store chunks + embeddings
    for chunk, embedding in zip(
        chunks,
        embeddings
    ):

        documents.append(
            {
                "source": document_name,
                "text": chunk,
                "embedding": embedding
            }
        )

    save_index()

    return len(chunks)


def save_index():
    """
    Save the RAG index.
    """

    with open(
        INDEX_FILE,
        "wb"
    ) as file:

        pickle.dump(
            documents,
            file
        )


def load_index():
    """
    Load previously saved notes.
    """

    global documents

    if os.path.exists(
        INDEX_FILE
    ):

        with open(
            INDEX_FILE,
            "rb"
        ) as file:

            documents = pickle.load(
                file
            )


def search_documents(
    question,
    number_of_results=3
):
    """
    Search relevant note chunks.
    """

    if not documents:
        return []

    # Convert question to embedding
    query_embedding = model.encode(
        question,
        convert_to_numpy=True
    )

    # Get document embeddings
    document_embeddings = np.array(
        [
            item["embedding"]
            for item in documents
        ]
    )

    # Calculate similarity
    scores = cosine_similarity(
        query_embedding,
        document_embeddings
    )

    # Highest similarity first
    ranked_indices = np.argsort(
        scores
    )[::-1]

    results = []

    for index in ranked_indices:

        score = float(
            scores[index]
        )

        # Ignore extremely unrelated chunks
        if score < 0.20:
            continue

        item = documents[index]

        results.append(
            {
                "source": item["source"],
                "text": item["text"],
                "score": score
            }
        )

        if len(results) >= number_of_results:
            break

    return results


def get_document_names():
    """
    Get uploaded document names.
    """

    return sorted(
        set(
            item["source"]
            for item in documents
        )
    )


def get_document_count():
    return len(
        get_document_names()
    )


def get_chunk_count():
    return len(documents)


def get_document_chunks(
    document_name
):
    return [
        item["text"]
        for item in documents
        if item["source"] == document_name
    ]


def delete_document(
    document_name
):
    global documents

    documents = [
        item
        for item in documents
        if item["source"] != document_name
    ]

    save_index()


# Load stored data when app starts
load_index()