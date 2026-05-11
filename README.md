# TP DevOps - Ansible

Projet d'exemple pour la prise en main d'Ansible dans un contexte DevOps.
Il illustre le déploiement automatisé d'une stack applicative (base de données, serveur API, reverse proxy Nginx) à l'aide de playbooks Ansible et de l'outil de test Molecule.

## Prérequis

Avant de commencer, assurez-vous d'avoir installé les outils suivants sur votre machine :

- [Python 3.12](https://www.python.org/download/)
  ```bash
  sudo apt-get install python3 python3-pip
  sudo pip3 install virtualenv
  ```
- [VirtualBox](https://www.virtualbox.org/)
- [Vagrant](https://www.vagrantup.com/)

## Mise en place de l'environnement local

Ce projet utilise un environnement virtuel Python pour isoler les dépendances. Pour l'initialiser, exécutez depuis la racine du projet :

```bash
source venv.sh
```

Cette commande crée l'environnement virtuel, l'active et installe toutes les dépendances Python nécessaires (Ansible, Molecule, etc.).

Des fonctions utilitaires sont ensuite disponibles dans le terminal :
- `download_galaxy` — télécharge les rôles Ansible déclarés dans `roles/requirements.yml`
- `rebuild_env` — recrée l'environnement virtuel from scratch
- `deactivate` — quitte l'environnement virtuel

## Développement et tests avec Molecule

Ce projet intègre [Molecule](https://molecule.readthedocs.io/en/stable/) pour tester les rôles Ansible dans des machines virtuelles éphémères.

| Commande | Description |
|---|---|
| `molecule converge` | Crée la VM de test et applique les playbooks |
| `molecule login` | Se connecte en SSH à la machine de test |
| `molecule verify` | Exécute les tests de vérification |
| `molecule test` | Lance le cycle de test complet (create → converge → verify → destroy) |

> Avant tout commit, vérifiez que tous les tests passent avec `molecule test`.

## Structure du projet

```
.
├── hosts/              # Inventaires (machines cibles)
│   └── hosts_dev       # Inventaire de développement (utilisé par Molecule)
├── group_vars/         # Variables par groupe d'hôtes
│   ├── all.yml
│   ├── api.yml
│   └── database.yml
├── roles/              # Rôles Ansible locaux
│   └── requirements.yml
├── molecule/           # Configuration des tests Molecule
├── playbook_install.yml # Playbook principal de déploiement
└── venv.sh             # Script d'initialisation de l'environnement
```

## Déploiement

### 1. Activer l'environnement virtuel

```bash
source venv.sh
```

### 2. Télécharger les rôles Galaxy

```bash
download_galaxy
```

### 3. Configurer le vault Ansible

Certaines variables sont chiffrées avec [Ansible Vault](https://docs.ansible.com/ansible/latest/user_guide/vault.html).
Créez un fichier `.devops_vault_pass.txt` à la racine du projet contenant le mot de passe du vault.

Pour ce projet d'exemple, le mot de passe est : `password`

> **Attention :** Ne poussez jamais ce fichier sur un dépôt distant. Ajoutez-le à votre `.gitignore`.

### 4. Lancer le playbook

Voici la commande pour lancer le playbook si une vrai machine est configuré (ce qui n'est pas le cas pour ce TP).
```bash
ansible-playbook -i hosts/hosts_dev -u devops playbook_install.yml
```

## Gestion des vaults

```bash
# Créer un nouveau vault
ansible-vault create group_vars/devops_dev/vault.yml

# Editer un vault existant
ansible-vault edit group_vars/devops_dev/vault.yml

# Consulter un vault
ansible-vault view group_vars/devops_dev/vault.yml
```

# Déploiement automatisé d’une infrastructure Flask avec Ansible

## Description du projet

Ce projet met en place une infrastructure complète automatisée avec Ansible pour déployer une API Flask sur une machine Ubuntu via Molecule, Vagrant et VirtualBox.

L’infrastructure déployée comprend :

- une application Flask exécutée avec systemd ;
- un reverse proxy nginx ;
- une base de données PostgreSQL ;
- des roles Ansible séparés et réutilisables ;
- des tests Molecule/Testinfra ;
- une vérification d’idempotence ;
- une analyse qualité avec ansible-lint et flake8.

Le projet respecte une approche Infrastructure as Code et automatise entièrement le déploiement, la configuration et la validation de l’environnement.

## Membres du binôme

- Oscar DEBEURET
- Geoffrey IBOS

## Bonus implémentés

- Ansible Vault : chiffrement du mot de passe de base de données.
- Multi-environnements : variables séparées pour dev, staging et production.
- Certbot : installation et préparation de la configuration Let's Encrypt.
- Maildev : serveur SMTP de développement sur les ports 1025 et 1080.
- Postfix : serveur de mail local configuré en loopback-only.
- Backup automatisé : dump PostgreSQL, archive applicative, rotation et cron.
