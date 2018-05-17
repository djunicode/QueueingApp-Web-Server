from rest_framework import serializers
from .models import Location, Teacher, Student, Queue, Token
from django.contrib.auth.models import User
from .tokens import account_activation_token
from django.core.mail import send_mail
from queueing_app import settings
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError


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

    def update(self, instance, validated_data):

        instance.username = validated_data.get('username', instance.username)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()
        return instance
        # token_obj = Token.objects.get(user=instance)
        # user_token = validated_data['token']
        # if token_obj == user_token:
        #     return Response("Token Matched!")
        # else:
        #     return Response("Token not matched")


class TeacherSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True)
    # location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(), allow_null=True)
    # queue = serializers.PrimaryKeyRelatedField(queryset=Queue.objects.all())
    class Meta:
        model = Teacher
        fields = ('id', 'name', 'isFree', 'sapId', 'subject', 'user', 'created_at', 'updated_at', 'location', 'register_id', 'queue')
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        teacher = Teacher(
            user=validated_data['user'],
            name=validated_data['name'],
            isFree=validated_data['isFree'],
            subject=validated_data['subject'],
            sapId=validated_data['sapId'],
            location=validated_data['location'],
            register_id=validated_data['register_id']
        )

        teacher.save()
        return teacher

    def update(self, instance, validated_data):
        instance.user = validated_data['user']
        instance.location = validated_data['location']
        instance.register_id = validated_data['register_id']
        instance.save()

        return instance


class StudentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Student
        fields = ('id', 'name', 'department', 'sapID', 'year', 'user', 'created_at', 'updated_at', 'batch', 'subscription', 'register_id')
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
            register_id=validated_data['register_id'],
        )

        student.save()
        return student


class QueueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Queue
        fields = ('id', 'isEmpty', 'isFull', 'size', 'maxLength', 'startTime', 'endTime', 'avgTime',
                  'subject', 'lock', 'created_at', 'updated_at', 'queueItems', 'location', 'flag')
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        queue = Queue(
            # size=validated_data['size'],
            maxLength=validated_data['maxLength'],
            startTime=validated_data['startTime'],
            endTime=validated_data['endTime'],
            subject=validated_data['subject'],
            queueItems=validated_data['queueItems'],
            location=validated_data['location'],
        )

        queue.save()
        return queue

    def update(self, instance, validated_data):
        instance.isEmpty = validated_data['isEmpty']
        instance.isFull = validated_data['isFull']
        instance.size = validated_data['size']
        instance.maxLength = validated_data['maxLength']
        instance.startTime = validated_data['startTime']
        instance.endTime = validated_data['endTime']
        instance.avgTime = validated_data['avgTime']
        instance.subject = validated_data['subject']
        instance.lock = validated_data['lock']
        instance.location = validated_data['location']
        instance.save()
        # item = validated_data['queueItems']
        # instance.queueItems.append(item)
        return instance


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = ('id', 'token', 'valid')


#Janice code
class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, min_length=8)
    email = serializers.EmailField(required=True)

    def validate(self, validated_data):
        hashed_pass = validated_data['password']
        user = User.objects.get(username = validated_data['username'])

        if not user:
            raise serializers.ValidationError("User Does not exist")

        if(check_password(hashed_pass,user.password)):
            return user
        raise serializers.ValidationError("Incorrect Password")

    class Meta:
        model = User
        fields = ['id','username','password','email']


class StudentLoginSerializer(serializers.ModelSerializer):
    sapID = serializers.CharField(min_length=11, required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Student
        fields = ('id','sapID','password')

    def validate(self, data):
        hashed_pass = data['password']
        try:
            query = Student.objects.get(sapID = data['sapID'])
        except ObjectDoesNotExist:
            raise ValidationError("User does not exist")
        else:
            student_password = query.user.password
            if check_password(hashed_pass,student_password):
                return query
            raise ValidationError("Incorrect password")




class TeacherLoginSerializer(serializers.ModelSerializer):
    sapId = serializers.CharField(min_length=11,required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Teacher
        fields = ('id', 'sapId', 'password')

    def validate(self, data):
        hashed_pass = data['password']
        try:
            query = Teacher.objects.get(sapId = data['sapId'])
        except ObjectDoesNotExist:
            raise ValidationError("User does not exist")
        else:
            teacher_pass = query.user.password
            if check_password(hashed_pass, teacher_pass):
                return query
            raise ValidationError("Incorrect sapid/password")



