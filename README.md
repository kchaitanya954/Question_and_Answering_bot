# Question-Answering Bot

This project implements a Question-Answering (QA) bot using Django and the Langchain framework. The bot can answer questions based on the content of a provided document (PDF or JSON).

## Features

- Accepts a JSON file containing questions and a document file (PDF or JSON) as input
- Processes the document using Langchain's document loading and text splitting capabilities
- Utilizes OpenAI's language models to generate answers to the provided questions
- Returns a JSON response pairing each question with its corresponding answer

## Prerequisites

- Python 3.8+
- Django 3.2+
- OpenAI API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/kchaitanya954/Question_and_Answering_bot.git
   cd Question_and_Answering_bot/qa_bot_project
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your OpenAI API key as an environment variable:
   ```
   export OPENAI_API_KEY='your-api-key-here'
   ```
   On Windows, use `set OPENAI_API_KEY=your-api-key-here`

5. Run migrations:
   ```
   python manage.py migrate
   ```

6. Start the development server:
   ```
   python manage.py runserver
   ```

## Usage

The API provides a single endpoint for question answering:

- **URL**: `/api/qa/`
- **Method**: POST
- **Content-Type**: multipart/form-data

### Request Parameters

- `questions`: A JSON file containing an array of questions
- `document`: A PDF or JSON file containing the document to be analyzed

### Example Request (using curl)

```bash
curl --location 'http://127.0.0.1:8000/api/qa/' \
--form 'document=@"/C:/Users/kchai/Downloads/ДЗ-1_Кришна Чаитаня.pdf"' \
--form 'questions=@"/C:/Users/kchai/OneDrive/Documents/work tasks/Question_and_Answering_bot/questions.json"'
```
### Example Response

```json
{
    "what language is it?": "The text provided is in Russian.",
    "where do they speak this language?": "Russian is spoken in Russia."
}
```


## Project Structure

```
qa-bot-project/
│
├── qa_bot/
│   ├── __init__.py
│   ├── views.py
│   └── urls.py
│
├── qa_bot_project/
│   ├── __init__.py
│   ├── settings.py
│   └── urls.py
│
├── manage.py
├── requirements.txt
└── README.md
```


## License

This project is licensed under the MIT License.