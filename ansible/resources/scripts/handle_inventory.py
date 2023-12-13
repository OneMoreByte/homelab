
import yaml

def add_role(hostname, role):
    with open("inventory.yaml") as handle:
        inventory = yaml.safe_load(handle.read())
    
    if not inventory.get(role) or not inventory.get(role).get("hosts"):
        if inventory.get(role):
            inventory[role]["hosts"] = []
        else:
            inventory[role] = {}
    inventory[role]["hosts"].append(hostname + ".localdomain")
    with open("inventory.yaml", "w") as handle:
        handle.write(yaml.dump(inventory))
