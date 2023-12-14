import urllib.request, json
from pkg_resources import packaging

def check_for_update(version_number):
    current_version = packaging.version.parse(version_number)
    update_available = None
    with urllib.request.urlopen("https://api.github.com/repos/N1nDr0id/FuserCustomSongManager/releases/latest") as url:
        data = json.load(url)
        latest_version_string = data['tag_name']
        latest_version = packaging.version.parse(latest_version_string[1:])
        #print(current_version)
        #print(latest_version)
        if (current_version < latest_version): # assume that latest version is newer than current version
            update_available = latest_version_string
            print("Update available!")
    return update_available

version_number = "1.0.0"

#check_for_update(version_number)