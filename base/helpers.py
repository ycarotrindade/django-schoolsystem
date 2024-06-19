from .models import Student
from django.contrib.auth.models import User
from django.core.paginator import Paginator,Page
from django.contrib.auth.hashers import check_password

def calcStatus(queryes:dict):
    status = None
    try:
        mean = float(queryes['score1'])+float(queryes['score2'])+float(queryes['score3'])
    except:
        status = 'UNDEFINED'
    else:
        if mean <=4:
            status = 'FAILED'
        elif mean > 4 and mean < 6:
            status = 'ANALYSIS'
        else:
            status = 'APROVED'
    finally:
        return status

def verifyStudentName(query_name:str,url_id:int):
    valid = False
    try:
        student = Student.objects.get(name=query_name)
    except:
        valid = True
    else:
        if student.id == url_id:
            valid = True
    return valid

def verifyUserName(query_name:str,url_id:int):
    valid = False
    try:
        user = User.objects.get(username=query_name)
    except:
        valid = True
    else:
        if user.id == url_id:
            valid = True
    return valid

def pages_display(page:Page,paginator:Paginator):
    pages_to_show = []
    if page.has_other_pages():
        if page.has_previous() and page.number >= 6:
            for i in range(1,6):
                pages_to_show.insert(0,page.number-i)
        elif page.has_previous():
            for i in range(1,page.number):
                pages_to_show.append(i)
        
        pages_to_show.append(page.number)
        
        if page.has_next() and (paginator.num_pages - page.number) > 5:
            for i in range(1,6):
                pages_to_show.append(page.number+i)
            pages_to_show.append("..")
            pages_to_show.append(paginator.num_pages)
        elif page.has_next():
            for i in range(1,(paginator.num_pages - page.number)+1):
                pages_to_show.append(page.number+i)
    return pages_to_show

def addFilterToQuery(inital_query:str,filters:dict,order_by:str):
    new_query = inital_query
    new_query += ' where'
    for key,value in filters.items():
        new_query += f" {key}='{value}' &&"
    new_query = new_query.removesuffix('&&')
    new_query += f' order by {order_by};'
    return new_query

def isDefaultPass(user:User):
    default_pass = 'default'
    return check_password(default_pass,user.password)