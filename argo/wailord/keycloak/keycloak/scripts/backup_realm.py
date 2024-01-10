import json
from dataclasses import dataclass
from getpass import getpass
from typing import Any

import requests


@dataclass
class Config:
    username: str
    password: str
    base_url: str
    realm: str


class RealmExporter:
    def __init__(self):
        self.config: Config = self.get_config()
        self.headers = {
            "Accept": "application/json",
            "Authorization": "Bearer " + self.get_token(),
        }

    def get_config(self) -> Config:
        username = input("Username: ")
        password = getpass()
        base_url = input("Base url: ")
        realm = input("Realm: ")
        return Config(username, password, base_url, realm)

    def get_token(self) -> str:
        path = "/auth/realms/master/protocol/openid-connect/token"
        data = {
            "client_id": "admin-cli",
            "username": self.config.username,
            "password": self.config.password,
            "grant_type": "password",
        }
        res = requests.post(self.config.base_url + path, data=data)
        if res.status_code == 200:
            return res.json().get("access_token", "")
        return ""

    def _get_from_kc(self, path: str) -> dict[str, Any] | None:
        res = requests.get(self.config.base_url + path, headers=self.headers)
        if res.status_code != 200:
            return None
        return res.json()

    def export_realm(self) -> dict[str, Any] | None:
        # https://stackoverflow.com/questions/65200310/export-users-and-roles-from-keycloak
        base_path = f"/auth/admin/realms/{self.config.realm}"
        realm = self._get_from_kc(base_path)
        if realm is None:
            print("failed to get realm json!")
            return None
        subpaths = [
            "users",
            "roles",
            "groups",
            "clients",
            "client-scopes",
        ]
        for subpath in subpaths:
            path = base_path + "/" + subpath
            data = self._get_from_kc(path)
            if data is None:
                print(f"failed to get {subpath} json!")
                return None
            realm[subpath] = data
        return realm


def main():
    realm_exporter = RealmExporter()
    realm_data = realm_exporter.export_realm()
    if realm_data is not None:
        with open("realm.json", "w", encoding="utf8") as f:
            f.write(json.dumps(realm_data, indent=4))


if __name__ == "__main__":
    main()
