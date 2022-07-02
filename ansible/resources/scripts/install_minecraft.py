import requests
import json
import os
import tempfile
import shutil
import glob
import subprocess
import zipfile


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
---
module: my_test

short_description: This is my test module

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is my longer description explaining my test module.

options:
    name:
        description: This is the message to send to the test module.
        required: true
        type: str
    new:
        description:
            - Control to demo if the result of this module is changed or not.
            - Parameter description can be a list as well.
        required: false
        type: bool
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - my_namespace.my_collection.my_doc_fragment_name

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  my_namespace.my_collection.my_test:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_namespace.my_collection.my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_namespace.my_collection.my_test:
    name: fail me
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
'''

from ansible.module_utils.basic import AnsibleModule


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True),
        new=dict(type='bool', required=False, default=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result['original_message'] = module.params['name']
    result['message'] = 'goodbye'

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if module.params['new']:
        result['changed'] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['name'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()


def install_paper(version="latest", install_path="."):
    paper_versions = get_paper_versions()
    if version == "latest":
        version = paper_versions[-1]
    else:
        if version not in paper_versions:
            print(f"version '{version}' is not a valid version. valid versions: {paper_versions}")
            exit(1)
    paper_release = get_paper_release(version)
    filename = get_paper_filename(version, paper_release)
    if os.path.isfile(f"{install_path}/{filename}"):
        print("latest version is already installed")
        return
    get_paper(version, paper_release, filename, install_path)
    sign_eula(install_path)


def install_forge_modpack(modpack_archive, install_path="."):
    old_manifest = None
    if os.path.isfile(f"{install_path}/manifest.json"):
        with open(f"{install_path}/manifest.json") as handle:
            old_manifest = json.load(handle)
    manifest = read_manifest(modpack_archive, install_path=install_path)
    if old_manifest:
        old_mods = set(old_manifest.get("files")) - set(manifest.get("files"))
        new_mods = set(manifest.get("files")) - set(old_manifest.get("files"))
        changed = False
        if old_mods:
            remove_mods(old_mods, install_path)
            changed = True
        if new_mods:
            get_mods(new_mods, install_path)
            changed = True
        old_mc_version = old_manifest.get("minecraft", {}).get("version")
        new_mc_version = manifest.get("minecraft", {}).get("version")
        old_forge_version = get_forge_version(old_manifest)
        new_forge_version = get_forge_version(manifest)
        if old_mc_version != new_mc_version or old_forge_version != new_forge_version:
            for forgejar in glob.glob(f"{install_path}/forge-{old_mc_version}-{old_forge_version}*"):
                os.remove(forgejar)
            install_forge(new_mc_version, old_forge_version, install_path)
            changed = True
        print(changed)
    else:
        mc_version = manifest.get("minecraft", {}).get("version")
        forge_version = get_forge_version(manifest)
        install_forge(mc_version, forge_version, install_path)
        sign_eula(install_path)
    shutil.move(f"{install_path}/new-manifest.json", f"{install_path}/manifest.json")
    return


def install_forge(mc_version, forge_version, install_path):
    version = f"{mc_version}-{forge_version}"
    url = "https://files.minecraftforge.net"
    path = f"/maven/net/minecraftforge/forge/{version}/forge-{version}-installer.jar"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0"}
    res = requests.get(url + path, headers=headers)
    filename = f"{install_path}/forge-{version}-installer.jar"
    if res.status_code == 200:
        with open(filename, "wb") as handle:
            for chunk in res.iter_content(chunk_size=128):
                handle.write(chunk)
        old_path = os.getcwd()
        os.chdir(install_path)
        subprocess.run(["java", "-jar", filename, "--installServer"])
        os.chdir(old_path)
        return f"forge-{version}-universal.jar"
    return None


def read_manifest(zip_path, install_path="."):
    manifest = None
    with tempfile.TemporaryDirectory() as temp:
        with zipfile.ZipFile(zip_path) as zip_handle:
            zip_handle.extractall(path=temp)
        if os.path.isdir(temp + "/overrides"):
            for item in glob.glob(temp + "/overrides/*"):
                if os.path.isfile(item):
                    shutil.copy(item, install_path + "/")
                else:
                    item_name = item.split("/")[-1]
                    shutil.copytree(item, install_path + "/" + item_name, dirs_exist_ok=True)
        with open(f"{temp}/manifest.json") as handle:
            manifest = json.load(handle)
        shutil.move(f"{temp}/manifest.json", f"{install_path}/new-manifest.json")
    return manifest


def get_mod_data(project_id, file_id):
    domain = "https://addons-ecs.forgesvc.net"
    url = f"{domain}/api/v2/addon/{project_id}/file/{file_id}"
    print(url)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0"}
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        return json.loads(res.text)
    return None


def get_mod(url, filename):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0"}
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        print(filename)
        with open(filename, "wb") as handle:
            for chunk in res.iter_content(chunk_size=128):
                handle.write(chunk)
        return True
    print(res.status_code)
    return False


def get_mods(mods, install_path):
    mod_dir = install_path + "/mods"
    os.makedirs(mod_dir, exist_ok=True)
    for mod in mods:
        project_id = mod.get("projectID")
        file_id = mod.get("fileID")
        required = mod.get("required")
        if required:
            mod_data = get_mod_data(project_id, file_id)
            get_mod(mod_data.get("downloadUrl"), f'{mod_dir}/{mod_data.get("fileName")}')


def remove_mods(mods, install_path):
    mod_dir = install_path + "/mods"
    os.makedirs(mod_dir, exist_ok=True)
    for mod in mods:
        project_id = mod.get("projectID")
        file_id = mod.get("fileID")
        required = mod.get("required")
        if required:
            mod_data = get_mod_data(project_id, file_id)
            os.remove(f'{mod_dir}/{mod_data.get("fileName")}')


def get_forge_version(manifest):
    if manifest.get("minecraft", {}).get("modLoaders"):
        modloaders = manifest.get("minecraft", {}).get("modLoaders")
        if "forge" in modloaders[0].get("id"):
            return modloaders[0].get("id").split("-")[-1]
    print("Not a forge modpack. Refusing")
    exit(1)


def sign_eula(install_dir):
    with open(install_dir + "/eula.txt", "w") as handle:
        handle.write("eula=true\n")


def get_paper_versions():
    res = requests.get("https://papermc.io/api/v2/projects/paper")
    if res.status_code == 200:
        return json.loads(res.text).get("versions", [])
    return []


def get_paper_release(version):
    res = requests.get(f"https://papermc.io/api/v2/projects/paper/versions/{version}")
    if res.status_code == 200:
        return json.loads(res.text).get("builds", [])[-1]
    return None


def get_paper_filename(version, release):
    domain = "https://papermc.io"
    url = f"{domain}/api/v2/projects/paper/versions/{version}/builds/{release}"
    res = requests.get(url)
    if res.status_code == 200:
        data = json.loads(res.text)
        return data.get("downloads", {}).get("application", {}).get("name")
    return None

def get_paper(version, release, filename, install_dir):
    print("Fetching paper version for mc version", version, "build", release)
    domain = "https://papermc.io"
    url = f"{domain}/api/v2/projects/paper/versions/{version}/builds/{release}/downloads/{filename}"
    res = requests.get(url)
    if res.status_code == 200:
        with open(f"{install_dir}/{filename}", "wb") as handle:
            for chunk in res.iter_content(chunk_size=128):
                handle.write(chunk)
        return filename
    return None


if __name__ == "__main__":
    install_forge_modpack("/mnt/c/Users/jsck/Downloads/RLCraft+1.12.2+-+Beta+v2.8.2.zip")