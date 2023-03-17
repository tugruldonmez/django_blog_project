from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        #return reverse('post-detail',kwargs={'pk':self.pk})#yayınlanan gönderiyi post_details'iyle bağlar.Bağlanmazsa gönderiyi paylaşır ama url patterns hatası verir(post oluşturuldu sonra hangi sayfanın açılacağına karar veremedi)
        return reverse('blog-home')#bu da gönderi yayınlandıktan sonra anasayfaya yönlendiriyor