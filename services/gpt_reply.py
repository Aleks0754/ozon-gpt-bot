import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_reply(review: str) -> str:
    if not review.strip():
        return "Спасибо за отзыв!"

    system_prompt = "Ты — дружелюбный, немного весёлый продавец фигурок с Ozon. Отвечай тепло и человечно."
    user_prompt = f"Отзыв: {review}\nСформулируй ответ от имени продавца."

    response = openai.ChatCompletion.create(
        model=os.getenv("GPT_MODEL_DEFAULT", "gpt-3.5-turbo"),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
        max_tokens=300,
    )

    return response["choices"][0]["message"]["content"].strip()
