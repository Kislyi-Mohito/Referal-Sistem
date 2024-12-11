from typing import Set

from django.shortcuts import render, redirect
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


            data = {"text": request.session['bd']}
    return render(request, 'index.html', context=data)






def set_session(request):                             #установить сеанс

    # Устанавливаем значение в сессии
    request.session['auth'] = '0'
    request.session['registr'] = '0'
    request.session['bd'] = '0'



    return redirect('home')

def get_session(request):
    # Проверяем, установлено ли значение в сессии
    if request.session['auth'] != '1':
        return redirect('/login/')  # Перенаправляем на установку сессии
    my_value = request.session['auth']


    return render(request, 'session_template.html', {'my_value': my_value})

'''я хочу чтоб он проверял значение логина со зночение в таблице Users'''


def login(request):                                             #настройка авторизаци

    login = request.POST.get('login')
    password = request.POST.get('password')
    button_send = request.POST.get('send')
    button_reg = request.POST.get('reg')
    data = {'text':''}


    if login == '1':
        request.session['auth'] = '1'
        return redirect('home')
    else:
        request.session['auth'] = '0'

        if login != '':
            data = {'text': f'{login} не авторизованны'}

#БЛОК ПОИСКА ПАРОЛЯ

    #произвожу поиск по логину в БД
    with connection.cursor() as cursor:
        #Переход на страницу регистрации
        if button_reg == 'reg':
            request.session['regist'] = '1'
            return redirect('reg')

        #Проверка авторзаци
        if button_send == 'send' and login != '':
            cursor.execute(f"SELECT * FROM Users WHERE name = '{login}';")
            rows = cursor.fetchall()
            bd = rows
            if bd:
                bd = bd[0]
                name = bd[1]     #Это для проверки



                if f'{password}' == f'{bd[4].strip()}':
                    request.session['bd'] = bd
                    request.session['auth'] = '1'  # тут должен быть реализован переход на страницу если логин и пароль подходят
                    return redirect('home')
                else:
                    name = f'че то  не сходится {len(password)} - {len(bd[4].strip())}'
                data = {'text': f'{bd[1]} есть в списке, ваш парооль {bd[4]}'}
            else:

                data = {'text': f'{login} вы не зарегестрированны'}







    return render(request, 'login.html', context=data)


def reg(request):
    #Проверка на зарегестрированного пользователя
    if request.session['auth'] == '1':
        return redirect('home')

    #Получение входных данных
    login = request.POST.get('login')
    password = request.POST.get('password')
    invait = request.POST.get('invait', '0')
    button_send = request.POST.get('send')
    button_auth = request.POST.get('auth')
    data = {}

    if button_auth == 'auth':
        return redirect('/login/')

        #Ввод входных данных в таблицу

        #Запись в таблицу данных
    with connection.cursor() as cursor:
        if button_send == 'send':

            # проверка верности инвайт кода
            # if len(invait) == 6:
            #     data = {'text': 'прошло'}
            # else:
            #     data = {'text': 'не подходящий инвайт'}

             #Генерация собственного инвайта
            ma_invait = randint(100000, 1000000)

            # Запись в таблицу данных
            cursor.execute(f"insert into Users (name, my_invait, pass, invait) values ('{login}','{ma_invait}','{password}', '{invait}')")

        #вывод данных для теста
        cursor.execute(f"select *from Users")
        rowss = cursor.fetchall()
        for row in rowss:
            table = f'{row[1]}-{row[2]}-{row[3]}-{row[4]}'

        data = {'text': table}


    #запись в таблицу

    return render(request, 'registr.html', context= data)