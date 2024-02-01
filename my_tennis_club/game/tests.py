from django.test import TestCase, Client
from django.contrib.auth.models import User
from datetime import datetime
from django.urls import reverse
from record.models import PlayRecord
from leaderboard.models import Leaderboard
import json

class GameViewsTestCase(TestCase):
    def setUp(self):
        # 創建測試 user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_game_main_authenticated_user(self):
        # 測試已登入 user 
        self.client.force_login(self.user)
        response = self.client.get(reverse('game:whackhole'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'whack_hole.html')
        self.assertContains(response, 'testuser')

    def test_game_main_authenticated_not_user(self):
        # 測試未登入是否正確重導向
        self.client.logout()
        response = self.client.get(reverse('game:whackhole'))
        self.assertEqual(response.status_code, 302) # 302 表重定址
        self.assertRedirects(response, reverse('login') + f'?next={reverse("game:whackhole")}')

    def test_logout_view(self):
        # 測試登出
        self.client.force_login(self.user)
        response = self.client.post(reverse('game:logout_view'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['alertMessage'], '成功登出')

    def test_start_game_authenticated_user(self):
        # 測試 start_game
        self.client.force_login(self.user)
        response = self.client.get(reverse('game:game_start'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game_main.html')
        self.assertContains(response, 'score')

    def test_start_game_unauthenticated_user(self):
        # 測試未登入是否正確重導向
        self.client.logout()
        response = self.client.get(reverse('game:game_start'))
        self.assertEqual(response.status_code, 302)  # 302 表重定址
        self.assertRedirects(response, reverse('login') + f'?next={reverse("game:game_start")}')

    def test_game_end_authenticated_user_update_best_score(self):
        # 測試 game_end
        self.client.force_login(self.user)
        response = self.client.post(reverse('game:game_end'), json.dumps({'score': 100}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['message'], 'Score saved successfully.')

        response = self.client.post(reverse('game:game_end'), json.dumps({'score': 150}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['message'], 'Score saved successfully.')

        # 檢查 PlayRecord 和 Leaderboard 是否正確保存
        play_record = PlayRecord.objects.get(username='testuser', score=150)
        self.assertIsNotNone(play_record)
        leaderboard = Leaderboard.objects.get(username='testuser', bestscore=150)
        self.assertEqual(leaderboard.bestscore, 150)

    def test_game_end_authenticated_user(self):
        # 測試 game_end
        self.client.force_login(self.user)
        response = self.client.post(reverse('game:game_end'), json.dumps({'score': 100}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['message'], 'Score saved successfully.')

        # 檢查 PlayRecord 和 Leaderboard 是否正確保存
        play_record = PlayRecord.objects.get(username='testuser', score=100)
        self.assertIsNotNone(play_record)
        leaderboard = Leaderboard.objects.get(username='testuser')
        self.assertEqual(leaderboard.bestscore, 100)

    def test_game_end_invalid_score(self):
        # 測試無效分數
        self.client.force_login(self.user)
        response = self.client.post(reverse('game:game_end'), json.dumps({'score': -50}), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['error'], 'Invalid score.')

    def test_game_end_invalid_method(self):
        # GET
        self.client.force_login(self.user)
        response = self.client.get(reverse('game:game_end'))
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['error'], 'Invalid request method.')
