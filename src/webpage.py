from block import markdown_to_html_node
import os

def extract_title(markdown:str) -> str:
        lines = markdown.split("\n")

        # headings
        for line in lines:
            if line.strip().startswith("# "):
                return line.lstrip("# ").strip()
        
        raise Exception("markdown does not contain h1 title")


#needs to be recursiveeeee
def generate_page(from_path, template_path, dest_path, base_path):
    # check if dirs exist
    from_dir = os.path.dirname(from_path)
    template_dir = os.path.dirname(template_path)
    if not os.path.exists(from_dir) or not os.path.exists(template_dir):
        raise Exception(f"failed to open dirs {from_dir} or {template_dir}")

    # let em know
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

    # read
    with open(from_path, "r") as markdown_file:
        markdown_contents = markdown_file.read()
    with open(template_path, "r") as template_file:
        template_contents = template_file.read()
    if not markdown_contents or not template_contents:
        raise Exception(f"failed to read {from_path} or {dest_path}")
    
    # convert the markdown to html and pull out the title
    content = markdown_to_html_node(markdown_contents).to_html()
    title = extract_title(markdown_contents)

    # replace
    write_contents = template_contents.replace("{{ Title }}", title).replace("{{ Content }}", content)
    # replace the base paths
    write_contents = write_contents.replace('href="/', f'href="{base_path}')
    write_contents = write_contents.replace('src="/', f'src="{base_path}')

    # write    
    # make dest if not made
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
         os.makedirs(dest_dir)
    with open(dest_path, "w") as dest_file:
         dest_file.write(write_contents)