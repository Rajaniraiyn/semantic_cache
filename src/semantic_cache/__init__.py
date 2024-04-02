from functools import wraps
from typing import Optional

from qdrant_client import QdrantClient

client = QdrantClient(":memory:")
out_store = {}


def semantic_cache(similarity_threshold: Optional[float] = None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            arg_desc = ", ".join([f"arg{i}: {str(arg)}" for i, arg in enumerate(args)])
            kwarg_desc = ", ".join([f"{k}={str(v)}" for k, v in kwargs.items()])

            params_str = f"Function: {func_name}\nArguments: {arg_desc}\nKeyword Arguments: {kwarg_desc}"

            fn_cache_name = str(hash(func.__code__))
            if client.collection_exists(fn_cache_name):
                embeddings = client.query(
                    collection_name=fn_cache_name,
                    query_text=params_str,
                    limit=1,
                )
                if embeddings:
                    embedding = embeddings[0]
                    key = (
                        embedding.metadata["args"],
                        frozenset(embedding.metadata["kwargs"].items()),
                    )
                    score = embedding.score
                    if score >= (similarity_threshold or 0.95):
                        if key in out_store:
                            return out_store[key]

            client.add(
                documents=[params_str],
                collection_name=fn_cache_name,
                metadata=[{"args": args, "kwargs": kwargs}],
                ids=[str(hash(params_str))],
            )

            out = func(*args, **kwargs)
            key = (args, frozenset(kwargs.items()))
            out_store[key] = out
            return out

        return wrapper

    return decorator
