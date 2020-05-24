import subprocess

subprocess.run(['pyinstaller', '--onedir', 'main.py', '--clean', '--hidden-import="pkg_resources.py2_warn"'])
