from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from record.models import PlayRecord
from datetime import datetime

class ShowRecordTestCase(TestCase):
    def setUp(self):
        # 在每個測試執行前建立一個使用者
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        test_date_1 = datetime(2023, 1, 1, 12, 0, 0)
        test_date_2 = datetime(2023, 1, 1, 13, 0, 0)

        # 在每個測試執行前建立一個 PlayRecord
        self.record_1 = PlayRecord.objects.create(username='testuser', score=999, date=test_date_1)
        self.record_2 = PlayRecord.objects.create(username='testuser', score=899, date=test_date_2)

    def test_show_record_authenticated_user(self):
        # 測試 Record 內容
        self.client.force_login(self.user)

        response = self.client.get(reverse('record_url:show_record'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'play_record.html')
        self.assertContains(response, '999')       # 確認頁面中包含分數
        self.assertContains(response, '2023-01-01 12:00')  # 確認頁面中包含日期
        self.assertContains(response, '899')       # 確認頁面中包含分數
        self.assertContains(response, '2023-01-01 13:00')  # 確認頁面中包含日期
    
    def test_show_record_authenticated_not_user(self):
        # 測試未登入是否正確重導向
        self.client.logout()
        response = self.client.get(reverse('record_url:show_record'))
        self.assertEqual(response.status_code, 302) # 302 表重定址
        self.assertRedirects(response, reverse('login') + f'?next={reverse("record_url:show_record")}')
