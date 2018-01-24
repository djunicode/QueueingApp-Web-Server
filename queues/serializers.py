from rest_framework import serializers
from .models import Location, Teacher, Student, Queue
from django.contrib.auth.models import User


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

    class Meta:
        model = User
        fields = ('id', 'username', 'password')

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user


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
