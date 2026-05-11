import os

import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_nginx_is_installed(host):
    package = host.package("nginx")
    assert package.is_installed


def test_nginx_is_running(host):
    service = host.service("nginx")
    assert service.is_running
    assert service.is_enabled


def test_postgresql_is_running(host):
    service = host.service("postgresql")
    assert service.is_running
    assert service.is_enabled


def test_simple_api_service_is_running(host):
    service = host.service("simple-api")
    assert service.is_running
    assert service.is_enabled


def test_app_health_endpoint(host):
    response = host.run("curl -s http://127.0.0.1/health")
    assert response.rc == 0
    assert '"status":"ok"' in response.stdout or '"status": "ok"' in response.stdout


def test_users_endpoint(host):
    response = host.run("curl -s http://127.0.0.1/users")
    assert response.rc == 0
    assert response.stdout.strip().startswith("[")


def test_api_uses_database(host):
    create_response = host.run(
        "curl -s -X POST http://127.0.0.1/users "
        "-H 'Content-Type: application/json' "
        "-d '{\"name\":\"molecule-test\"}'"
    )
    assert create_response.rc == 0
    assert "molecule-test" in create_response.stdout

    list_response = host.run("curl -s http://127.0.0.1/users")
    assert list_response.rc == 0
    assert "molecule-test" in list_response.stdout


def test_certbot_is_installed(host):
    package = host.package("certbot")
    assert package.is_installed


def test_maildev_service_is_running(host):
    service = host.service("maildev")
    assert service.is_running
    assert service.is_enabled


def test_maildev_ports_are_listening(host):
    smtp = host.socket("tcp://0.0.0.0:1025")
    web = host.socket("tcp://0.0.0.0:1080")
    assert smtp.is_listening
    assert web.is_listening


def test_postfix_is_installed(host):
    package = host.package("postfix")
    assert package.is_installed


def test_postfix_is_running(host):
    service = host.service("postfix")
    assert service.is_running
    assert service.is_enabled


def test_backup_script_exists(host):
    backup_script = host.file("/usr/local/bin/simple-api-backup.sh")
    assert backup_script.exists
    assert backup_script.mode == 0o750


def test_backup_cron_is_configured(host):
    cron = host.run("sudo crontab -l")
    assert cron.rc == 0
    assert "simple-api-backup.sh" in cron.stdout


def test_backup_script_runs_successfully(host):
    result = host.run("sudo /usr/local/bin/simple-api-backup.sh")
    assert result.rc == 0

    backups = host.run("sudo find /var/backups/simple-api -type f")
    assert "database_" in backups.stdout
    assert "app_" in backups.stdout
