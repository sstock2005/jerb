import openai    

openai.api_key = "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"
completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a jerbal named Jerb"},
      {"role": "user", "content": "test"}
    ]
)
print(completion.choices[0].message)