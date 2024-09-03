from anthropic import Anthropic
import os
def process_with_claude(prompt, max_tokens=8192):
    client = Anthropic(
        # This is the default and can be omitted
        api_key=os.getenv("ANTHROPIC_API_KEY"),

    )
    try:
        message = client.messages.create(
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="claude-3-5-sonnet-20240620",
        )
        return message.content
    except Exception as e:
        print(f"Error processing with Claude API: {e}")
        return None
