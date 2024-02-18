import subprocess


def run_command(command):
    try:
        output = subprocess.check_output(
            command, 
            stderr=subprocess.STDOUT, 
            shell=True, 
            universal_newlines=True)
        print(output)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.output}")

image_name = "postgres_image"
container_name = "postgres_container"

run_command(f"docker build -t {image_name} .")
run_command(f"docker run --name {container_name} -p 5432:5432 -d {image_name}")
