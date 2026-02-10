import pytest
from unittest.mock import patch, MagicMock
import NetRe

def test_get_windows_wifi_success(mocker):
    # Mock subprocess output for netsh profiles
    mocker.patch("NetRe.subprocess.check_output", side_effect=[
        b"Profiles on interface Wi-Fi:\n\nGroup policy profiles (read only)\n---------------------------------\n    <None>\n\nUser profiles\n-------------\n    All User Profile     : Home-WiFi\n",
        b"Profile Home-WiFi on interface Wi-Fi:\n\nSecurity settings\n-----------------\n    Key Content            : password123\n"
    ])
    
    results = NetRe.get_windows_wifi()
    assert len(results) == 1
    assert results[0]["ssid"] == "Home-WiFi"
    assert results[0]["password"] == "password123"

def test_get_macos_wifi_success(mocker):
    # Mock networksetup and security output
    mocker.patch("NetRe.subprocess.check_output", side_effect=[
        b"Preferred networks on en0:\n  Office-WiFi\n",
        b"secure_password\n"
    ])
    
    results = NetRe.get_macos_wifi()
    assert len(results) == 1
    assert results[0]["ssid"] == "Office-WiFi"
    assert results[0]["password"] == "secure_password"

def test_get_linux_wifi_success(mocker):
    # Mock nmcli output
    mocker.patch("NetRe.subprocess.check_output", side_effect=[
        b"Linux-WiFi\n",
        b"linux_pass\n"
    ])
    
    results = NetRe.get_linux_wifi()
    assert len(results) == 1
    assert results[0]["ssid"] == "Linux-WiFi"
    assert results[0]["password"] == "linux_pass"

def test_unsupported_os(mocker):
    mocker.patch("NetRe.platform.system", return_value="UnknownOS")
    # Capturing stdout would be better, but testing the branch logic
    # by ensuring it returns or handles as expected.
    with patch("sys.stdout", new=MagicMock()) as mock_stdout:
        NetRe.main()
        # Verify the error message for unsupported OS was printed
        printed = "".join(call.args[0] for call in mock_stdout.write.call_args_list)
        assert "is not supported" in printed
