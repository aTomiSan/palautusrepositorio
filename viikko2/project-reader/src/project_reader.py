from urllib import request
from project import Project
import toml

class ProjectReader:
    def __init__(self, url):
        self._url = url

    def get_project(self):
        # tiedoston merkkijonomuotoinen sisältö
        content = request.urlopen(self._url).read().decode("utf-8")
        loaded = toml.loads(content)
        name = loaded["tool"]["poetry"]["name"]
        description = loaded["tool"]["poetry"]["description"]
        license = loaded["tool"]["poetry"]["license"]
        authors = loaded["tool"]["poetry"]["authors"]
        dependencies = loaded["tool"]["poetry"]["dependencies"]
        group_dependencies = loaded["tool"]["poetry"]["group"]["dev"]["dependencies"]
        author_list = []
        for one in authors: 
            author_list.append(f"\n- {one}")
        dependency_list = []
        for one in dependencies: 
            dependency_list.append(f"\n- {one}")
        group_dependency_list = []
        for one in group_dependencies: 
            group_dependency_list.append(f"\n- {one}")

        # deserialisoi TOML-formaatissa oleva merkkijono ja muodosta Project-olio sen tietojen perusteella
        return Project(name, description, license, author_list, dependency_list, group_dependency_list)
