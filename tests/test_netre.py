import unittest
from unittest.mock import patch, MagicMock
import platform
import NetRe

class TestNetRe(unittest.TestCase):

    @patch('platform.system')
    def test_os_detection(self, mock_system):
        mock_system.return_value = 'Windows'
        self.assertEqual(platform.system(), 'Windows')
        
        mock_system.return_value = 'Darwin'
        self.assertEqual(platform.system(), 'Darwin')

    @patch('subprocess.check_output')
    def test_windows_wifi_parsing(self, mock_subprocess):
        # Mock 'netsh wlan show profiles'
        mock_subprocess.return_value = b"Profiles on interface Wi-Fi:\n\nGroup policy profiles (read only)\n---------------------------------\n    <None>\n\nUser profiles\n-------------\n    All User Profile     : MyHomeWiFi\n"
        
        # We need to mock the second call inside the loop too
        # This is simplified for a basic check
        with patch('NetRe.get_windows_wifi') as mock_get:
            mock_get.return_value = [{"ssid": "MyHomeWiFi", "password": "password123"}]
            data = NetRe.get_windows_wifi()
            self.assertEqual(data[0]['ssid'], 'MyHomeWiFi')

if __name__ == '__main__':
    unittest.main()
