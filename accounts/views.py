from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache

from HrManagement import settings
from accounts.models import Student

# Signup
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('txtname')
        email = request.POST.get('txtmail')
        password = request.POST.get('pswd')
        confirm_password = request.POST.get('cpswd')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Signup successful. Please log in.')
        return redirect('login')

    return render(request, 'signup.html')

# Dashboard
@login_required
@never_cache
def dashboard_view(request):
    # Get total count of all students (Superuser sees all, HR sees their own)
    if request.user.is_superuser:
        total_students = Student.objects.all().count()
        # For Admin/Superuser: Count all non-superuser employees (HRs)
        total_employees = User.objects.filter(is_superuser=False).count()
    else:
        # For HR/Normal User: Count only students they added
        total_students = Student.objects.filter(user=request.user).count()
        # Non-superusers don't manage employees, so the count is 0 or not shown
        total_employees = 0

    context = {
        'total_students': total_students,
        'total_employees': total_employees,
    }
    return render(request, 'dashboard.html', context)

# View Students
@login_required
def student_views(request):
    if request.user.is_superuser:
        my_students = Student.objects.all().values()
    else:
        my_students = Student.objects.filter(user=request.user.id).values()


    return render(request, 'display.html', {'student_data': my_students})




# Add Student
@login_required
def add_student_view(request):
    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        student_email = request.POST.get('student_email')
        education = request.POST.get('education')
        course = request.POST.get('course')
        total_fee = float(request.POST.get('total_fee'))
        fee_paid = float(request.POST.get('fee_paid'))

        if Student.objects.filter(email=student_email).exists():
            messages.error(request, 'email already exists')
            return redirect('addstudent')
        student = Student.objects.create(
            user=request.user,
            name=student_name,
            email=student_email,
            education=education,
            course=course,
            total_fee=total_fee,
            paid_fee=fee_paid
        )

        pending_fee = total_fee - fee_paid
        subject = "Admission Confirmation"
        message = f"""
        Hello {student_name},

        You have successfully joined the course: {course}.
        Total Fee: ₹{total_fee}
        Fee Paid: ₹{fee_paid}
        Pending Fee: ₹{pending_fee}

        Please pay the remaining fee on time.

        Regards,
        Palle Institute
        """
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [student_email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return redirect('mystudents')

    return render(request, 'addstudent.html', {'action': "add"})





# from django.http import HttpResponse
def delete_student_view(request,id):
    student = get_object_or_404(Student,id=id,user=request.user)
    student.delete()
    return redirect('mystudents')
2
def update_student_view(request,id):
    student = get_object_or_404(Student, id=id, user=request.user)
    if request.method == 'POST':
        student.name = request.POST.get('student_name')
        student.email = request.POST.get('student_email')
        student.education = request.POST.get('education')
        student.course = request.POST.get('course')
        student.total_fee = float(request.POST.get('total_fee'))
        student.paid_fee = float(request.POST.get('fee_paid'))
        student.save()
        return redirect('mystudents')
    return render(request, 'addstudent.html', {'action': "update","student_data": student})


def employee_view(request):
    employees=User.objects.all().values()
    return render(request, 'employee_display.html', {'employee_data': employees})


def add_employee_view(request):
    if request.method == 'POST':
        employee_name = request.POST.get('username')
        employee_email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        role = request.POST.get('role')
        if password != cpassword:
            messages.error(request, 'Password and cpassword do not match')


        if User.objects.filter(email=employee_email).exists():
            messages.error(request, 'email already exists')
            return redirect('addemployee')
        if role == 'admin':
            employee = User.objects.create_superuser(username=employee_name,
                                                email=employee_email,
                                                password=password)

        else:

            employee = User.objects.create_user(username=employee_name,
                                            email=employee_email,
                                            password=password)
        employee.is_active =True
        employee.is_staff=False
        employee.save()
        return redirect('myemployees')

    return render(request, 'add_employee.html', {'action': "Add"})

def delete_employee_view(request,id):
    employee = get_object_or_404(User, id=id)
    employee.delete()
    return redirect('myemployees')


@login_required
def update_employee_view(request, id):
    employee = get_object_or_404(User, id=id)

    if request.method == 'POST':
        employee.username = request.POST.get('username')
        employee.email = request.POST.get('email')

        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        role = request.POST.get('role')

        if password and password == cpassword:
            employee.set_password(password)  # use set_password for hashing

        # role check
        if role == 'admin':
            employee.is_superuser = True
            employee.is_staff = True
        else:
            employee.is_superuser = False
            employee.is_staff = False

        employee.save()
        messages.success(request, "Employee updated successfully")
        return redirect('myemployees')

    return render(request, 'add_employee.html', {'action': "Update", 'employee': employee})


