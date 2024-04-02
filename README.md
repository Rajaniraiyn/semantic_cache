<div align="center">

# `semantic-cache`: Semantic Caching for Python Functions

</div>

This project provides a decorator for Python functions that implements semantic caching. This means that function calls with semantically similar inputs will return the cached result, even if the exact input values are different. This can be useful for optimizing expensive function calls, especially when dealing with natural language processing or other tasks where inputs can vary slightly but still have the same meaning.

## How it works

The semantic_cache decorator uses the Qdrant vector similarity search engine to store and retrieve function call information. When a function is decorated, the following happens:

1. **Input encoding:** The function arguments and keyword arguments are converted into a string representation.
2. **Similarity search:** This string representation is used to query Qdrant for similar previously cached function calls.
3. **Cache hit:** If a similar call is found with a similarity score above a threshold (default 0.95), the cached result is returned.
4. **Cache miss:** If no similar call is found, the function is executed, its output is stored in the cache along with the input representation, and the output is returned.

## Installation

```sh
pip install semantic-cache
```

## Usage

```py
from semantic_cache import semantic_cache

@semantic_cache()
def say(message: str) -> str:
    return f"Hi {message}"

# First call, function is executed
result1 = say("John")

# Second call with semantically similar input, cached result is used
result2 = say("john")

assert result1 == result2
```

## Features

- **Similarity threshold:** You can adjust the similarity threshold for determining cache hits.
- **In-memory caching:** By default, an in-memory Qdrant instance is used for caching. You can configure a persistent Qdrant server for production use.
- **Automatic input encoding:** The decorator automatically handles the conversion of function arguments into a searchable representation.

## Potential Applications

- **Natural language processing:** Cache results for functions that process text inputs, even if the wording is slightly different.
- **Machine learning model inference:** Optimize inference calls by caching results for similar input data points.
- **Expensive calculations:** Cache the results of computationally intensive functions based on input parameters.

## Contributing

Contributions are welcome! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for details.

## License

This project is licensed under the [MIT License](LICENSE).
