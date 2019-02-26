# contactFormDjango
Контактная форма для Django с подтверждением по e-mail и записи в базу пользователя.
Когда пользователь сайта пытается заказать обратную связь, то формируется сообщение с сылкой, пройдя по которой, пользователь подтверждает, что он реальный пользователь, а не бот.
В форме присутствует capcha, поэтому необходимо ее установить в django.
Инструкция по тому как это можно сделать описана здесь:
https://django-simple-captcha.readthedocs.io/en/latest/usage.html
