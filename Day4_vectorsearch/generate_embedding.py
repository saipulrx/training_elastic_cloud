from sentence_transformers import SentenceTransformer
import json

# Load a pre-trained Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Example text
text = ["This is the first sentence."]

# Generate embeddings
embeddings = model.encode(text)

# Print embeddings
print("Embedding shape:", embeddings.shape)
print(embeddings[0])

doc = {"sentence": text[0], "vector": embeddings[0].tolist()}
print(json.dumps(doc, indent=2))
