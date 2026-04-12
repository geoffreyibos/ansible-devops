import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_nginx_running_and_enabled(host):
    app_service = host.service("nginx")
    assert app_service.is_running
    assert app_service.is_enabled


def test_nginx_listening(host):
    assert host.socket("tcp://0.0.0.0:8080").is_listening
