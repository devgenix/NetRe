import pytest
from unittest.mock import patch, MagicMock
import subprocess
import platform
import json
import os
from NetRe import get_windows_wifi, get_macos_wifi, get_linux_wifi, main

def test_windows_retrieval(mocker):
    mock_output = "All User Profile     : MyWifi\n"
    mock_password_output = "Key Content            : secret123\n"
    
    mocker.patch("subprocess.check_output", side_effect=[
        mock_output.encode("utf-8"),
        mock_password_output.encode("utf-8")
    ])
    
    networks = get_windows_wifi()
    assert len(networks) == 1
    assert networks[0]["ssid"] == "MyWifi"
    assert networks[0]["password"] == "secret123"

def test_macos_retrieval(mocker):
    mock_list = "Preferred networks on en0:\n  MyMacWifi\n"
    mock_pass = "mac_secret\n"
    
    mocker.patch("subprocess.check_output", side_effect=[
        mock_list.encode("utf-8"),
        mock_pass.encode("utf-8")
    ])
    
    networks = get_macos_wifi()
    assert len(networks) == 1
    assert networks[0]["ssid"] == "MyMacWifi"
    assert networks[0]["password"] == "mac_secret"

def test_linux_retrieval(mocker):
    mock_list = "MyLinuxWifi\n"
    mock_pass = "linux_secret\n"
    
    mocker.patch("subprocess.check_output", side_effect=[
        mock_list.encode("utf-8"),
        mock_pass.encode("utf-8")
    ])
    
    networks = get_linux_wifi()
    assert len(networks) == 1
    assert networks[0]["ssid"] == "MyLinuxWifi"
    assert networks[0]["password"] == "linux_secret"
