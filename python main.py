import pandas as pd
import string
import matplotlib.pyplot as plt
from transformers import pipeline

# -----------------------------
# Load Sentiment Analysis Model
# -----------------------------
print("Loading AI model... Please wait.")

sentiment_model = pipeline("sentiment-analysis")

# -----------------------------
# Stop Words List
# -----------------------------
stop_words = {
    "the", "is", "and", "a", "an",
    "of", "to", "in", "for", "on",
    "was", "were", "am", "are",
    "this", "that", "it"
}

# -----------------------------
# Text Cleaning Function
# -----------------------------
def clean_text(text):

    # Convert to lowercase
    text = text.lower()

    # Remove punctuation
    text = text.translate(
        str.maketrans('', '', string.punctuation)
    )

    # Split into words
    words = text.split()

    # Remove stop words
    filtered_words = []

    for word in words:
        if word not in stop_words:
            filtered_words.append(word)

    return " ".join(filtered_words)

# -----------------------------
# Read Feedback Data
# -----------------------------
try:
    df = pd.read_csv("feedback.csv")
except FileNotFoundError:
    print("Error: feedback.csv not found.")
    exit()

# -----------------------------
# Clean Text
# -----------------------------
df["cleaned_comment"] = df["comment"].apply(clean_text)

# -----------------------------
# Sentiment Analysis
# -----------------------------
sentiments = []

for comment in df["cleaned_comment"]:

    result = sentiment_model(comment)

    label = result[0]["label"]

    sentiments.append(label)

df["sentiment"] = sentiments

# -----------------------------
# Display Results
# -----------------------------
print("\n" + "="*60)
print("FEEDBACK ANALYSIS REPORT")
print("="*60)

for index, row in df.iterrows():

    print(f"\nComment {index+1}")
    print("Original :", row["comment"])
    print("Cleaned  :", row["cleaned_comment"])
    print("Sentiment:", row["sentiment"])

# -----------------------------
# Summary Statistics
# -----------------------------
print("\n" + "="*60)
print("SUMMARY")
print("="*60)

sentiment_counts = df["sentiment"].value_counts()

print(sentiment_counts)

positive_count = sentiment_counts.get("POSITIVE", 0)
negative_count = sentiment_counts.get("NEGATIVE", 0)

total_comments = len(df)

print("\nTotal Comments :", total_comments)
print("Positive       :", positive_count)
print("Negative       :", negative_count)

# -----------------------------
# Save Results
# -----------------------------
df.to_csv("sentiment_results.csv", index=False)

print("\nResults saved to sentiment_results.csv")

# -----------------------------
# Plot Bar Chart
# -----------------------------
plt.figure(figsize=(6, 4))

sentiment_counts.plot(kind="bar")

plt.title("Feedback Sentiment Analysis")
plt.xlabel("Sentiment")
plt.ylabel("Number of Comments")

plt.tight_layout()

plt.show()
