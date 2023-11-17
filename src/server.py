import subprocess, questionary, json, os
from . import utils, pangea
from rich import print

def get_server_list():
    with open(os.path.expanduser('~/.ssm/server.json'), 'r') as fr:
        data = json.load(fr)
        return data

def add_server():
    answer = questionary.form(
        name = questionary.text("Name for this server:"),
        username = questionary.text("Username:"),
        server = questionary.text("Server IP or Hostname:"),
        credential_type = questionary.select("Type of credential:", choices=["password", "key_file"])
    ).ask()

    if answer.get("credential_type") == "password":
        credential = questionary.password("Enter your password:").ask()
    else:
        credential = questionary.path("The key file path:").ask()
        filename = credential.split("/")[-1]
        command = f"cp {os.path.expanduser(credential)} {str(utils.PROJECT_DIR)}/keys/{filename}"
        print("Copying SSH key...")
        print(command)
        subprocess.run(command, shell=True, )
        command = f"chmod 600 {str(utils.PROJECT_DIR)}/keys/{filename}"
        subprocess.run(command, shell=True, )

        credential = f"~/.ssm/keys/{filename}"
        
    answer = {**answer, "credential": credential}
    with open(os.path.expanduser('~/.ssm/server.json'), 'r') as fr:
        data: list = json.load(fr)
        with open(os.path.expanduser('~/.ssm/server.json'), 'w') as fw:
            data.append(answer)
            json.dump(data, fw, indent=4)
            
    print("[bold green]Server configuration saved successfully[/bold green]")

def select_server(servers: list):
    choice = questionary.select("Select item", choices=[server["name"] for server in servers]).ask()
    server = list(filter(lambda server: server["name"] == choice, servers))[0]
    return server
    
def run_ssh_command(credential, credential_type, username, server, **kwargs):
    if credential_type == "key_file":
        command = f"ssh -i {credential} {username}@{server}"
        print(f"Connecting to {kwargs.get('name')}: {command}")
        subprocess.run(command, shell=True)
    else:
        print("Connect ssh via password is in progress")