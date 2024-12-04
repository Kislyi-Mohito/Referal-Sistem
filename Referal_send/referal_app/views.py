from django.shortcuts import render
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from random import randint



def home(request):

    if 'auth' not in request.session:
        return redirect('login/')  # Перенаправляем на установку сессии

    if request.session['auth'] != '1':
        return redirect('login/')  # Перенаправляем на установку сессии


    login = request.POST.get('login',"не вижу")
    password = request.POST.get("password")
    invait = request.POST.get("invait")
    send = request.POST.get('send')
    logout = request.POST.get('logout')

    if logout == 'ok':
        request.session['auth'] == 0
        return redirect('login/')  # Перенаправляем на установку сессии


    with connection.cursor() as cursor:
        ma_invait = randint(100000,1000000)
        if send == 'send':
            cursor.execute(f"insert into Users (name, my_invait, pass, invait) values ('{login}','{ma_invait}','{password}', '{invait}')")
        cursor.execute(f"select *from Users")
        rowss = cursor.fetchall()

        for row in rowss:

            table = f'{row[1]}-{row[2]}-{row[3]}-{row[4]}'


            data = {"text": table}
    return render(request, 'index.html', context=data)




from django.shortcuts import render, redirect

def set_session(request):                             #установить сеанс

    # Устанавливаем значение в сессии
    request.session['auth'] = '0'



    return redirect('home')

def get_session(request):
    # Проверяем, установлено ли значение в сессии
    if request.session['auth'] != '1':
        return redirect('/login/')  # Перенаправляем на установку сессии
    my_value = request.session['auth']


    return render(request, 'session_template.html', {'my_value': my_value})


def login(request):

    login = request.POST.get('login')
    password = request.POST.get('password')
    data = {'text':''}

    with connection.cursor() as cursor:
        cursor.execute(f'SELECT * FROM Users WHERE name = '{login}';')
        rows = cursor.fetchall()

        data = {'text':rows}
    #
    # if login == '1':
    #     request.session['auth'] = '1'
    #     return redirect('home')
    # else:
    #     request.session['auth'] = '0'
    #     if login != '':
    #
    #         data = {'text': f'{login} не авторизованны'}


    return render(request, 'login.html', context=data)