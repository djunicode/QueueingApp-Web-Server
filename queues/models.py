from django.db.models import CharField, BooleanField, OneToOneField
from django.db.models import ManyToManyField, IntegerField, DateTimeField
from django.db.models import TimeField, FileField, Model, CASCADE
from django_mysql.models import ListCharField
from django.contrib.auth.models import User
# from queueingApp import settings


class Location(Model):
    floor = IntegerField(null=True)
    department = CharField(max_length=10, null=True)
    room = CharField(max_length=20, null=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return "{} Floor - {} Dept. - {}".format(self.floor, self.department, self.room)


class Queue(Model):
    maxLength = IntegerField(null=True, blank=True)
    isEmpty = BooleanField(default=True)
    isFull = BooleanField(default=False)
    size = IntegerField(null=True, blank=True)
    startTime = TimeField(auto_now_add=True)
    avgTime = TimeField(null=True, blank=True)
    endTime = TimeField(null=True, blank=True)
    subject = CharField(max_length=100, null=True)
    lock = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    queueItems = ListCharField(
        base_field=IntegerField(),
        size=100,
        max_length=100 * 12,
        null=True,
        blank=True
    )

    def __str__(self):
        return "{} - {} items".format(self.subject, len(self.queueItems))


# class Teacher(Model):
#     name = CharField(max_length=100)
#     isFree = BooleanField(default=False)
#     sapId = IntegerField(unique=True)
#     photo = FileField(null=True, blank=True)
#     subject = CharField(max_length=100)
#     created_at = DateTimeField(auto_now_add=True)
#     updated_at = DateTimeField(auto_now=True)
#     loation = OneToOneField(Location, on_delete=CASCADE)
#     queue = ManyToManyField(Queue, blank=True)

#     def __str__(self):
#         return "{}".format(self.name)


# class Student(Model):
#     name = CharField(max_length=100)
#     sapID = IntegerField(unique=True)
#     department = CharField(max_length=10)
#     year = CharField(max_length=2)
#     div = CharField(max_length=1)
#     batch = CharField(max_length=2)
#     subscription = ManyToManyField(Teacher, blank=True)
#     inQueue = BooleanField(default=False)
#     created_at = DateTimeField(auto_now_add=True)
#     updated_at = DateTimeField(auto_now=True)
#     photo = FileField(null=True, blank=True)

#     def __str__(self):
#         return "{}".format(self.name)


# class UserProfile(Model):
#     USER_TYPES = (
#         (0, 'Students'),
#         (1, 'Teachers')
#     )
#     user = OneToOneField(User, on_delete=CASCADE)
#     user_type = IntegerField(null=True, choices=USER_TYPES)
#     name = CharField(max_length=100, blank=True, null=True)
#     sapId = IntegerField(unique=True, blank=True, null=True)
#     photo = FileField(null=True, blank=True, upload_to="images/")
#     created_at = DateTimeField(auto_now_add=True)
#     updated_at = DateTimeField(auto_now=True)
#     def __str__(self):
#         return "{}".format(self.name)
#     class Meta:
#         abstract = True
# class TeacherProfile(Model):
#     loation = OneToOneField(Location, on_delete=CASCADE)
#     queue = ManyToManyField(Queue, blank=True)
#     subject = CharField(max_length=100, blank=True, null=True)
#     isFree = BooleanField(default=False)
#     class Meta:
#         abstract = True
# class StudentProfile(Model):
#     department = CharField(max_length=10, blank=True, null=True)
#     year = CharField(max_length=2, blank=True, null=True)
#     batch = CharField(max_length=2, blank=True, null=True)
#     # subscription = ManyToManyField(TeacherProfile, blank=True)
#     inQueue = BooleanField(default=False)
#     class Meta:
#         abstract = True
# class Profile(TeacherProfile, StudentProfile, UserProfile):
#     USERNAME_FIELD = 'sapId'


class Teacher(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    name = CharField(max_length=100, null=True)
    isFree = BooleanField(default=False)
    sapId = IntegerField(unique=True, null=True)
    photo = FileField(null=True, blank=True)
    subject = CharField(max_length=100, null=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    loation = OneToOneField(Location, on_delete=CASCADE)
    queue = ManyToManyField(Queue, blank=True)

    def __str__(self):
        return "{}".format(self.name)


class Student(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    name = CharField(max_length=100, null=True)
    sapID = IntegerField(unique=True, null=True)
    department = CharField(max_length=10, null=True)
    year = CharField(max_length=2, null=True)
    div = CharField(max_length=1, null=True)
    batch = CharField(max_length=2, null=True)
    subscription = ManyToManyField(Teacher, blank=True)
    inQueue = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    photo = FileField(null=True, blank=True)

    def __str__(self):
        return "{}".format(self.name)


# @receiver(post_save, sender=User)
# def create_user_teacher_profile(sender, instance, created, **kwargs):
#     if created:
#         Teacher.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_teacher_profile(sender, instance, **kwargs):
#     instance.teacher.save()
#
#
# @receiver(post_save, sender=User)
# def create_user_student_profile(sender, instance, created, **kwargs):
#     if created:
#         Student.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_student_profile(sender, instance, **kwargs):
#     instance.sudent.save()
