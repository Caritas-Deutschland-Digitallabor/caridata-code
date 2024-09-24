# VSCode Configuration
## VSCode Settings
This [settings.json file](../../.vscode/settings.json) is configuring Visual Studio Code settings specifically for Python files. Here's a breakdown of what each setting does:

`editor.formatOnSave`: This setting is set to true, which means that every time you save a Python file, VS Code will automatically format it using the specified formatter.

`editor.codeActionsOnSave`: This setting specifies code actions that are run when a file is saved. In this case, it's set to run two actions: `source.fixAll` and `source.organizeImports`. However, both are set to "explicit", which means they will only run when explicitly invoked.

`editor.defaultFormatter`: This setting specifies the default formatter to use for Python files. In this case, it's set to charliermarsh.ruff. This formatter will be used when you manually invoke the Format Document command or when `editor.formatOnSave` is set to true.

`editor.rulers`: This setting specifies where to draw vertical rulers in the editor. These rulers can be used as visual guides. In this case, a ruler is drawn at the 100th character, which can be useful for enforcing line length limits.

These settings help automate and standardize certain aspects of writing Python code in VS Code, such as formatting and organizing imports.

## VSCode Debugger
The [launch.json file](../../.vscode/launch.json) is a configuration file for Visual Studio Code that configures how the debugger should be launched. This specific launch.json file is set up to debug a FastAPI application using the debugpy debugger. Here's a breakdown of the configuration:

__"name"__: "Python Debugger: FastAPI": This is the name of the debug configuration that will appear in the dropdown of the Debug view.

__"type"__: "debugpy": This specifies that the debugger to use is debugpy, which is a Python debugger.

__"cwd"__: "${workspaceFolder}/backend/src": This sets the current working directory for the debugger to the backend/src directory in your workspace.

__"request"__: "launch": This tells VS Code to start a new instance of the target (in this case, a Python process) for debugging.

__"module"__: "uvicorn": This specifies that the debugger should run the uvicorn module. Uvicorn is an ASGI server that is used to serve FastAPI applications.

__"args"__: ["api:app", "--reload", "--host", "0.0.0.0", "--port", "8001"]: These are the arguments that are passed to the uvicorn module. It's telling Uvicorn to serve the FastAPI application defined in the api module (specifically the app object), to automatically reload the server when code changes are detected, and to serve the application on host 0.0.0.0 and port 8001.

__"jinja"__: true: This enables Jinja templating support in the debugger.

With this configuration, you can start a debugging session for your FastAPI application directly from VS Code by selecting "Python Debugger: FastAPI" from the debug configurations dropdown and pressing the start debugging button.

## VSCode Tasks
The [tasks.json](../../.vscode/tasks.json) file in Visual Studio Code is used to configure tasks that can be run from within VS Code. These tasks can be anything from running scripts, compiling code, or starting servers. Here's a breakdown this tasks.json file:

__NPM Task (Lines 4-18)__: This task runs the "dev" script in the "webapp" directory using npm. The task is labeled as "npm: dev - webapp" and is associated with the "vite" detail. The output of this task is always revealed in a new panel in the "startup" group. This task is set to run automatically when the folder is opened (runOn: "folderOpen").

__Shell Task (Lines 19-48)__: This task is labeled as "FastAPI: Run" and runs a sequence of shell commands. It first sleeps for 5 seconds, then uses Poetry to run the Uvicorn server with the FastAPI application. The working directory for this task is set to `${workspaceFolder}/backend/src` and the shell used to run the command is `/bin/bash`. The output of this task is always revealed in a new panel in the "startup" group. This task is also set to run automatically when the folder is opened (runOn: "folderOpen").

These tasks are designed to automatically start your development servers (both frontend and backend) when you open your workspace in VS Code. The frontend server is started using Vite (a modern frontend build tool), and the backend server is a FastAPI application served using Uvicorn.
