from django.db import models
from django.db.models import DateTimeField


class Student(models.Model):
    student_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=40)
    speciality = models.CharField(max_length=124, blank=False)


class Faculty(models.Model):
    faculty_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=124, blank=False)
    last_name = models.CharField(max_length=124, blank=False)


class Course(models.Model):
    course_id = models.IntegerField(primary_key=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    description = models.TextField()
    credits = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()


class Grade(models.Model):
    grade_id = models.IntegerField(primary_key=True)
    marks = models.IntegerField()
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)


class StudentRegistration(models.Model):
    registration_id = models.IntegerField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    registration_data = DateTimeField(auto_now_add=True)


class ScheduleSlot(models.Model):
    schedule_id = models.IntegerField(primary_key=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    student_id = models.ManyToManyField(Student)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    start_time = models.IntegerField()
    end_time = models.IntegerField()
