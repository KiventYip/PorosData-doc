# Examples

This section provides practical examples of using PorosData-Processor in various scenarios.

## Basic Text Cleaning

### Simple Usage

```python
from porosdata_processor import TextCleaner

# Initialize cleaner
cleaner = TextCleaner()

# Clean basic text
text = "This is a  test text with   multiple   spaces."
result = cleaner.clean(text)
print(result)  # "This is a test text with multiple spaces."
```

### Academic Text Processing

```python
# Process academic text with formulas and citations
academic_text = """
The energy equation is $E = mc^2$ [Einstein, 1905].
Greek letters like α and β are common in physics.
See reference 【1】 for more details.
"""

cleaner = TextCleaner()
result = cleaner.clean(academic_text)
print(result)
# Output:
# The energy equation is $E = mc^2$ [Einstein, 1905].
# Greek letters like \alpha and \beta are common in physics.
# See reference [1] for more details.
```

## Custom Pipelines

### Minimal Pipeline

```python
# Only perform essential cleaning
minimal_cleaner = TextCleaner(pipeline=[
    "normalize_whitespace",
    "remove_extra_spaces"
])

text = "Text   with    extra   spaces    and  inconsistent  formatting."
result = minimal_cleaner.clean(text)
# Result: "Text with extra spaces and inconsistent formatting."
```

### Science-Focused Pipeline

```python
# Focus on scientific content processing
science_cleaner = TextCleaner(pipeline=[
    "greek_to_latex",
    "citation_rules",
    "patterns_cleaning"
])

text = "α particles and β rays 【1】 are studied in nuclear physics."
result = science_cleaner.clean(text)
# Result: "\alpha particles and \beta rays [1] are studied in nuclear physics."
```

## File Processing

### Single File Processing

```python
# Process a Markdown file
cleaner = TextCleaner()

cleaner.clean_file(
    input_path="research_paper.md",
    output_path="clean_research_paper.md",
    encoding="utf-8"
)
```

### Batch Processing

```python
from processing.batch_processor import BatchProcessor

# Process all Markdown files in a directory
processor = BatchProcessor()
processor.process_text_data(
    input_dir="data/raw_papers",
    output_dir="data/cleaned_papers"
)
```

## Advanced LaTeX Processing

### Formula Space Cleaning

```python
# Enable advanced LaTeX formula cleaning
advanced_cleaner = TextCleaner(clean_options={
    "clean_latex_math_spaces": True
})

# Before: formulas with extra spaces
messy_formulas = """
The matrix is $\\mathbf { X }$ and the fraction is $\\frac { a }{ b }$.
"""

result = advanced_cleaner.clean(messy_formulas)
print(result)
# After: "\\mathbf{X}" and "\\frac{a}{b}"
```

### Complex Mathematical Expressions

```python
cleaner = TextCleaner()

complex_math = """
The Schrödinger equation is $i\\hbar\\frac{\\partial}{\\partial t}\\psi = \\hat{H}\\psi$.

For multiple particles: $\\sum_{i=1}^{N} \\nabla_i^2 \\psi + \\frac{1}{r_{ij}}\\psi = E\\psi$.
"""

result = cleaner.clean(complex_math)
# Formulas are protected and Greek letters converted
```

## Real-World Use Cases

### Research Paper Processing

```python
# Process a research paper with mixed content
paper_text = """
`# Introduction`

In quantum mechanics, the wave function ψ satisfies the equation:

$$i\\hbar\\frac{\\partial}{\\partial t}\\psi = \\hat{H}\\psi$$

Greek letters like α, β, and γ are used throughout physics.

`## References`

【1】 Einstein, A. (1905). "Zur Elektrodynamik bewegter Körper".

