import random

from openai import OpenAI

from mental.models import Quote


def create_quote(mood):
    if mood:
        prompt = f'باتوجه به حالت روزانه {mood} '
    else:
        prompt = f'به طور رندوم'

    client = OpenAI(
        api_key='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')

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": f'یک جمله انگیزشی {prompt} بگو.'
            }
        ]
    )

    return completion.choices[0].message.content


def get_new_quote(user, mood):
    if mood:
        quotes = Quote.objects.filter(mood=mood)
    else:
        quotes = Quote.objects.all()

    if quotes.exists():
        idx = random.randint(0, len(quotes) - 1)
        return quotes[idx].sentence

    return None

