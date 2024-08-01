import os
import subprocess

def run_clang_tidy(file_path):
    cmd = ['clang-tidy', file_path, '--']
    
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if result.returncode != 0:
        print(f"Syntax issues found in {file_path}:")
        print(result.stderr.decode('utf-8'))
        return False
    return True

def main():
    project_dir = "my-lab-repository/src" 
    
    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith('.cpp') or file.endswith('.h'):
                file_path = os.path.join(root, file)
                if not run_clang_tidy(file_path):
                    exit(1)
    
    print("All files passed syntax checks")

if __name__ == "__main__":
    main()
