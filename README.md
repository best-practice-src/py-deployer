# Py Deployer

Py Deployer is a lightweight package to execute zero-downtime deployment on **Linux servers**.

```bash
pydeploy -s prod
```

## ✨ Features

- Cross-technology deployments
- Simple configuration
- Zero downtime deployments
- Multiple environment management
- Release version management
- Use SSH protocol

#### ⚠ This package does not currently support after-deployment scripts

## 1️⃣ Installation

```bash
sudo pip3 install py-deployer
```

## 2️⃣ Configuration

Create the file `deploy/config.yaml` inside your project as following:

```yaml
# Example of file: ./deploy/config.yaml

deploy:
  # Shared files and folders (between releases)
  shared: [.env]

  # All available servers (SSH configuration)
  servers:
    dev:
      hostname: '10.56.12.0'
      port: 22
      user: 'dev_username'
      password: ~ # Ignore that if you use SSH keys
      deploy_path: '/server/application/path'
      stage: 'develop'
      branch: 'dev'
      identity_file: ~  # Ignore that if it stay in the default folder (~/.ssh)
      repository: ~     # Ignore that if you run pydeploy from a git project directory
      max_releases: 3
    # ...
    prod:
      hostname: '10.56.11.0'
      port: 22
      user: 'prod_username'
      password: ~ # Ignore that if you use SSH keys
      deploy_path: '/server/application/path'
      stage: 'production'
      branch: 'master'
      identity_file: ~  # Ignore that if it stay in the default folder (~/.ssh)
      repository: ~     # Ignore that if you run pydeploy from a git project directory
      max_releases: 3


```

## 3️⃣ Deployment

Deploy your application by running:

```bash
pydeploy -s <dev|stag|prod|...>
```

## Links

- [PyPi](https://pypi.org/project/py-deployer/)