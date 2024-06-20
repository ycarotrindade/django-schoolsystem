from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.models import User,Group
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required, permission_required
from .models import Student
from django.core.paginator import Paginator,EmptyPage
from .helpers import calcStatus,verifyStudentName,pages_display,addFilterToQuery,verifyUserName,isDefaultPass,blockForSpecialUser
# Create your views here.


def login_page(request:HttpRequest):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User or Password does not exist')
        else:
            user = authenticate(request,username=username,password=password)
            if user is not None:
                request.session['isDefaultPass'] = isDefaultPass(user)
                login(request,user)
                return redirect('home')
            else:
                messages.error(request, 'Username or Password does not exist')
    return render(request,'base/login.html')

def logout_func(request:HttpRequest):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request:HttpRequest):
    if request.method == "POST":
        try:
            User.objects.filter(id=request.user.id).update(password=make_password(request.POST.get('password')))
            messages.success(request,'Password changed')
            logout(request)
            return redirect('login')
        except:
            messages.error(request,'An error occurred')
    return render(request,'base/main.html')

@login_required(login_url='login')
def students(request:HttpRequest,page:str):
    try:
        page = int(page)
    except:
        return redirect('students',page=1)
    status_options = Student.STATUS_CHOICE.values()
    queryes = request.GET.dict()
    try:
        num_students = Student.objects.filter(**queryes).order_by('name')
    except Exception:
        num_students = Student.objects.all().order_by('name')
    finally:
        paginator = Paginator(num_students,10)
        try:
            student_rows = paginator.page(page)
        except EmptyPage:
            return redirect('students',page=1)
        pages_to_show = pages_display(student_rows,paginator)
                    
        context = {
            'student_rows':student_rows,
            'pages_to_show':pages_to_show,
            'page':page,
            'status_options':status_options
        }
        return render(request,'base/students.html',context=context)

@login_required(login_url='login')
def students_create(request:HttpRequest):
    if request.method == 'POST':
        name = request.POST.get('name')
        try:
            student = Student.objects.get(name=name)
        except:
            queryes = request.POST.dict()
            queryes.pop('csrfmiddlewaretoken')
            queryes['status'] = calcStatus(queryes)
            queryes = {k: v for k, v in queryes.items() if v}
            student = Student.objects.create(**queryes)
            messages.success(request,'Student added')
        else:
            messages.error(request,'Student already added')
            
    
    return render(request,'base/students_create.html')

@login_required(login_url='login')
def students_delete(request:HttpRequest,pk:str):
    try:
        Student.objects.get(id=pk).delete()
    except:
        messages.error(request,'An error occurred')
    else:
        messages.success(request,'Student deleted')
    finally:
        return redirect('students',page='1')

@login_required(login_url='login')
def student_edit(request:HttpRequest,pk:str):
    try:
        student = Student.objects.get(id=pk)
    except:
        messages.error(request,'An error occurred')
        return redirect('students',page=1)
    if request.method == 'POST':
        queryes = request.POST.dict()
        try:
            isNameValid = verifyStudentName(queryes['name'],int(pk))
        except:
            messages.error(request,'An error occurred')
            return redirect('students',page=1)
        else:
            if isNameValid:
                try:
                    queryes['status'] = calcStatus(queryes)
                    queryes.pop('csrfmiddlewaretoken')
                    queryes = {k: v for k, v in queryes.items() if v}
                    Student.objects.filter(id=pk).update(**queryes)
                    messages.success(request,'Student edited')     
                except:
                    messages.error(request,'An error occurred')
                finally:
                    return redirect('students',page=1)
            else:
                messages.error(request,'Invalid name')
                return redirect('student_edit',pk=pk)
    else:
        context = {
            'student':student
        }
        return render(request,'base/student_edit.html',context=context)


