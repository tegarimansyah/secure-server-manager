import os
from fastapi import FastAPI, BackgroundTasks, responses, Request
from rich import print
from . import pangea

def shutdown():
    os._exit(os.EX_OK)
   
def success_page():
   return """
    <html>
        <head>
            <title>Login Success</title>
        </head>
        <body>
            <h1>Login Success</h1>
            <p>You can close this tab and back to your terminal</p>
        </body>
    </html>
    """

def failed_page(e):
   return f"""
    <html>
        <head>
            <title>Login Failed</title>
        </head>
        <body>
            <h1>Login Failed</h1>
            <p>{e}</p>
        </body>
    </html>
    """

def create_web_server(add_local_token):
    app = FastAPI()


    async def login(code: str):
        try:
            print(f"Logged in. Now get access token and profile.")
            token = pangea.get_jwt(code)
            add_local_token(token.get('result'))
            return responses.RedirectResponse("success")
        except AssertionError as e:
            return responses.RedirectResponse(f"fail?msg={e}")

    def success(background_tasks: BackgroundTasks):
        print("[bold green]Login success[/bold green]")
        background_tasks.add_task(shutdown)
        return responses.HTMLResponse(success_page(), status_code=200)
    
    def fail(msg:str, background_tasks: BackgroundTasks):
        print(f"[bold red]Login failed[/bold red]: {msg}")
        background_tasks.add_task(shutdown)
        return responses.HTMLResponse(failed_page(msg), status_code=200)

    app.add_api_route("/", login, methods=["GET"])
    app.add_api_route("/success", success, methods=["GET"])
    app.add_api_route("/fail", fail, methods=["GET"])
  
    return app