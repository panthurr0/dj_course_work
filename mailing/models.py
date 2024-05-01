from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(verbose_name='контактный email', max_length=150, **NULLABLE, unique=True)
    name = models.CharField(verbose_name='ФИО', max_length=200, **NULLABLE)
    commentary = models.TextField(verbose_name='комментарий', **NULLABLE)

    def __str__(self):
        return f'{self.name} ({self.email})'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Message(models.Model):
    theme = models.CharField(verbose_name='тема письма')
    body = models.CharField(verbose_name='тело письма')

    def __str__(self):
        return f'{self.theme}'

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Mailing(models.Model):
    client = models.ForeignKey(Client, verbose_name='клиент', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, verbose_name='сообщение', on_delete=models.CASCADE)
    first_datetime = models.DateTimeField(verbose_name='дата и время первой отправки рассылки', auto_now_add=True)
    periodicity = models.CharField(verbose_name='периодичность')
    status = models.CharField(verbose_name='status')

    def __str__(self):
        return f'{self.first_datetime}: {self.periodicity}. {self.status}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class MailingTry(models.Model):
    mailing = models.ForeignKey(Mailing, verbose_name='рассылка', on_delete=models.CASCADE)
    last_at = models.DateTimeField(verbose_name='дата и время последней попытки', auto_now_add=True)
    status = models.CharField(verbose_name='статус попытки (успешно / не успешно)')
    code = models.CharField(verbose_name='ответ почтового сервера, если он был')

    def __str__(self):
        return f'{self.last_at}: {self.status} ({self.code})'

    class Meta:
        verbose_name = 'попытка'
        verbose_name_plural = 'попытки'
