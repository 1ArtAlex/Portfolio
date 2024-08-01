import os

def check_copyright(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        if not lines:
            return False
        return "Copyright" in lines[0]

def main():
    project_dir = "my-lab-repository/scr" 
    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith('.cpp'):
                file_path = os.path.join(root, file)
                if not check_copyright(file_path):
                    print(f"Copyright missing in {file_path}")
                    exit(1)
    print("All files have copyright")

if __name__ == "__main__":
    main()
