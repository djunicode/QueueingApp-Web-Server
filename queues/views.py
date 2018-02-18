from rest_framework import generics
from .serializers import LocationSerializer, UserSerializer, TeacherSerializer, StudentSerializer
from .serializers import QueueSerializer, TokenSerializer
from .models import Location, Teacher, Student, Queue, Token
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404


class LocationList(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def platfrom_create(self, serializer):
        serializer.save()


class LocationDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def platform_create(self, serializer):
        serializer.save()
#
#
# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class UserList(APIView):
#     def get(self, request):
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        token = Token.objects.get(user=user)
        tokenSerializer = TokenSerializer(token)
        # valid_data = serializer.data

        if serializer.is_valid():
            if serializer.data['token'].is_valid() and serializer.data['token'] == token.token:
                tokenSerializer.data['valid'] = True
                return Response(tokenSerializer.data)
            else:
                return Response(tokenSerializer.data)
            serializer.save()
            # if serializer.is_valid():
            #     serializer.save()
            # return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherList(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def platfrom_create(self, serializer):
        serializer.save(user=self.request.user, location=self.request.location)


class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class StudentList(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def platfrom_create(self, serializer):
        serializer.save(user=self.request.user)


class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class QueueList(generics.ListCreateAPIView):
    queryset = Queue.objects.all()
    serializer_class = StudentSerializer

    def platfrom_create(self, serializer):
        serializer.save()


class QueueDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer
