import os, json, typer, subprocess
from rich import print
from . import utils, web, pangea

def get_local_token():
   '''
   Will return the token if exists, None if not exists
   '''
   credential_path = os.path.expanduser('~/.ssm/credential')
   if os.path.exists(credential_path):
     with open(credential_path, 'r') as f:
       data = json.load(f)
       return data
   return None

def add_local_token(token):
  print(f"Saving credential")
  utils.create_ssm_dir()
  with open(os.path.expanduser('~/.ssm/credential'), 'w') as f:
    json.dump(token, f, indent=4)
  
  print(f"Getting Server Configuration")
  with open(os.path.expanduser('~/.ssm/server.json'), 'w') as f:
    server_config = pangea.get_server_config(token)
    json.dump(server_config, f, indent=4)

  print(f"Getting Secret Keys")
  (utils.PROJECT_DIR / "keys").mkdir(parents=True, exist_ok=True)
  private_key: dict
  for private_key in pangea.get_private_keys(token):
    filename = os.path.expanduser(f'~/.ssm/keys/{private_key.get("name")}')
    with open(filename, 'w') as f:
      f.write(private_key.get("secret"))
    command = f"chmod 600 {filename}"
    subprocess.run(command, shell=True)

def open_login_web():
  '''
  Open browser and ask user to login, after that call api to local
  server, save the token and shutdown local server
  '''
  # url = "http://localhost:8001/" + '?jwt=abc.123.def'
  url = "https://pdn-kn4l2akl67yjxi6nbqp5lktw5bdncyft.login.aws.us.pangea.cloud/authorize?redirect_uri=http://localhost:8001/&state=cli_login"
  print("Loging in. Please click this app to login:")
  print(f"[bold green]{url}[/bold green]")

  import uvicorn
  local_web = web.create_web_server(add_local_token)
  typer.launch(url)
  uvicorn.run(local_web, host="0.0.0.0", port=8001, log_level="error")

def login():
  token = get_local_token()
  if token:
     print("Already login")
     return
  
  open_login_web()

def logout():
   print("Loging Out")
   print(f"[bold red]Deleting {str(utils.PROJECT_DIR)}[/bold red]")
   command = f"rm -Rf {str(utils.PROJECT_DIR)}"
   subprocess.run(command, shell=True)