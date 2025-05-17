# notes/tests.py
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import User
from .models import Note

class NoteTests(APITestCase):
    def setUp(self):
        # Create a user and obtain JWT token
        self.user = User.objects.create_user(user_email='test@example.com', user_name='Test', password='testpass')
        token_response = self.client.post(reverse('token_obtain_pair'),
                                          {'user_email': 'test@example.com', 'password': 'testpass'},
                                          format='json')
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        token = token_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_unauthorized_create(self):
        # Ensure no token = unauthorized
        self.client.credentials()  # remove auth
        response = self.client.post('/api/notes/', {'note_title': 'X', 'note_content': 'Y'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_note_authenticated(self):
        data = {'note_title': 'Note1', 'note_content': 'This is note content.'}
        response = self.client.post('/api/notes/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 1)
        self.assertEqual(Note.objects.get().note_title, 'Note1')

    def test_get_notes_list(self):
        # Create two notes for this user
        Note.objects.create(user=self.user, note_title='Note1', note_content='Content1')
        Note.objects.create(user=self.user, note_title='Note2', note_content='Content2')
        response = self.client.get('/api/notes/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_note_detail(self):
        note = Note.objects.create(user=self.user, note_title='Note1', note_content='Content1')
        response = self.client.get(f'/api/notes/{note.note_id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['note_title'], 'Note1')

    def test_update_note(self):
        note = Note.objects.create(user=self.user, note_title='Note1', note_content='Content1')
        data = {'note_title': 'Updated', 'note_content': 'Updated content.'}
        response = self.client.put(f'/api/notes/{note.note_id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        note.refresh_from_db()
        self.assertEqual(note.note_title, 'Updated')

    def test_delete_note(self):
        note = Note.objects.create(user=self.user, note_title='Note1', note_content='Content1')
        response = self.client.delete(f'/api/notes/{note.note_id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Note.objects.count(), 0)

    def test_cannot_access_others_note(self):
        # Create a note for another user and ensure current user cannot see it
        other_user = User.objects.create_user(user_email='other@example.com', user_name='Other', password='pass2')
        note_other = Note.objects.create(user=other_user, note_title='Other Note', note_content='...')
        response = self.client.get(f'/api/notes/{note_other.note_id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)