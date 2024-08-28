from openai import OpenAI

def create_sentence(mood):
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

