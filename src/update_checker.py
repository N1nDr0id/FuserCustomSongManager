import urllib.request, json

def check_for_update(version_number):
    update_available = None
    with urllib.request.urlopen("https://api.github.com/repos/N1nDr0id/FuserCustomSongManager/releases/latest") as url:
        data = json.load(url)
        latest_version = data['tag_name']
        if (version_number != latest_version): # assume that latest version is newer than current version
            update_available = latest_version
            print("Update available!")
    return update_available

version_number = "v1.0.0"

#check_for_update(version_number)