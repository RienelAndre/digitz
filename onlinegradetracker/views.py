from django.shortcuts import render
from .models import *
from django.shortcuts import redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            if user.groups.filter(name='teacher').exists():
                return redirect('teacherdashboard', teacher_pk=1)
            elif user.groups.filter(name='student').exists():
                return redirect('studentdashboard', student_pk=1)
            else:
                messages.info(request, 'Username or Password is incorrect')        
        else:
            messages.info(request, 'Username or Password is incorrect')

    return render(request, 'pages/login.html')
def register(request):
    teacher_form = CreateTeacherForm()
    student_form = CreateStudentForm()
    
    if request.method == 'POST':
        registration_type = request.POST.get('registration_type')
        
        if registration_type == 'teacher':
            form = CreateTeacherForm(request.POST)
            if form.is_valid():
                user = form.save()
                teacher_group = Group.objects.get_or_create(name='teacher')[0]
                teacher_group.user_set.add(user)
                messages.success(request, 'Account was created for ' + user.username)
                return redirect('login')
            
        elif registration_type == 'student':
            form = CreateStudentForm(request.POST)
            if form.is_valid():
                user = form.save()
                student_group = Group.objects.get_or_create(name='student')[0]
                student_group.user_set.add(user) 
                messages.success(request, 'Account was created for ' + user.username)
                return redirect('login')

    context = {'teacher_form': teacher_form, 'student_form': student_form}
    return render(request, 'pages/register.html', context)

def logoutteacher(request):
    return redirect('login')


def student(request):
    return render(request, 'pages/student.html')

def teacher(request):
    return render(request, 'pages/teacher.html')


def about(request, teacher_pk):
    teacher = Teacher.objects.get(pk=teacher_pk)

    context = {
        'teacher': teacher
    }
    return render(request, 'pages/about.html', context)


def studentgrades(request, student_pk, course_pk):
    student = Student.objects.get(pk=student_pk)
    course = Course.objects.get(pk=course_pk)
    grades = Grade.objects.filter(student=student, course=course)

    context = {
        'student':student,
        'course':course,
        'grades':grades
    }

    return render(request, 'pages/studentgrades.html', context)

def teacherindex(request):
    return render(request, 'pages/teacherindex.html')


def studentdashboard(request, student_pk):
    student = Student.objects.get(pk=student_pk)
    enrolled_courses = student.get_enrolled_courses()

    context = {
        'student': student,
        'enrolled_courses': enrolled_courses
    }
    return render(request, 'pages/studentdashboard.html', context)

@login_required(login_url='login')
def teachergrading(request, teacher_pk, course_pk):
    teacher = Teacher.objects.get(pk=teacher_pk)
    course = Course.objects.get(pk=course_pk)
    enrolled_students = course.students_enrolled.all()

    student_grades = []
    for student in enrolled_students:
        try:
            grade = Grade.objects.get(teacher=teacher, course=course, student=student)
            student_grades.append(grade)

        except Grade.DoesNotExist:
            default_grade = Grade(teacher=teacher, course=course, student=student)
            student_grades.append(default_grade)
    context = {
        'course': course,
        'teacher': teacher,
        'enrolled_students':enrolled_students,
        'student_grades': student_grades
    }
    return render(request, 'pages/teachergrading.html', context)

@login_required(login_url='login')
def teacherdashboard(request, teacher_pk):
    teacher = Teacher.objects.get(pk=teacher_pk)
    current_courses = teacher.get_current_courses()

    context = {
        'teacher': teacher,
        'current_courses': current_courses
    }
    return render(request, 'pages/teacherdashboard.html', context)


def studentindex(request):
    return render(request, 'pages/studentindex.html')

@login_required(login_url='login')
def studentprofile(request, student_pk):
    student = Student.objects.get(pk=student_pk)

    try:
        student_profile = StudentProfile.objects.get(student=student)
    except StudentProfile.DoesNotExist:
        student_profile = None 

    context = {
        'student': student,
        'student_profile': student_profile
    }
    return render(request, 'pages/studentprofile.html', context)

@login_required(login_url='login')
def teacherprofile(request, teacher_pk):
    teacher = Teacher.objects.get(pk=teacher_pk)

    try:
        teacher_profile = TeacherProfile.objects.get(user=teacher)
    except TeacherProfile.DoesNotExist:
        teacher_profile = None
        
    context = {
        'teacher': teacher,
        'teacher_profile': teacher_profile
    }
    return render(request, 'pages/teacherprofile.html', context)

