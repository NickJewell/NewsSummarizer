with open('newsletter_20241104.md', 'r', encoding='utf-8') as f:
    content = f.read()
    print("Newsletter content length:", len(content))
    print("\nFirst 200 characters:")
    print(content[:200])
