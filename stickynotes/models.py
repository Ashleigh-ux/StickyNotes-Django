from django.db import models

class Note(models.Model):
    """
    Represents a single sticky note with a title and content.
    """

    title = models.CharField(max_length=120, help_text="Enter a short title for the note.")
    content = models.TextField(help_text="Enter the content of your note.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = "Note"
        verbose_name_plural = "Notes"

    def __str__(self):
        """Return a readable string representation of the note."""
        return f"{self.title} ({self.updated_at:%Y-%m-%d %H:%M})"

