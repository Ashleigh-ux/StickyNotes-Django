"""
Automated tests for the Sticky Notes Django application.
These tests confirm that the Note model and all views
(home, add, edit, delete) work correctly.
"""

from django.test import TestCase
from django.urls import reverse
from .models import Note


class NoteModelTest(TestCase):
    """Test that the Note model stores data correctly."""

    def setUp(self):
        """Create a sample note to use in tests."""
        self.note = Note.objects.create(
            title="Test Note",
            content="This is a test note."
        )

    def test_note_title_is_correct(self):
        """Confirm the note title matches what was saved."""
        self.assertEqual(self.note.title, "Test Note")

    def test_note_content_is_correct(self):
        """Confirm the note content matches what was saved."""
        self.assertEqual(self.note.content, "This is a test note.")


class NoteViewTest(TestCase):
    """Test that all main views respond and render properly."""

    def setUp(self):
        """Create a sample note for view tests."""
        self.note = Note.objects.create(
            title="View Note",
            content="Testing the view system."
        )

    def test_home_view_status_code(self):
        """Ensure the home page loads successfully."""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_home_view_displays_note(self):
        """Ensure the home page displays the note title."""
        response = self.client.get(reverse("home"))
        self.assertContains(response, "View Note")

    def test_add_note_view_status_code(self):
        """Ensure the Add Note page loads correctly."""
        response = self.client.get(reverse("add_note"))
        self.assertEqual(response.status_code, 200)

    def test_edit_note_view_status_code(self):
        """Ensure the Edit Note page loads correctly."""
        response = self.client.get(
            reverse("edit_note", args=[self.note.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_note_view_status_code(self):
        """Ensure the Delete Note page loads correctly."""
        response = self.client.get(
            reverse("delete_note", args=[self.note.id])
        )
        self.assertEqual(response.status_code, 200)

