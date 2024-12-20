def count_tokens(text, cohere_client):
    response = cohere_client.tokenize(text=text)
    return len(response.tokens)