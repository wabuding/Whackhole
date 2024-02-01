from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class MembersTestCase(TestCase):
    def setUp(self):
        # 在每個測試執行前建立一個使用者
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_members_view(self):
        # 測試 members view
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_register_view(self):
        # 測試 register view
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        # 登入成功
        response = self.client.post(reverse('login_view'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {'alertMessage': '登入成功'})

        # 登入失敗
        # case1: 使用者名稱正確, 密碼錯誤
        response = self.client.post(reverse('login_view'), {'username': 'testuser', 'password': 'testpasswors'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {'alertMessage': '登入失敗'})

        # case2: 使用者名稱錯誤, 密碼正確
        response = self.client.post(reverse('login_view'), {'username': 'testusee', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {'alertMessage': '登入失敗'})

        # case3: GET
        response = self.client.get(reverse('login_view'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {'alertMessage': '登入失敗'})

    def test_register_view_create_user(self):
        # 測試註冊成功的情況
        response = self.client.post(reverse('register_view'), {'username': 'newuser', 'password1': 'newpasswordfortest001', 'password2': 'newpasswordfortest001'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {'alertMessage': '建立成功'})

        # 測試註冊失敗的情況
        
        # case1.1: 使用者名稱已存在, 相同(失敗)
        response = self.client.post(reverse('register_view'), {'username': 'testuser', 'password1': 'fortestinregister001', 'password2': 'fortestinregister001'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {'alertMessage': ' 使用者名稱已存在 '})

        # case1.2: 使用者名稱已存在, 差一個字(成功)
        response = self.client.post(reverse('register_view'), {'username': 'testusew', 'password1': 'fortestinregister001', 'password2': 'fortestinregister001'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {'alertMessage': '建立成功'})

        # case1.3: 使用者名稱已存在, 多一個字(成功)
        response = self.client.post(reverse('register_view'), {'username': 'testuser1', 'password1': 'fortestinregister001', 'password2': 'fortestinregister001'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {'alertMessage': '建立成功'})

        # case2: 密碼過於普通
        response = self.client.post(reverse('register_view'), {'username': 'newuser001', 'password1': 'newpassword', 'password2': 'newpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {'alertMessage': ' 密碼太過普通 '})

        # case3.1: 再次輸入密碼與密碼不同, 錯最後一個字
        response = self.client.post(reverse('register_view'), {'username': 'testuser001', 'password1': 'fortestinregister001', 'password2': 'fortestinregister002'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {'alertMessage': ' 再次輸入密碼與密碼不同 '})

        # case3.2: 再次輸入密碼與密碼不同, 多一個字
        response = self.client.post(reverse('register_view'), {'username': 'testuser001', 'password1': 'fortestinregister001', 'password2': 'fortestinregister0011'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {'alertMessage': ' 再次輸入密碼與密碼不同 '})

        # case4.1: 密碼過短, 7個字(失敗)
        response = self.client.post(reverse('register_view'), {'username': 'testuser001', 'password1': 'afwqry1', 'password2': 'afwqry1'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {'alertMessage': ' 密碼至少8個字 '})

        # case4.2: 密碼過短, 8個字(成功)
        response = self.client.post(reverse('register_view'), {'username': 'testuser001', 'password1': 'afwqry12', 'password2': 'afwqry12'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {'alertMessage': '建立成功'})

        # case5: GET
        response = self.client.get(reverse('register_view'), {'username': 'newuser', 'password1': 'newpasswordfortest001', 'password2': 'newpasswordfortest001'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {'alertMessage': '建立失敗'})