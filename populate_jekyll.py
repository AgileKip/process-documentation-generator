from yaml import safe_load, YAMLError
import shutil
import os

filename = 'mock.yml'
jekyl_project_name = 'jekyl_project_test'
jekyl_project_path = 'E:/Workspace'
project_path = f'{jekyl_project_path}/{jekyl_project_name}'

files_to_copy = ['index.html']
folders_to_copy = ['_layouts', '_includes', 'assets/css']

def create_folder(path, name):
    folder_path = f'{path}/{name}'
    try:
        os.mkdir(folder_path)
    except OSError as e:
        print(f"Failed to create {folder_path}")

def create_collection(path, items, layout):
    for identifier, properties in items.items():
        with open(f'{path}/{identifier}.md', 'w') as f:
            f.write('---\n')

            f.write(f'layout: {layout}\n\n')

            f.write(f'pk: {identifier}\n\n')
            for property, values in properties.items():
                if values is None:
                    f.write(f'{property}:\n')
                elif isinstance(values, str) or isinstance(values, bool):
                    f.write(f'{property}: {values}\n')
                elif isinstance(values, list):
                    f.write(f'{property}:\n')
                    for value in values:
                        f.write(f'  - {value}\n')
                else:
                    raise TypeError(f'"{values}" is not a valid value for the "{property}" property')

            f.write('---')

def add_collections_to_config(path, collections):
    with open(path, 'a') as f:
        f.write('\ncollections:\n')

        for collection in collections:
            f.write(f'  {collection}:\n')
            f.write(f'    output: true\n')

def copy_statics_to_project(dest_path, files, folders):
    current_path = os.getcwd()

    for file in files:
        shutil.copyfile(f'{current_path}/{file}', f'{dest_path}/{file}')
    
    for folder in folders:
        os.mkdir(f'{dest_path}/{folder}')
        
        for _, _, folder_files in os.walk(folder):
            for file in folder_files:
                shutil.copyfile(f'{current_path}/{folder}/{file}', f'{dest_path}/{folder}/{file}')


# Init Jekyll project
os.system(f'jekyll new {project_path}')

# Remove template files
os.remove(f'{project_path}/404.html')
os.remove(f'{project_path}/about.markdown')
os.remove(f'{project_path}/index.markdown')

# Create collections
raw_data = {}
with open(filename, 'r') as stream:
    try:
        raw_data = safe_load(stream)
    except YAMLError as exc:
        print(exc)

entities = raw_data.keys()
for entity in entities:
    collection_name = f'_{entity}'
    create_folder(project_path, collection_name)

    collection_path = f'{project_path}/{collection_name}'
    create_collection(collection_path, raw_data[entity], entity)
    print(f'Created {entity} collection successfully')

config_path = f'{project_path}/_config.yml'
add_collections_to_config(config_path, entities)

# Copy static files
os.mkdir(f'{project_path}/assets')
copy_statics_to_project(project_path, files_to_copy, folders_to_copy)