【2】 Schrödinger, E. (1926). "An undulatory theory of the mechanics of atoms and molecules".
"""

cleaner = TextCleaner()
processed_paper = cleaner.clean(paper_text)
# Result: Properly formatted academic paper with protected equations
```

### Dataset Preparation for LLM Training

```python
# Prepare academic text for LLM training
training_texts = [
    "The photoelectric effect shows that light behaves as particles (photons) with energy $E = h\\nu$.",
    "Quantum entanglement involves states where particles are correlated, even at large distances 【Einstein, 1935】.",
    "The uncertainty principle states that $\\Delta x \\cdot \\Delta p \\geq \\frac{\\hbar}{2}$.",
]

cleaner = TextCleaner()

for text in training_texts:
    cleaned = cleaner.clean(text)
    # Save cleaned text for training
    print(f"Original: {text}")
    print(f"Cleaned:  {cleaned}")
    print("-" * 50)
```

### Code Documentation Processing

```python
# Process documentation containing code examples
documentation = '''
The `calculate_energy` function implements Einstein's famous equation:

```python
def calculate_energy(mass, velocity):
    """
    Calculate relativistic energy.

    Args:
        mass: Rest mass in kg
        velocity: Velocity in m/s

    Returns:
        Total energy in Joules
    """
    c = 3e8  # Speed of light
    return mass * c**2 / (1 - velocity**2/c**2)**0.5
```

The formula $E = \\frac{mc^2}{\\sqrt{1 - \\frac{v^2}{c^2}}}$ is used.
'''

cleaner = TextCleaner()
result = cleaner.clean(documentation)
# Code blocks and formulas are preserved, text is cleaned
```

## Error Handling

### Graceful Error Handling

```python
# Continue processing even if some plugins fail
robust_cleaner = TextCleaner(ignore_errors=True)

problematic_text = "Text with potential issues..."
try:
    result = robust_cleaner.clean(problematic_text)
    print(f"Successfully processed: {result}")
except Exception as e:
    print(f"Processing failed: {e}")
```

### Custom Error Handling

```python
from porosdata_processor.exceptions import TextProcessorError

cleaner = TextCleaner(ignore_errors=False)  # Raise exceptions

try:
    result = cleaner.clean("potentially problematic text")
except TextProcessorError as e:
    print(f"Processing error: {e}")
    # Handle error appropriately
```

## Performance Optimization

### Processing Large Documents

```python
# For very large files, process in chunks
def process_large_file(file_path, chunk_size=1024*1024):
    cleaner = TextCleaner()

    with open(file_path, 'r', encoding='utf-8') as f:
        while chunk := f.read(chunk_size):
            cleaned_chunk = cleaner.clean(chunk)
            # Process or save cleaned_chunk
            yield cleaned_chunk
```

### Benchmarking Performance

```python
import time

def benchmark_cleaner(text, cleaner, iterations=100):
    start_time = time.time()

    for _ in range(iterations):
        result = cleaner.clean(text)

    end_time = time.time()
    avg_time = (end_time - start_time) / iterations

    print(".4f")
    return result
```

## Integration Examples

### With Pandas

```python
import pandas as pd

# Process text columns in a DataFrame
df = pd.read_csv('academic_papers.csv')

cleaner = TextCleaner()

# Clean abstract column
df['clean_abstract'] = df['abstract'].apply(cleaner.clean)

# Clean title column
df['clean_title'] = df['title'].apply(cleaner.clean)
```

### With spaCy

```python
import spacy
from porosdata_processor import TextCleaner

# Combine with spaCy for advanced NLP processing
nlp = spacy.load("en_core_web_sm")
cleaner = TextCleaner()

def process_academic_text(text):
    # First clean the text
    cleaned = cleaner.clean(text)

    # Then apply NLP processing
    doc = nlp(cleaned)

    return doc

# Process academic text
text = "The α particle has energy $E = \\frac{1}{2}mv^2$."
doc = process_academic_text(text)
```

### Web Framework Integration

```python
# Example Flask integration
from flask import Flask, request, jsonify
from porosdata_processor import TextCleaner

app = Flask(__name__)
cleaner = TextCleaner()

@app.route('/clean', methods=['POST'])
def clean_text():
    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        result = cleaner.clean(text)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

These examples demonstrate the versatility of PorosData-Processor across different use cases and integration scenarios.