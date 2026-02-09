import pytest
from unittest.mock import patch, MagicMock
import subprocess
import platform
from NetRe import get_windows_wifi, get_macos_wifi, get_linux_wifi

def test_get_windows_wifi_success(mocker):
    # Mock subprocess output for netsh profiles
    mocker.patch("subprocess.check_output", side_effect=[
        b"Profiles on interface Wi-Fi:\n\nGroup policy profiles (read only)\n---------------------------------\n    <None>\n\nUser profiles\n-------------\n    All User Profile     : Home-WiFi\n",
        b"Profile Home-WiFi on interface Wi-Fi:\n\nSecurity settings\n-----------------\n    Key Content            : password123\n"
    ])
    
    results = get_windows_wifi()
    assert len(results) == 1
    assert results[0]["ssid"] == "Home-WiFi"
    assert results[0]["password"] == "password123"

def test_get_macos_wifi_success(mocker):
    # Mock networksetup and security output
    mocker.patch("subprocess.check_output", side_effect=[
        b"Preferred networks on en0:\n  Office-WiFi\n",
        b"secure_password\n"
    ])
    
    results = get_macos_wifi()
    assert len(results) == 1
    assert results[0]["ssid"] == "Office-WiFi"
    assert results[0]["password"] == "secure_password"

def test_get_linux_wifi_success(mocker):
    # Mock nmcli output
    mocker.patch("subprocess.check_output", side_effect=[
        b"Linux-WiFi\n",
        b"linux_pass\n"
    ])
    
    results = get_linux_wifi()
    assert len(results) == 1
    assert results[0]["ssid"] == "Linux-WiFi"
    assert results[0]["password"] == "linux_pass"

def test_unsupported_os(mocker):
    with patch("platform.system", return_value="UnknownOS"):
        # Since main() handles the print, we'd test logic here if exported
        pass
