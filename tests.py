# tests.py
from unittest import TestCase, main as unittest_main, mock
from app import app
from bson.objectid import ObjectId

sample_video_id = ObjectId('5da005918edd63f14c355675')
sample_video = {
    'title': 'Cat Videos',
    'description': 'Cats acting weird',
    'videos': [
        'https://youtube.com/embed/hY7m5jjJ9mM',
        'https://www.youtube.com/embed/CQ85sUNBK7w'
    ]
}
sample_form_data = {
    'title': sample_video['title'],
    'description': sample_video['description'],
    'videos': '\n'.join(sample_video['videos'])
}

class videosTests(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test the videos homepage."""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'videos', result.data)

    def test_new(self):
        """Test the new video creation page."""
        result = self.client.get('/videos/new')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'New video', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_video(self, mock_find):
        """Test showing a single video."""
        mock_find.return_value = sample_video

        result = self.client.get(f'/videos/{sample_video_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Cat Videos', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_video(self, mock_find):
        """Test editing a single video."""
        mock_find.return_value = sample_video

        result = self.client.get(f'/videos/{sample_video_id}/edit')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Cat Videos', result.data)

    @mock.patch('pymongo.collection.Collection.update_one')
    def test_update_video(self, mock_update):
        result = self.client.post(f'/videos/{sample_video_id}', data=sample_form_data)

        self.assertEqual(result.status, '302 FOUND')
        mock_update.assert_called_with({'_id': sample_video_id}, {'$set': sample_video})

    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_delete_video(self, mock_delete):
        form_data = {'_method': 'DELETE'}
        result = self.client.post(f'/videos/{sample_video_id}/delete', data=form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_delete.assert_called_with({'_id': sample_video_id})

if __name__ == '__main__':
    unittest_main()
