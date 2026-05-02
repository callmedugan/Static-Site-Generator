import shutil
from webpage import generate_page
from pathlib import Path
import sys

def main():
    from_folder="./content"
    template_file="./template.html"
    dest_folder="./public"

    basepath = "/" if len(sys.argv) <= 1 else sys.argv[1]
    print(basepath)

    #copies over the resources
    shutil.copytree("./static", "./public", dirs_exist_ok=True)

    # find each file in the content folder and generate a page and copy it over
    for md_file in Path(from_folder).rglob('*md'):
        if md_file.is_file():
            #just caching
            md_file_path = str(md_file)
            #remove the old parent folder name and any . or / 
            split = md_file_path.split("/", 1)
            if not split[1]:
                raise Exception("problem parsing new file name for " + md_file_path)
            new_root = split[1].removeprefix(from_folder).lstrip("./")
            #change the file type and add the new parent folder name
            dest = dest_folder + "/" + new_root.removesuffix(".md") + ".html"
            generate_page(md_file_path, template_file, dest)

main()