from rest_framework import generics
from .serializers import LocationSerializer, UserSerializer, TeacherSerializer, StudentSerializer
from .serializers import QueueSerializer, UserLoginSerializer, TeacherLoginSerializer, StudentLoginSerializer
from .models import Location, Teacher, Student, Queue, Token
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from pyfcm import FCMNotification
import json


class LocationList(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def platfrom_create(self, serializer):
        serializer.save()


class LocationDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


# class UserList(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#     def platform_create(self, serializer):
#         serializer.save()
#
#
# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class UserList(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        # token = Token.objects.get(user=user)
        # tokenSerializer = TokenSerializer(token)
        # print(request.data['token'] == token.token)
        # valid_data = serializer.data

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # if tokenSerializer.data['token'] == token.token:
            #     token.valid = True
            #     # token.valid = True
            #     return Response(token.valid)
            # else:
            #     return Response(token.valid)
            # serializer.save()
            # if serializer.is_valid():
            #     serializer.save()
            # return Response(serializer.data)
            # return Response(tokenSerializer.data)
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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


# class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer


class StudentSubscription(APIView):
    def get_object(self, pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        student = self.get_object(pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def put(self, request, pk):
        student = self.get_object(pk)
        serializer = StudentSerializer(student)
        teacherIds = []
        print(request.data['teacherNames'])
        teacherName = json.loads(request.data['teacherNames'])
        for x in teacherName:
            print(x)
            teacher = Teacher.objects.get(name=x)
            print(teacher.name)
            # student.subscription.append(teacher.id)
            teacherIds.append(teacher.id)
        student.subscription = teacherIds
        student.save()

        return Response(serializer.data)

    def delete(self, request, pk):
        student = self.get_object(pk)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DeleteStudentSubscription(APIView):
    def get_object(self, pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            raise Http404


    def put(self, request, pk):
        student = self.get_object(pk)
        serializer = StudentSerializer(student)
        teacherIds = []
        teacherName = json.loads(request.data['teacherNames'])
        for x in teacherName:
            teacher = Teacher.objects.get(name=x)
            # teacherIds.pop(teacherIds.index(teacher.id))
            teacherIds.append(teacher.id)
            student.subscription.pop(student.subscription.index(teacher.id))
        student.save()

        return Response(serializer.data)



# class QueueList(generics.ListCreateAPIView):
#     queryset = Queue.objects.all()
#     serializer_class = QueueSerializer
#
#     def platfrom_create(self, serializer):
#         serializer.save()


class QueueList(APIView):
    # push_service = FCMNotification(api_key="AAAAIPgZxGg:APA91bES1oGIg3Em-SQQSxYUynTjIdoHciNadaq6-olWdXVFxWEpwVHEaRo5Wf_PU-EX2yD4tiih3xaPWA0d3sAJWgVQbJrtODhlklYV7dOQ-WmV2qJ5mnIbqxLoEpTzI6Qhsu4VaI9q")

    def get(self, request):
        queue = Queue.objects.all()
        serializer = QueueSerializer(queue, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = QueueSerializer(data=request.data)
        # teacherName = request.data['teacherName']
        # teacher = Teacher.objects.get(name=teacherName)
        # subscribers = teacher.subscribers.all()
        # registration_ids = [x.register_id for x in subscribers]
        # message_title = "First Notification"
        # message_body = "Getting all the list of queues"
        # data_message = {
        #     "click_action": "StudentScreenActivity"
        # }
        # self.push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body, data_message=data_message)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class QueueDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Queue.objects.all()
#     serializer_class = QueueSerializer


class QueueDetails(APIView):
    push_service = FCMNotification(api_key="AAAAIPgZxGg:APA91bES1oGIg3Em-SQQSxYUynTjIdoHciNadaq6-olWdXVFxWEpwVHEaRo5Wf_PU-EX2yD4tiih3xaPWA0d3sAJWgVQbJrtODhlklYV7dOQ-WmV2qJ5mnIbqxLoEpTzI6Qhsu4VaI9q")

    def get_object(self, pk):
        try:
            return Queue.objects.get(pk=pk)
        except Queue.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        registration_ids = ["d-Di8WDILuw:APA91bE02qGEkVUWelt_frw67UeaaD9L5rAEKDHW79zQ_p7J10jTusa0dHIEJ8Op3IWHLX37jQioNAMHSEro0RpyUwsg8035kV4IondFC_rHU1ObbX7eBhwNqwGIq94Bv2ZPvm92uiBG",
                            "eEq2eaw8sGE:APA91bFDG6Mt9X2t5fx-HCLmVCcqlUn6qMXVblolXgcBBfu0gvhJo0SKLeU37SgamSLri-5SfNOLWm_BuoXzlLKduK05FF_VlHaYjq4awz9Z3QcsZmpz8hhhCrILQtX7Ydh6fhg_G9gw"]
        message_title = "First Notification"
        message_body = "Getting all the list of queues"
        data_message = {
            "click_action": "StudentScreenActivity"
        }
        self.push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body, data_message=data_message)
        queue = self.get_object(pk)
        serializer = QueueSerializer(queue)
        return Response({"data": serializer.data, "items": queue.queueItems})

    def put(self, request, pk):
        queue = self.get_object(pk)
        serializer = QueueSerializer(queue, data=request.data)
        # if serializer.is_valid():
        #     queue.queueItems.append(request.data['queueItems'])
        #     for x in queue.queueItems:
        #         print(x)
        #     # print(queue.queueItems)
        #     queue.save()
        #     return Response({"data": serializer.data, "items": queue.queueItems})
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        queue = self.get_object(pk)
        queue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QueueDeleteItems(APIView):
    def get_object(self, pk):
        try:
            return Queue.objects.get(pk=pk)
        except Queue.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        queue = self.get_object(pk)
        # serializer = QueueSerializer(queue, data=request.data)
        deleted = queue.queueItems.pop(0)
        print(queue.queueItems)
        queue.save()
        return Response({"items": queue.queueItems, "deleted": deleted})


class QueueDeleteSpecificItems(APIView):
    def get_object(self, pk):
        try:
            return Queue.objects.get(pk=pk)
        except Queue.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        queue = self.get_object(pk)
        deleted = queue.queueItems.pop(queue.queueItems.index(request.data['element']))
        # serializer = QueueSerializer(queue, data=request.data)
        # deleted = queue.queueItems.pop(request.data['element'])
        # for x in queue.queueItems:
        #     if x == request.data['element']:
        #         queue.queueItems.pop(x)
        print(queue.queueItems)
        # print(deleted)
        queue.save()
        return Response({"items": queue.queueItems, "deleted": deleted})


class TeacherNameGet(APIView):
    def get_object(self, name):
        try:
            return Teacher.objects.get(name=name)
        except Teacher.DoesNotExist:
            raise Http404

    def get(self, request, name):
        teacher = self.get_object(name)
        serializer = TeacherSerializer(teacher)
        return Response(serializer.data)


class GetItemIndex(APIView):
    def get_object(self, pk):
        try:
            return Queue.objects.get(pk=pk)
        except Queue.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        queue = self.get_object(pk)
        serializer = QueueSerializer(queue)
        if request.data['sapID'] in queue.queueItems:
            index = queue.queueItems.index(request.data['sapID'])
        else:
            index = -1
        return Response({
            "data": serializer.data,
            "index": index+1
        })


class YouAreNextNotification(APIView):
    push_service = FCMNotification(api_key="AAAAIPgZxGg:APA91bES1oGIg3Em-SQQSxYUynTjIdoHciNadaq6-olWdXVFxWEpwVHEaRo5Wf_PU-EX2yD4tiih3xaPWA0d3sAJWgVQbJrtODhlklYV7dOQ-WmV2qJ5mnIbqxLoEpTzI6Qhsu4VaI9q")
    def get_object(self, pk):
        try:
            return Queue.objects.get(pk=pk)
        except Queue.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        student = Student(sapID=request.data['sapID'])
        message_title = "First Notification"
        message_body = "Getting all the list of queues"
        data_message = {
            "click_action": "StudentScreenActivity"
        }
        registration_id = student.register_id
        self.push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body, data_message=data_message)
        return Response({"response": "valid"})


class GetSubjectTeachers(APIView):
    # def get_object(self, subject):
    #     try:
    #         return Teacher.objects.all(subjects=subject)
    #     except Teacher.DoesNotExist:
    #         raise Http404

    def put(self, request):
        teacher = Teacher.objects.all()
        teacherNames = []
        for x in teacher:
            if request.data["name"] in x.subject:
                teacherNames.append(x.name)
        print(teacherNames)
        return Response({"teachers": teacherNames})


class TokenMatch(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        user = self.get_object(pk)
        # serializer = UserSerializer(user, data=request.data)
        token = Token.objects.get(user=user)
        # tokenSerializer = TokenSerializer(token)
        print(request.data['token'] == token.token)
        # valid_data = serializer.data

        if request.data['token'] == token.token:
            return Response({"valid": "true"})
        else:
            return Response({"valid": "false"})



#Janice code
class UserLogin(generics.ListCreateAPIView):
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentLogin(APIView):
    serializer_class = StudentLoginSerializer

    def post(self, request):
        serializer = StudentLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)



class TeacherLogin(generics.ListCreateAPIView):
    serializer_class = TeacherLoginSerializer
    queryset = Teacher.objects.all()

    def post(self, request):
        serializer = TeacherLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class AddSubjects(APIView):
    def get_object(self, pk):
        try:
            return Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        teacher = self.get_object(pk)
        # serializer = TeacherSerializer(teacher, data=request.data)
        teacher.subject.append(request.data['subject'])
        for x in teacher.subject:
            print(x)
        teacher.save()
        return Response({"subject": teacher.subject})


class SendNotificationToSubscribers(APIView):
    push_service = FCMNotification(
        api_key="AAAAIPgZxGg:APA91bES1oGIg3Em-SQQSxYUynTjIdoHciNadaq6-olWdXVFxWEpwVHEaRo5Wf_PU-EX2yD4tiih3xaPWA0d3sAJWgVQbJrtODhlklYV7dOQ-WmV2qJ5mnIbqxLoEpTzI6Qhsu4VaI9q")

    def get(self, request):
        queue = Queue.objects.all()
        serializer = QueueSerializer(queue, many=True)
        return Response(serializer.data)


    def post(self, request):
        queue = Queue.objects.get(id=request.data['id'])
        teacherName = request.data['teacherName']
        teacher = Teacher.objects.get(name=teacherName)
        subscribers = teacher.subscribers.all()
        registration_ids = [x.register_id for x in subscribers]
        message_title = "Queue Started"
        message_body = "Submission of " + queue.subject + " is started by Prof. " + teacher.name
        data_message = {
            "sound": "default"
        }
        queue.flag = 1
        queue.save()
        self.push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body, data_message=data_message)
        return Response({"response": "Notification sent"})


class GetTeacherLocatonFromName(APIView):
    def put(self, request):
        teacher = Teacher.objects.get(name=request.data['name'])
        return Response({"location": teacher.location})


class QueueAddItems(APIView):
    def get_object(self, pk):
        try:
            return Queue.objects.get(pk=pk)
        except Queue.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        queue = self.get_object(pk)
        serializer = QueueSerializer(queue, data=request.data)
        if serializer.is_valid():
            queue.queueItems.append(request.data['queueItems'])
            for x in queue.queueItems:
                print(x)
            # print(queue.queueItems)
            queue.save()
            return Response({"data": serializer.data, "items": queue.queueItems})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class AddTeacherSubject(APIView):
#     def get_object(self, pk):
#         try:
#             return Teacher.objects.get(pk=pk)
#         except Teacher.DoesNotExist:
#             raise Http404
#
#     def put(self, request, pk):
#         teacher = self.get_object(pk)


class GetTeacherQueues(APIView):


    def post(self, request):
        teacher = Teacher.objects.get(name=request.data['teacherName'])
        teacherQueues = teacher.queue.all()
        finalResponse = []
        for x in teacherQueues:
            print(x)
            serializer = QueueSerializer(x)
            finalResponse.append(serializer.data)
        # serializer = QueueSerializer(teacher.queue.all())
        return Response(finalResponse)


class TeacherAddingQueues(APIView):
    def get_object(self, pk):
        try:
            return Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        teacher = self.get_object(pk)
        queue = Queue.objects.get(pk=request.data['id'])
        teacher.queue.add(queue)
        teacher.save()
        return Response({"added": "true"})
        # teacher.queue = []
        # if len(teacher.queue) == 0:
        #     teacher.queue[0] = request.data['id']
        # else:
        #     length = len(teacher.queue)
        #     teacher.queue[length] = request.data['id']


class TeacherDeletingQueues(APIView):
    def get_object(self, pk):
        try:
            return Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        teacher = self.get_object(pk)
        queue = Queue.objects.get(pk=request.data['id'])
        teacher.queue.remove(queue)
        teacher.save()
        return Response({"deleted": "true"})
