from openai import openai
client = OpenAI()


response = client.responses.create(
    model = "gpt-4.1",
    input = "Based on these user preferences request a recipe from spoonacular api..."
)
print(response.output_text)