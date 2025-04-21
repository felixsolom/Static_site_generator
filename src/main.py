import shutil
import os
from markdown_to_html import extract_title, markdown_to_html


from_path = "./content"
template_path = "./"
dest_path = "./public"
static_path = "./static"

def main():
    clean_dir(dest_path)
    copy_dir_to_dir(static_path, dest_path)
    generate_pages_recursive(from_path, template_path, dest_path)
 
def clean_dir(path):
    if os.path.exists(path):
       shutil.rmtree(path)
    os.mkdir(path)
 
def copy_dir_to_dir(path_from, path_to):
    if not os.path.exists(path_from):
        os.mkdir(path_from)
    if not os.path.exists(path_to):
        os.mkdir(path_to)
    listed_dir_to_copy = os.listdir(path=path_from)
    for item in listed_dir_to_copy:
        if os.path.isfile(f"{path_from}/{item}"):
            shutil.copy(f"{path_from}/{item}", path_to)
        elif os.path.isdir(f"{path_from}/{item}"):
            copy_dir_to_dir(f"{path_from}/{item}", f"{path_to}/{item}")
            
def generate_page(from_path, template_path, dest_path):
    print(f"""
          ======== Generating page =========
             from {from_path} to {dest_path} 
                using {template_path}.
              """)
    
    with open(os.path.join(from_path, "index.md")) as file:
        markdown_file = file.read()
    with open(os.path.join(template_path, "template.html")) as file:
        html_template = file.read()
    title = extract_title(markdown_file)
    node = markdown_to_html(markdown_file)
    html = node.to_html()
    full_html = html_template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
    if not os.path.isfile(os.path.join(dest_path, "index.html")):
        dest_file = open(os.path.join(dest_path, "index.html"), "w")
    dest_file.write(full_html)
    dest_file.close()
    
def generate_pages_recursive(dir_path_content, template_path, dest_path):
    print(f"""
          ======== Generating page =========
             from {dir_path_content} to {dest_path} 
                using {template_path}.
              """)
    with open(os.path.join(template_path, "template.html")) as file:
        html_template = file.read() 
    if not os.path.exists(dir_path_content):
        os.mkdir(dir_path_content)
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
    listed_dir_path_content = os.listdir(path=dir_path_content)
    for item in listed_dir_path_content:
        if os.path.isfile(os.path.join(dir_path_content, item)):
            with open(os.path.join(dir_path_content, item)) as file:
                markdown_file = file.read()
            title = extract_title(markdown_file)
            node = markdown_to_html(markdown_file)
            html = node.to_html()
            full_html = html_template.replace("{{ Title }}", title).replace("{{ Content }}", html)
            #if not os.path.exists(dest_path):
                #os.mkdir(dest_path)
            if not os.path.isfile(os.path.join(dest_path, "index.html")):
                dest_file = open(os.path.join(dest_path, "index.html"), "w")
            dest_file.write(full_html)
            dest_file.close()
        elif os.path.isdir(os.path.join(dir_path_content, item)):
            generate_pages_recursive(
                os.path.join(dir_path_content, item),
                template_path,
                os.path.join(dest_path, item) 
            )
            
             
    
    
    
if __name__=="__main__":
    main()