@login_required(login_url='login')
@permission_required("auth.view_user",login_url='login',raise_exception=True)
def employees(request:HttpRequest,page:str):
    try:
        page = int(page)
    except:
        return redirect('employees',page=1)
    queryes = request.GET.dict()
    queryes = {k: v for k, v in queryes.items() if v}
    query = 'select us.id,us.username, us.email, us.date_joined, us.last_login, gp.name from auth_user us inner join auth_user_groups ug on us.id = ug.user_id inner join auth_group gp on gp.id = ug.group_id'
    query = addFilterToQuery(query,queryes,'us.username') if len(queryes.keys()) > 0 else query
    try:
        users = User.objects.raw(query)
    except:
        messages.error(request,'An error occurred')
    paginator = Paginator(users,10)
    try:
        users_rows = paginator.page(page)
    except EmptyPage:
        return redirect('employees',page=1)
    pages_to_show = pages_display(users_rows,paginator)
    
    try:
        options = Group.objects.all()
    except:
        messages.error(request,'An error occurred')
        return redirect('employees',page=1)
    context = {
        'page':page,
        'users_rows':users_rows,
        'pages_to_show':pages_to_show,
        'options':options
    }
    
    return render(request,'base/employees.html',context=context)

@login_required(login_url='login')
@permission_required('auth.delete_user',login_url='login',raise_exception=True)
@blockForSpecialUser
def employee_delete(request:HttpRequest,pk:str):
    try:
        user = User.objects.get(id=pk)
    except:
        messages.error(request,'An error occurred')
    else:
        if user.username == 'TEST':
            messages.error(request,"You can't delete this user")
        else:
            try:
                user.delete()
            except:
                messages.error(request,'An error occurred')
            else:
                messages.success(request,'User deleted')
    finally:
        return redirect('employees',page=1)



@login_required(login_url='login')
@permission_required('auth.add_user',login_url='login',raise_exception=True)
def employee_add(request:HttpRequest):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            user = User.objects.get(username=username)
        except:
            queryes = request.POST.dict()
            group = queryes['access']
            queryes.pop('access')
            queryes.pop('csrfmiddlewaretoken')
            queryes['password'] = make_password('default')
            queryes['is_active'] = True
            user = User.objects.create(**queryes)
            group = Group.objects.get(name=group)
            group.user_set.add(user)
            messages.success(request,'User created')
        else:
            messages.error(request,'Invalid Username')
    try:
        options = Group.objects.all()
    except:
        messages.error(request,'An error occurred')
        return redirect('employees',page=1)
    
    context = {
        'options':options
    }
    return render(request,'base/employee_add.html',context=context)

@login_required(login_url='login')
@permission_required('auth.change_user',login_url='login',raise_exception=True)
@blockForSpecialUser
def employee_edit(request:HttpRequest,pk:str):
    try:
        query = 'select us.id, us.username, us.email, gp.name from auth_user us inner join auth_user_groups ug on us.id = ug.user_id inner join auth_group gp on gp.id = ug.group_id where us.id = %s;'
        employee = User.objects.raw(query,params=[pk])[0]
        options = Group.objects.all()
    except:
        messages.error(request,'An error occurred')
        return redirect('employees',page=1)
    if request.method == 'POST':
        queryes = request.POST.dict()
        group = queryes['access']
        queryes.pop('csrfmiddlewaretoken')
        queryes.pop('access')
        try:
            isnameValid = verifyUserName(queryes['username'],int(pk))
        except:
            messages.error(request,'An error occurred')
            return redirect('employees',page=1)
        else:
            if isnameValid:
                try:
                    User.objects.filter(id=pk).update(**queryes)
                    employee = User.objects.get(id=pk)
                    employee.groups.clear()
                    employee.save()
                    group = Group.objects.get(name=group)
                    group.user_set.add(employee)
                    messages.success(request,'User updated')
                except:
                    messages.error(request,'An error occurred')
                finally:
                    return redirect('employees',page=1)
            else:
                messages.error(request,'Invalid Name')
                return redirect('employee_edit',pk=pk)
    else:
        context = {
            'employee':employee,
            'options':options
        }
        return render(request,'base/employee_edit.html',context=context)

@login_required(login_url='login')
@permission_required('auth.change_user',login_url='login',raise_exception=True)
@blockForSpecialUser
def reset_password(request:HttpRequest,pk:str):
    try:
        User.objects.filter(id=pk).update(password=make_password('default'))
    except:
        messages.error(request,'An error occurred')
    else:
        messages.success(request,'Password reseted')
    finally:
        return redirect('employees',page=1)