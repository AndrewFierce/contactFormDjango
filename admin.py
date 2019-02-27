from django.contrib import admin
from .models import Subscribers

# Представление списка e-mail пользователей для обратной связи
class SubscribersAdmin (admin.ModelAdmin):
	list_display = ('email', 'confirmation', 'randomkey')

admin.site.register(Subscribers, SubscribersAdmin)
