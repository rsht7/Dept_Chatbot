with open('data/courses_data.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Spliting by double newline
paragraphs = text.strip().split('\n\n')

print(f"Total paragraphs detected: {len(paragraphs)}")

# printing first few paragraphs to check
for i, para in enumerate(paragraphs[:5]):  # Just first 5 for sample
    print(f"\n--- Paragraph {i+1} ---\n")
    print(para)
