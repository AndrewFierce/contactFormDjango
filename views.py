from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from .models import Subscribers
from .forms import NameForm

def index(request):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		email = request.POST.get('sender', '')
		your_name = request.POST.get('your_name', '')
		subject = request.POST.get('subject', '')
		description = request.POST.get('message', '')
		subscribeEmail = ""
		toEmail = "your@email.com"
		# create a form instance and populate it with data from the request:
		form = NameForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			for validEmail in Subscribers.objects.values('email', 'confirmation').filter(email=email,):
				subscribeEmail = validEmail['email']
				confirmation = validEmail['confirmation']
			if subscribeEmail == "":
				random = get_random_string(length=10)
				subscribers = Subscribers.objects.create(email=email, randomkey = random)
				subscribers.save()
				# send_mail('Confirmation', 'Hello!\nDear, '+your_name+'.\n For confirm your e-mail, follow the link below.:\n'+request.build_absolute_uri('') + 'confirmation/' + email + '/' + random, None, [email], fail_silently=False)
				print(request.build_absolute_uri('') + 'confirmation/' + email + '/' + random)
				# send_mail(subject+' no confirmation', 'User ' + your_name + ' send you next message:\n\n'+description, None, [email], fail_silently=False)
				return render(request, 'success.html', context={'name':your_name, 'message':'Пройдите, пожалуйста, по ссылке, отправленной Вам в сообщении, чтобы доказать, что Вы реальный пользователь.'},)
			elif subscribeEmail != "" and confirmation == True:
				# send_mail(subject, your_name + " send you next message:\n\n" + description, None, [toEmail], fail_silently=False)
				return render(request, 'success.html', context={'name':your_name, 'message':'Спасибо за Ваше обращение! Мы ответим на Ваше сообщение в ближайшее время!'},)
			elif subscribeEmail != "" and confirmation != True:
				return render(request, 'success.html', context={'name':your_name, 'message':'Пройдите, пожалуйста, по ссылке, отправленной Вам в сообщении ранее, чтобы доказать, что Вы реальный пользователь.'},)
	# if a GET (or any other method) we'll create a blank form
	else:
		form = NameForm()
	return render(request, 'name.html', {'form': form})

def confirmation(request, email = None, random = None):
	try:
		subscribers = Subscribers.objects.get(email=email, randomkey=random)
	except Subscribers.DoesNotExist:
		return render(request, 'confirmation.html', context={'email':'Почтовый ящик '+email+' не был подтвержден. Пожалуйста, не меняйте адрес ссылки!'},)
	if str(subscribers.email) != str(email) or str(subscribers.randomkey) != str(random):
		return render(request, 'confirmation.html', context={'email':'Почтовый ящик '+email+' не был подтвержден. Пожалуйста, не меняйте адрес ссылки!'},)
	else:
		subscriber = Subscribers.objects.filter(email=email,)
		for subscribe in subscriber:
			subscribe.confirmation = True
			subscribe.save()
	return render(request, 'confirmation.html', context={'email':'Почтовый ящик '+email+' успешно был подтвержден'},)