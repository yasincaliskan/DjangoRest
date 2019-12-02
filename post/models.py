from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=120)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    created = models.DateField(editable=False)
    modified = models.DateField()
    slug = models.SlugField(unique=True, max_length=150, editable=False)
    image = models.ImageField(upload_to="", null=True, blank=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='modified_by')

    def __str__(self):
        return self.title

    def get_slug(self):
        slug = slugify(self.title.replace("ı", "i"))
        unique = slug
        number = 1

        while Post.objects.filter(slug = unique).exists():
            unique = '{}-{}'.format(slug,number)
            number += 1

        return unique

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now() # ilk oluşturulduğun id değeri olmadığından oluşturma anını tutar.

        self.modified = timezone.now() # her bir değişiklik olduğunda o tarihi tutar.
        self.slug = self.get_slug()
        return super(Post, self).save(*args, **kwargs)

