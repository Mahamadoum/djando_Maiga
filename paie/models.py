from django.db import models
from django.urls import reverse


class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.file.name


# Manager personnalisé pour les employés actifs
class ActifManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(actif=True)


# Modèle Poste (doit être AVANT Employe)
class Poste(models.Model):
    nom = models.CharField(max_length=100, db_index=True, verbose_name="Название должности")
    slug = models.SlugField(max_length=100, unique=True, db_index=True)

    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse('postes_detail', kwargs={'poste_slug': self.slug})


# Modèle Tag
class Tag(models.Model):
    nom = models.CharField(max_length=100, db_index=True, verbose_name="Навык")
    slug = models.SlugField(max_length=100, unique=True, db_index=True)

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse('tag_detail', kwargs={'tag_slug': self.slug})


# Modèle Employe
class Employe(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Фамилия")
    prenom = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(unique=True, verbose_name="Email")
    salaire = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Зарплата")
    date_embauche = models.DateField(auto_now_add=True, verbose_name="Дата приёма")
    actif = models.BooleanField(default=True, verbose_name="Активен")
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL")
    poste = models.ForeignKey(Poste, on_delete=models.PROTECT, verbose_name="Должность")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Навыки")

    # 👇 NOUVEAU CHAMP PHOTO (AJOUTE CETTE LIGNE)
    photo = models.ImageField(
        upload_to='photos/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name="Фото"
    )

    # Managers
    objects = models.Manager()  # Manager par défaut (tous les employés)
    actifs = ActifManager()  # Manager personnalisé (uniquement les actifs)

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return f"{self.nom} {self.prenom}"

    def get_absolute_url(self):
        return reverse('detail_employe_slug', kwargs={'emp_slug': self.slug})