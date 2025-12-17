from langchain_ollama import OllamaEmbeddings
from sentence_transformers.util import cos_sim

embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")

text_data = ["Sigiriya is a UNESCO World Heritage Site famous for its ancient rock fortress and mirror wall.",
             "Ella is known for one of the world’s most scenic train journeys through tea plantations.",
             "Galle Fort is a living colonial town with strong Portuguese and Dutch influences.",
             "Yala National Park has one of the highest leopard densities in the world.",
             "Nuwara Eliya is called Little England due to its cool climate and tea estates."]

text_data_vectors = embeddings.embed_documents(texts=text_data)

print(len(text_data_vectors[0]))


def semantic_search(search_query, k=5):
    search_query_vec = embeddings.embed_query(search_query)

    scores = [(0, 0.234345345), (1, 0.354545)]

    for i, doc in enumerate(text_data_vectors):
        cosine_similarity = cos_sim(search_query_vec, doc)[0][0].item()
        scores.append((i, cosine_similarity))

    scores.sort(key=lambda x: x[1], reverse=True)

    return [(text_data[index], score) for index, score in scores[:k]]


search_results=semantic_search("Capital of Sri Lanka")

for val,score in search_results:
    print(f"Score : {score} - Val : {val}")