import pytest
from unittest.mock import patch, MagicMock
import subprocess
import platform
import io
import sys
from NetRe import get_windows_wifi, get_macos_wifi, get_linux_wifi, main

def test_get_windows_wifi_success(mocker):
    # Mock subprocess.check_output in the NetRe module
    mock_check = mocker.patch("NetRe.subprocess.check_output")
    mock_check.side_effect = [
        b"Profiles on interface Wi-Fi:\n\nGroup policy profiles (read only)\n---------------------------------\n    <None>\n\nUser profiles\n-------------\n    All User Profile     : Home-WiFi\n",
        b"Profile Home-WiFi on interface Wi-Fi:\n\nSecurity settings\n-----------------\n    Key Content            : password123\n"
    ]
    
    results = get_windows_wifi()
    assert len(results) == 1
    assert results[0]["ssid"] == "Home-WiFi"
    assert results[0]["password"] == "password123"

def test_get_macos_wifi_success(mocker):
    mock_check = mocker.patch("NetRe.subprocess.check_output")
    mock_check.side_effect = [
        b"Preferred networks on en0:\n  Office-WiFi\n",
        b"secure_password\n"
    ]
    
    results = get_macos_wifi()
    assert len(results) == 1
    assert results[0]["ssid"] == "Office-WiFi"
    assert results[0]["password"] == "secure_password"

def test_get_linux_wifi_success(mocker):
    mock_check = mocker.patch("NetRe.subprocess.check_output")
    mock_check.side_effect = [
        b"Linux-WiFi\n",
        b"linux_pass\n"
    ]
    
    results = get_linux_wifi()
    assert len(results) == 1
    assert results[0]["ssid"] == "Linux-WiFi"
    assert results[0]["password"] == "linux_pass"

def test_main_unsupported_os(mocker):
    mocker.patch("platform.system", return_value="UnknownOS")
    # Mock sys.argv to avoid conflicts with pytest args
    mocker.patch("sys.argv", ["NetRe.py", "--silent"])
    
    captured_output = io.StringIO()
    sys.stdout = captured_output
    
    try:
        main()
    finally:
        sys.stdout = sys.__stdout__
        
    assert "is not supported" in captured_output.getvalue()

def test_main_windows_flow(mocker):
    mocker.patch("platform.system", return_value="Windows")
    mocker.patch("NetRe.get_windows_wifi", return_value=[{"ssid": "TestSSID", "password": "TestPassword"}])
    mocker.patch("sys.argv", ["NetRe.py", "--silent"])
    
    captured_output = io.StringIO()
    sys.stdout = captured_output
    
    try:
        main()
    finally:
        sys.stdout = sys.__stdout__
        
    output = captured_output.getvalue()
    assert "TestSSID" in output
    assert "TestPassword" in output
