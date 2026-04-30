import shutil
from webpage import generate_page

def main():
    from_path="./content/index.md"
    template_path="./template.html"
    dest_path="./public/index.html"
    shutil.copytree("./static", "./public", dirs_exist_ok=True)
    generate_page(from_path, template_path, dest_path)

main()