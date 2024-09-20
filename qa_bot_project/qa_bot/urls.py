from django.urls import path
from .views import QuestionAnsweringView

urlpatterns = [
    path('qa/', QuestionAnsweringView.as_view(), name='question-answering'),
]

