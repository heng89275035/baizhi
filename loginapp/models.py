
from django.db import models


class Type(models.Model):
    title = models.CharField(max_length=20, blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'type'


class User(models.Model):
    username = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)
    salt = models.CharField(max_length=50)

    class Meta:
        db_table = 'user'


class Writings(models.Model):
    course_id = models.AutoField(primary_key=True)
    time = models.DateTimeField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    course_name = models.CharField(max_length=60, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    cate = models.ForeignKey(Type, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'writings'
