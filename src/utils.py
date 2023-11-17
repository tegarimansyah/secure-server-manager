import pathlib, subprocess

PROJECT_DIR = pathlib.Path("~/.ssm").expanduser()

def create_ssm_dir():
  PROJECT_DIR.mkdir(parents=True, exist_ok=True)

def create_rsa_private_public_key():
  filename = "enc"
  command = f'ssh-keygen -t rsa -b 4096 -f {str(PROJECT_DIR / filename)} -N ""'
  subprocess.run(command, shell=True)

def create_server_configuration():
  filename = "server.json"
  command = 'echo [] > ' + str(PROJECT_DIR / filename)
  subprocess.run(command, shell=True)
  (PROJECT_DIR / "keys").mkdir(parents=True, exist_ok=True)