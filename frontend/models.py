from django.db import models


class Page(models.Model):
    """
    Modelo para páginas editables (Inicio, Nosotros, Contacto, etc.)
    Permite a los admins editar contenido sin tocar código
    """
    title = models.CharField(max_length=200, unique=True, verbose_name="Título")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug (URL)")
    content = models.TextField(verbose_name="Contenido HTML", help_text="Contenido en HTML")
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        verbose_name="Meta Descripción",
        help_text="Para SEO (máx 160 caracteres)"
    )
    is_active = models.BooleanField(default=True, verbose_name="¿Activa?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creada el")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizada el")

    class Meta:
        verbose_name = "Página"
        verbose_name_plural = "Páginas"
        ordering = ['title']

    def __str__(self):
        return self.title
