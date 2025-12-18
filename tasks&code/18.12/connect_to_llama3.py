GROQ_API_KEY = "вставь сюда API ключ"

def extract_params_with_llama3(text: str) -> dict:
    client = Groq(api_key=GROQ_API_KEY)

    prompt = f"""
        Ты — ИИ, который извлекает параметры из технических документов.

        Извлеки параметры и их значения из следующего текста и верни ТОЛЬКО JSON без пояснений, без markdown и лишнего текста.
        Выдели минимум 10 параметров.

        Пример:
        {{
        "Дата составления акта": "01.01.2025",
        "Полувагон": "000123",
        "Место осмотра": "ТВМ 652"
        }}

        Текст:
        {text}
        """

    chat_completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    raw_response = chat_completion.choices[0].message.content.strip()
    print("Ответ от LLM:\n", raw_response)  # отладка

    try:
        # Некоторые LLM могут обернуть JSON в markdown (```)
        json_start = raw_response.find('{')
        json_end = raw_response.rfind('}') + 1
        json_text = raw_response[json_start:json_end]
        return json.loads(json_text)
    except Exception as e:
        raise ValueError(f"Не удалось разобрать JSON из ответа:\n{raw_response}") from e
    