@login_required(login_url='login')
def teacherform(request, teacher_pk):
    teacher = Teacher.objects.get(pk=teacher_pk)
    teacher_form = teacherUpdateForm(instance=teacher)
    
    try:
        teacher_profile = teacher.teacherprofile
    except TeacherProfile.DoesNotExist:
        teacher_profile = TeacherProfile.objects.create(user=teacher)

    if request.method == 'POST':
        teacher_form = teacherUpdateForm(request.POST, instance=teacher)
        profile_form = TeacherProfileForm(request.POST, request.FILES, instance=teacher_profile)
        if teacher_form.is_valid() and profile_form.is_valid():
            teacher_form.save()
            profile_form.save()

            return redirect('teacherprofile', teacher_pk=teacher.pk)

    else:
        profile_form = TeacherProfileForm(instance=teacher_profile)

    context = {
        'teacher': teacher,
        'teacher_form': teacher_form,
        'profile_form': profile_form
    }
    return render(request, 'pages/teacherform.html', context)

@login_required(login_url='login')
def gradeform(request, teacher_pk, course_pk, student_pk):
    teacher = Teacher.objects.get(pk=teacher_pk)
    course = Course.objects.get(pk=course_pk)
    student = Student.objects.get(pk=student_pk)

    try:
        grade = Grade.objects.get(teacher=teacher, course=course, student=student)
    except Grade.DoesNotExist:
        grade = Grade(teacher=teacher, course=course, student=student)

    if request.method =='POST':
        form = GradeEditForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            return redirect('teachergrading', teacher_pk=teacher.pk, course_pk=course.pk)
    else:
        form = GradeEditForm(instance=grade)

    context = {
        'teacher': teacher,
        'course': course,
        'student': student,
        'grade': grade,
        'form': form
    }

    return render(request, 'pages/gradeform.html', context)

@login_required(login_url='login')
def enrollform(request, student_pk):
    student = Student.objects.get(pk=student_pk)
    course = None
    if request.method == 'POST':
        form = EnrollForm(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data['course_code']
            try:
                course = Course.objects.get(CourseCode=entered_code)
                student.courses_enrolled.add(course)
                return redirect('studentdashboard', student_pk=student.pk)
            except Course.DoesNotExist:
                form.add_error('course_code', 'Invalid course code. Please Try Again.')
    else:
        form=EnrollForm()

    context = {
        'student': student,
        'course': course,
        'form': form,
    }
    return render(request, 'pages/enroll.html', context)

@login_required(login_url='login')
def addcourse(request, teacher_pk):
    teacher = Teacher.objects.get(pk=teacher_pk)

    if request.method == 'POST':
        form = CourseAddForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)  
            course.generate_unique_course_code()  
            course.save()  
            teacher.course_taught.add(course)
            return redirect('teacherdashboard', teacher_pk=teacher.pk)
    else:
        course = Course()
        course.generate_unique_course_code()
        initial_data = {'CourseCode': course.CourseCode}
        form = CourseAddForm(initial=initial_data)

    context = {
        'teacher': teacher,
        'form': form,
    }
    return render(request, 'pages/addcourse.html', context)

@login_required(login_url='login')
def removecourse(request, teacher_pk, course_pk):
    teacher = Teacher.objects.get(pk=teacher_pk)
    course = Course.objects.get(pk=course_pk)
    teacher.course_taught.remove(course)
    return redirect('teacherdashboard', teacher_pk=teacher.pk)

@login_required(login_url='login')
def studentform(request, student_pk):
    student = Student.objects.get(pk=student_pk)
    student_form = StudentUpdateForm(instance=student)
    
    try:
        student_profile = student.studentprofile
    except StudentProfile.DoesNotExist:
        student_profile = StudentProfile.objects.create(student=student)

    if request.method == 'POST':
        student_form = StudentUpdateForm(request.POST, instance=student)
        profile_form = StudentProfileForm(request.POST, request.FILES, instance=student_profile)
        if student_form.is_valid() and profile_form.is_valid():
            student_form.save()
            student_profile = profile_form.save(commit=False)
            student_profile.student = student 
            profile_form.save()

            return redirect('studentprofile', student_pk=student.pk)

    else:
        profile_form = StudentProfileForm(instance=student_profile)

    context = {
        'student': student,
        'student_form': student_form,
        'profile_form': profile_form
    }
    return render(request, 'pages/studentform.html', context)

@login_required(login_url='login')
def studentabout(request, student_pk):
    student = Student.objects.get(pk=student_pk)

    context = {
        'student': student
    }
    return render(request, 'pages/studentabout.html', context)



