from django.db.models import CharField, BooleanField, OneToOneField
from django.db.models import ManyToManyField, IntegerField, DateTimeField
from django.db.models import TimeField, FileField, Model, CASCADE, ForeignKey
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
    maxLength = IntegerField(null=True, blank=True, default=200)
    isEmpty = BooleanField(default=True)
    isFull = BooleanField(default=False)
    size = IntegerField(null=True, blank=True)
    # startTime = TimeField(auto_now_add=True)
    startTime = TimeField(null=True, blank=True)
    avgTime = TimeField(null=True, blank=True)
    endTime = TimeField(null=True, blank=True)
    subject = CharField(max_length=100, null=True)
    lock = BooleanField(default=False)
    flag = IntegerField(default=0)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    queueItems = ListCharField(
        base_field=CharField(max_length=11),
        size=100,
        max_length=100 * 12,
        null=True,
        blank=True
    )
    location = OneToOneField(Location, on_delete=CASCADE, related_name="queue_location", null=True)

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
    user = OneToOneField(User, on_delete=CASCADE, related_name='teacher')
    register_id = CharField(max_length=250, null=True, blank=True)
    name = CharField(max_length=100, null=True)
    isFree = BooleanField(default=False)
    sapId = CharField(unique=True, null=True, max_length=11)
    photo = FileField(null=True, blank=True)
    # subject = CharField(max_length=100, null=True)
    subject = ListCharField(
        base_field=CharField(max_length=50),
        size=15,
        max_length=15 * 51,
        null=True,
        blank=True
    )
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    location = OneToOneField(Location, on_delete=CASCADE, related_name='location', null=True)
    queue = ManyToManyField(Queue, blank=True, related_name='queue')

    def __str__(self):
        return "{}".format(self.name)


class Student(Model):
    user = OneToOneField(User, on_delete=CASCADE, related_name='student')
    register_id = CharField(max_length=250, null=True, blank=True)
    name = CharField(max_length=100, null=True)
    sapID = CharField(unique=True, null=True, max_length=11)
    department = CharField(max_length=10, null=True)
    year = CharField(max_length=2, null=True)
    div = CharField(max_length=1, null=True)
    batch = CharField(max_length=2, null=True)
    subscription = ManyToManyField(Teacher, blank=True, related_name='subscribers')
    inQueue = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    photo = FileField(null=True, blank=True)

    def __str__(self):
        return "{}".format(self.name)


# mysqltestserver

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


class Token(Model):
    user = OneToOneField(User, on_delete=CASCADE, related_name='token')
    token = CharField(max_length=200, null=True, blank=True)
    valid = BooleanField(default=False)

    def __str__(self):
        return self.token
