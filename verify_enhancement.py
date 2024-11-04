# Script to check both newsletter files and verify enhancement
with open('newsletter_20241104.md', 'r', encoding='utf-8') as f:
    original = f.read()
    print("\nOriginal Newsletter Sample:")
    print("=" * 50)
    print(original[:500])

with open('newsletter_edited_20241104.md', 'r', encoding='utf-8') as f:
    enhanced = f.read()
    print("\nEnhanced Newsletter Sample:")
    print("=" * 50)
    print(enhanced[:500])
