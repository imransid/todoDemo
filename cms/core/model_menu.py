from django.db import models
from django.contrib.auth import get_user_model
from mptt.models import MPTTModel, TreeForeignKey


class NavMenu(models.Model):
    """A menu created by a user."""
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="menus"
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Each user can only have one menu per slug
        unique_together = ('user', 'slug')
        ordering = ['name']

    def __str__(self):
        return self.name


class NavMenuItem(MPTTModel):
    """
    Represents a single entry in a menu.  Inheriting from MPTTModel adds
    `lft`, `rght`, `tree_id` and `level` fields to efficiently store the
    tree structure:contentReference[oaicite:2]{index=2}.
    """
    menu = models.ForeignKey(
        NavMenu,
        on_delete=models.CASCADE,
        related_name="items"
    )
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True, null=True)
    # Self‑referencing parent field enables unlimited nesting
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    # Use order to control sibling ordering
    order = models.PositiveIntegerField(default=0)
    visible = models.BooleanField(default=True)

    class MPTTMeta:
        # When inserting or moving nodes, order siblings by this field
        order_insertion_by = ['order']

    class Meta:
        # Querysets are ordered by tree_id and lft so they follow
        # depth‑first ordering:contentReference[oaicite:3]{index=3}.
        ordering = ['tree_id', 'lft']

    def __str__(self):
        return self.name
