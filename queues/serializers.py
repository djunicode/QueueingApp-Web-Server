from rest_framework import serializers
from .models import Location, Teacher, Student, Queue, Token
from django.contrib.auth.models import User
from .tokens import account_activation_token
from django.core.mail import send_mail
from queueing_app import settings


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ('id', 'room', 'department', 'floor', 'updated_at')
        read_only_fields = ('updated_at',)

    def create(self, validated_data):
        location = Location(room=validated_data['room'], department=validated_data['department'],
                            floor=validated_data['floor'])
        location.save()
        return location


class UserSerializer(serializers.ModelSerializer):
    # teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())
    # token = serializers.CharField(max_length=100)
    # token = serializers.PrimaryKeyRelatedField(queryset=Token.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')
        # read_only_fields = ('token',)

    def create(self, validated_data):
        user = User(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()

        subject = "Email verification for django"
        message = account_activation_token.make_token(user)
        token = Token.objects.create(user=user, token=message)
        token.save()
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
        return user

    # def update(self, instance, validated_data):
    #     token_obj = Token.objects.get(user=instance)
    #     user_token = validated_data['token']
    #     if token_obj == user_token:
    #         return Response("Token Matched!")
    #     else:
    #         return Response("Token not matched")


class TeacherSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())

    class Meta:
        model = Teacher
        fields = ('id', 'name', 'isFree', 'sapId', 'subject', 'user', 'created_at', 'updated_at', 'location')
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        teacher = Teacher(
            user=validated_data['user'],
            name=validated_data['name'],
            isFree=validated_data['isFree'],
            subject=validated_data['subject'],
            sapId=validated_data['sapId'],
            location=validated_data['location']
        )

        teacher.save()
        return teacher


class StudentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Student
        fields = ('id', 'name', 'department', 'sapID', 'year', 'user', 'created_at', 'updated_at', 'batch')
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        student = Student(
            user=validated_data['user'],
            name=validated_data['name'],
            department=validated_data['department'],
            year=validated_data['year'],
            sapID=validated_data['sapID'],
            # div=validated_data['div'],
            batch=validated_data['batch'],
        )

        student.save()
        return student


class QueueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Queue
        fields = ('id', 'isEmpty', 'isFull', 'size', 'maxLength', 'startTime', 'endTime', 'avgTime',
                  'subject', 'lock', 'created_at', 'updated_at', 'queueItems')
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        queue = Queue(
            size=validated_data['size'],
            startTime=validated_data['startTime'],
            endTime=validated_data['endTime'],
            subject=validated_data['subject'],
            queueItems=validated_data['queueItems'],
        )

        queue.save()
        return queue


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = ('id', 'token', 'valid')
