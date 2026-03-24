import subprocess


def dev() -> None:
    subprocess.run(["fastapi", "dev", "app/main.py", "--host", "127.0.0.1", "--port", "8000"], check=True)


if __name__ == "__main__":
    dev()
