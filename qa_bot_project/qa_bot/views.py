# qa_bot/views.py

import json
from django.core.files.storage import default_storage
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from langchain.document_loaders import PyPDFLoader, JSONLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI

class QuestionAnsweringView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        questions_file = request.FILES.get('questions')
        document_file = request.FILES.get('document')

        if not questions_file or not document_file:
            return Response({"error": "Both questions and document files are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Save files temporarily
        questions_path = default_storage.save('documents/questions.json', questions_file)
        document_path = default_storage.save(f'documents/document.{document_file.name.split(".")[-1]}', document_file)

        try:
            # Load questions
            with default_storage.open(questions_path) as f:
                questions = json.load(f)

            # Load document
            if document_path.endswith('.pdf'):
                loader = PyPDFLoader(document_path)
                pages = loader.load_and_split()
            elif document_path.endswith('.json'):
                loader = JSONLoader(file_path=document_path, jq_schema='.', text_content=False)
                pages = loader.load()
            else:
                return Response({"error": "Unsupported document file type"}, status=status.HTTP_400_BAD_REQUEST)

            # Process document
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            texts = text_splitter.split_documents(pages)

            # Create embeddings and store in FAISS index
            embeddings = OpenAIEmbeddings()
            docsearch = FAISS.from_documents(texts, embeddings)

            # Initialize the QA chain with ChatOpenAI
            chat_model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
            chain = load_qa_chain(chat_model, chain_type="stuff")

            # Process questions and get answers
            results = {}
            for question in questions:
                docs = docsearch.similarity_search(question)
                answer = chain.run(input_documents=docs, question=question)
                results[question] = answer

            return Response(results, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        finally:
            # Clean up temporary files
            default_storage.delete(questions_path)
            default_storage.delete(document_path)

