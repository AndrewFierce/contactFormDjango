from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from .models import Subscribers
from .forms import NameForm

# функция отображения формы
def index(request):
	# если получены данные методом POST
	if request.method == 'POST':
		# Получаем переменные полей с формы обратной связи
		email = request.POST.get('sender', '')
		your_name = request.POST.get('your_name', '')
		subject = request.POST.get('subject', '')
		description = request.POST.get('message', '')
		subscribeEmail = ""
		toEmail = "your@email.com"
		# создаем экземпляр формы и заполняем его данными из запроса:
		form = NameForm(request.POST)
		# Проверяем заполненность формы:
		if form.is_valid():
			# Ищем подписчиков из базы данных Subscribers и проверяем подтверждение
			for validEmail in Subscribers.objects.values('email', 'confirmation').filter(email=email,):
				subscribeEmail = validEmail['email']
				confirmation = validEmail['confirmation']
			# Если пользователь впервые запрашивает обратную связь
			if subscribeEmail == "":
				# формируем ключ
				random = get_random_string(length=10)
				# создаем нового неподтвержденного пользователя в БД
				subscribers = Subscribers.objects.create(email=email, randomkey = random)
				# сохраняем
				subscribers.save()
				# формируем ссылку для подтверждения почтового ящика и отправляем ее пользователю на почту
				send_mail('Confirmation', 'Hello!\nDear, '+your_name+'.\n For confirm your e-mail, follow the link below.:\n'+request.build_absolute_uri('') + 'confirmation/' + email + '/' + random, None, [email], fail_silently=False)
				# отправляем нам сообщение с добавлением к теме 'no confirmation', чтобы в будущем отсеивать неподтвержденные ящики
				send_mail(subject+' no confirmation', 'User ' + your_name + ' send you next message:\n\n'+description, None, [email], fail_silently=False)
				# перенаправляем на страницу, где указываем пользователю на необходимость подтверждения почтового ящика, чтобы доказать, что он не спамер
				return render(request, 'success.html', context={'name':your_name, 'message':'Пройдите, пожалуйста, по ссылке, отправленной Вам в сообщении, чтобы доказать, что Вы реальный пользователь.'},)
			# если пользователь ранее подтверждал свой почтовый ящик, то просто отправляем сообщение в чистом виде и перенаправляем его на страницу с благодарностью
			elif subscribeEmail != "" and confirmation == True:
				send_mail(subject, your_name + " send you next message:\n\n" + description, None, [toEmail], fail_silently=False)
				return render(request, 'success.html', context={'name':your_name, 'message':'Спасибо за Ваше обращение! Мы ответим на Ваше сообщение в ближайшее время!'},)
			# если почтовый адрес не подтвержден, то сообщаем о необходимости его подтвердить
			elif subscribeEmail != "" and confirmation != True:
				return render(request, 'success.html', context={'name':your_name, 'message':'Пройдите, пожалуйста, по ссылке, отправленной Вам в сообщении ранее, чтобы доказать, что Вы реальный пользователь.'},)
	# если метод GET (или любой другой метод) мы создадим пустую форму
	else:
		form = NameForm()
	return render(request, 'name.html', {'form': form})

# функция подтверждения почтового ящика
def confirmation(request, email = None, random = None):
	# пытаемся получить e-mail пользователя с ключом
	try:
		subscribers = Subscribers.objects.get(email=email, randomkey=random)
	# если пользователь не был найдем, возвращаем его на страницу отказа подтверждения
	except Subscribers.DoesNotExist:
		return render(request, 'confirmation.html', context={'email':'Почтовый ящик '+email+' не был подтвержден. Пожалуйста, не меняйте адрес ссылки!'},)
	# если ключ или пользователь не соответствуют действительность, например, злоумышленник пытается подобрать ключи
	if str(subscribers.email) != str(email) or str(subscribers.randomkey) != str(random):
		return render(request, 'confirmation.html', context={'email':'Почтовый ящик '+email+' не был подтвержден. Пожалуйста, не меняйте адрес ссылки!'},)
	# если ссылка соответствует действительность, то подтверждаем почтовый ящик в базе и отправляем пользователя на страницу подтверждения
	else:
		subscriber = Subscribers.objects.filter(email=email,)
		for subscribe in subscriber:
			subscribe.confirmation = True
			subscribe.save()
	return render(request, 'confirmation.html', context={'email':'Почтовый ящик '+email+' успешно был подтвержден'},)
