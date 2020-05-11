#Program for downloading files using url.
import requests
def download_tar(url,name):
    print("Downloading Started")
    r = requests.get(url, allow_redirects=True)
    print("Successfully Downloaded")
    open(name, 'wb').write(r.content)
print("Downloaded_module successfully called")