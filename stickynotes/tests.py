"""
Automated tests for the Sticky Notes app (Part 2).
Covers model basics and full view behaviour:
- Home page renders and lists notes
- Add/Edit/Delete: both GET and POST flows
- Invalid POST is handled and does not mutate data
"""

from django.test import TestCase
from django.urls import reverse
from .models import Note


class NoteModelTest(TestCase):
    """Basic model tests to ensure fields are saved correctly."""

    @classmethod
    def setUpTestData(cls):
        cls.note = Note.objects.create(
            title="Test Note",
            content="This is a test note."
        )

    def test_note_title_saved(self):
        """Note.title persists correctly."""
        self.assertEqual(self.note.title, "Test Note")

    def test_note_content_saved(self):
        """Note.content persists correctly."""
        self.assertEqual(self.note.content, "This is a test note.")


class NoteViewTest(TestCase):
    """
    View tests for:
    - home (GET)
    - add_note (GET + POST valid/invalid)
    - edit_note (GET + POST valid/invalid)
    - delete_note (GET + POST)
    """

    @classmethod
    def setUpTestData(cls):
        cls.note = Note.objects.create(
            title="View Note",
            content="Original content"
        )

    # -------- Home --------

    def test_home_status_and_lists_note(self):
        """Home should load (200) and include a known title."""
        resp = self.client.get(reverse("home"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "View Note")

    # -------- Add Note --------

    def test_add_note_get(self):
        """Add form should render on GET."""
        resp = self.client.get(reverse("add_note"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "<form", html=False)

    def test_add_note_post_valid_creates_object(self):
        """Valid POST should create a new note and redirect to home."""
        start_count = Note.objects.count()
        resp = self.client.post(
            reverse("add_note"),
            data={"title": "New Note", "content": "Body"},
            follow=False,
        )
        # Should redirect after success
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse("home"))
        self.assertEqual(Note.objects.count(), start_count + 1)
        self.assertTrue(Note.objects.filter(title="New Note").exists())

    def test_add_note_post_invalid_does_not_create(self):
        """
        Invalid POST (e.g., missing title) should re-render the form
        with status 200 and NOT create a new object.
        """
        start_count = Note.objects.count()
        resp = self.client.post(
            reverse("add_note"),
            data={"title": "", "content": "Missing title"},
            follow=False,
        )
        self.assertEqual(resp.status_code, 200)  # stays on form
        self.assertEqual(Note.objects.count(), start_count)
        # Typical Django form error text (won't assert exact wording)
        self.assertContains(resp, "This field is required", html=False)

    # -------- Edit Note --------

    def test_edit_note_get(self):
        """Edit page should render for an existing note."""
        resp = self.client.get(reverse("edit_note", args=[self.note.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "<form", html=False)
        self.assertContains(resp, "Original content")

    def test_edit_note_post_valid_updates_object(self):
        """Valid POST should update the note and redirect to home."""
        resp = self.client.post(
            reverse("edit_note", args=[self.note.id]),
            data={"title": "Updated Title", "content": "Updated content"},
            follow=False,
        )
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse("home"))
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "Updated Title")
        self.assertEqual(self.note.content, "Updated content")

    def test_edit_note_post_invalid_keeps_form(self):
        """
        Invalid POST should not update the object and should re-render the form.
        """
        original_title = self.note.title
        resp = self.client.post(
            reverse("edit_note", args=[self.note.id]),
            data={"title": "", "content": "No title"},
            follow=False,
        )
        self.assertEqual(resp.status_code, 200)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, original_title)
        self.assertContains(resp, "This field is required", html=False)

    # -------- Delete Note --------

    def test_delete_note_get(self):
        """Delete confirmation page should render."""
        resp = self.client.get(reverse("delete_note", args=[self.note.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Delete", html=False)

    def test_delete_note_post_deletes_object(self):
        """POSTing delete should remove the note and redirect home."""
        resp = self.client.post(reverse("delete_note", args=[self.note.id]))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse("home"))
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())
