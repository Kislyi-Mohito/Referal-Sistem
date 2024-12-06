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

'''я хочу чтоб он проверял значение логина со зночение в таблице Users'''


def login(request):                                             #настройка авторизаци

    login = request.POST.get('login')
    password = request.POST.get('password')
    button = request.POST.get('send')
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
        if button == 'send':
            cursor.execute(f"SELECT name FROM Users WHERE name = '{login}';")
            rows = cursor.fetchall()
            name = ""           #в эту переменную я запишу найденное имя чтоб можно было вывести

################тестовый блок######################################################################
            #тут какойт то косяк
            # имя дальше не проходит а так система рабочая
            cursor.execute(f"SELECT * FROM Users WHERE name = 'denis';")
            test = cursor.fetchall()
            login = str(test)
            login = login[2:-2]  # тут записывается строка 48, 'denis', '123456 ', ' ', '00000 ' я ее запишу в список
            '''
            #идея состоит в лейдующем,
            # 1.  я для началя сдеаю срез строки чтоб там небыло скобок [()],
            # а дальше запишу строку в список при помощи азделителя ',' и буду обращаться по индексам
            # 2. нужно этот список записать в Словарь session
            '''
            #пробую записать в список
            #z = line.split(';')  функция разделения и записи  line - это строка в моем случает это или логин или тест

            bd = login.split(',')    # подумай как лучше назвать переменную где хранится весь массив
            login = bd[1][2:-1] #тут я присваиваю логину имя 'denis' и тут же делаю срез скобок и получается denis

###################################################################################################################

            for row in rows:
                name = str(row)

                name = name[2:-3]       # тут я получаю уже иямя без скобок с которым можно работать

#БЛОК ПРОВЕРКИ ПАРОЛЯ

            #тут я ввожу проверку на пустую строку и есть ли логин
            if name != '' and password == '1':
                request.session['auth'] = '1'           #тут должен быть реализован переход на страницу если логин и пароль подходят
                return redirect('home')
            # реализация подсказки для пароля


            elif name != '':
                data = {'text': f'{name} есть в списке, ваш парооль {bd[4]}'}
            else:

                data = {'text': f'{login} вы не зарегестрированны'}


    return render(request, 'login.html', context=data)