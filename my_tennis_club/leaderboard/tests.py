from django.test import TestCase
from django.contrib.auth.models import User
from leaderboard.models import Leaderboard
from django.urls import reverse

class ShowLeaderTestCase(TestCase):
    def setUp(self):
        # 創建12個 user
        self.users = []
        self.leaderboard_entries = []

        for i in range(1, 13):
            user = User.objects.create_user(username=f'testuser{i}', password=f'testpasswordforleaderboard{i}')
            self.users.append(user)

            leaderboard_entry = Leaderboard.objects.create(username=user.username, bestscore=10000 - i)
            self.leaderboard_entries.append(leaderboard_entry)

    def test_show_leader_authenticated_user(self):
        # 登入為第12名的 user
        self.client.force_login(self.users[11])

        response = self.client.get(reverse('leaderboard_url:show_leader'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'leaderboard.html')
        self.assertContains(response, f'{12}')
        self.assertContains(response, f'testuser12')
        self.assertContains(response, f'{10000 - 12}')

        # 檢查頁面中是否包含正确的排行信息
        for i in range(1, 11):
            self.assertContains(response, f'{i}')
            self.assertContains(response, f'testuser{i}')
            self.assertContains(response, f'{10000 - i}')

    def test_show_leader_unauthenticated_not_user(self):
        # 測試未登入是否正確重導向
        self.client.logout()
        response = self.client.get(reverse('leaderboard_url:show_leader'))
        self.assertEqual(response.status_code, 302) # 302 表重定址
        self.assertRedirects(response, reverse('login') + f'?next={reverse("leaderboard_url:show_leader")}')

