
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from todos.serializers import TodoSerializer
from rest_framework.permissions import IsAuthenticated
from todos.models import Todo
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from todos.pagination import CustomPageNumberPagination


class TodosAPIView(ListCreateAPIView):
    serializer_class = TodoSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAuthenticated,]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter]

    def perform_create(self, serializer):           #Saves the owner as the user that created the todo
        return serializer.save(owner = self.request.user)

    def get_queryset(self):
        return Todo.objects.filter(owner= self.request.user)
    
    filterset_fields = ['id', 'title', 'is_completed',]
    search_fields = ['id', 'title', 'is_completed',]
    ordering_fields = ['id', 'title', 'is_completed',]
    

class  TodoDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated,]
    lookup_field = "id"

    def get_queryset(self):
        return Todo.objects.filter(owner= self.request.user)
    

# class CreateTodoAPIView(CreateAPIView):
#     serializer_class = TodoSerializer
#     permission_classes = [IsAuthenticated,]
#     authentication_classes = [JWTAuthentication]

#     def perform_create(self, serializer):           #Saves the owner as the user that created the todo
#         return serializer.save(owner = self.request.user)
    

# class TodoListAPIView(ListAPIView):
#     serializer_class = TodoSerializer
#     permission_classes = [IsAuthenticated,]
#     authentication_classes = [JWTAuthentication]
     
#     queryset = Todo.objects.all()

#     def get_queryset(self):
#         return Todo.objects.filter(owner= self.request.user)
