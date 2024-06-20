# Django-SchoolSystem

A CRUD application made with Django, MySQL, and Bootstrap, emulating a simple school system.

# Details

In this system, you can add students and employees. In the students section, the main features are adding scores and calculating the situation, considering a minimum average of 4.0 for Analysis and a minimum average of 6 to Aproved. In the employees section, you can add two types of employees: ADMINs, who can add and modify students and other employees, and EMPLOYEEs, who can only add and modify students. This software uses the Django Authentication System.

# Preview

If you just want to see the software, you can access this link: [https://ycaro.pythonanywhere.com/](https://ycaro.pythonanywhere.com/). You can log in with the username: 'TEST' and the password: 'default'.

# Installation

1. Download or clone this repository:

```
git clone https://github.com/ycarotrindade/django-schoolsystem.git
```

2. Add your information in **env.example**, then change the filename to **.env**

3. Create a **superuser**:

```
py manage.py createsuperuser
```

4. Migrate the models:
```
py manage.py migrate
```

5. Run the Django built-in server:

```
py manage.py runserver
```
