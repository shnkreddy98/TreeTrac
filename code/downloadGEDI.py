import os
import requests
from dotenv import load_dotenv
from datetime import datetime
from custom_logging import CustomLogging

# create session with the user credentials that will be used to authenticate access to the data
load_dotenv()
USERNAME = os.environ['username']
PASSWORD = os.environ['password']

# overriding requests.Session.rebuild_auth to mantain headers when redirected
class SessionWithHeaderRedirection(requests.Session):
    AUTH_HOST = 'urs.earthdata.nasa.gov'
    def __init__(self, username, password):
        super().__init__()
        self.auth = (username, password)

    # Overrides from the library to keep headers when redirected to or from
    # the NASA auth host.
    def rebuild_auth(self, prepared_request, response):
        headers = prepared_request.headers
        url = prepared_request.url
        if 'Authorization' in headers:
            original_parsed = requests.utils.urlparse(response.request.url)
            redirect_parsed = requests.utils.urlparse(url)
            if (original_parsed.hostname != redirect_parsed.hostname) and \
                    redirect_parsed.hostname != self.AUTH_HOST and \
                    original_parsed.hostname != self.AUTH_HOST:
                del headers['Authorization']
        return


class Download():

    def gediFile(dataDir, url, i, gediL2AFlag):
        starttime = datetime.now()
        global USERNAME 
        global PASSWORD
        session = SessionWithHeaderRedirection(USERNAME, PASSWORD)
        
        # extract the filename from the url to be used when saving the file
        filename = dataDir+"/h5/"+url.split("/")[-1]
        try:
            CustomLogging.logOutput(f"[INFO] Downloading file {i}...", gediL2AFlag)
            # submit the request using the session
            response = session.get(url, stream=True)
            CustomLogging.logOutput(f"[INFO] Response {response.status_code} for file {i}", gediL2AFlag)

            # raise an exception in case of http errors
            response.raise_for_status()  
            
            CustomLogging.logOutput(f"[INFO] Writing file {i} to {filename}...", gediL2AFlag)
            # save the file
            with open(filename, 'wb+') as fd:
                for chunk in response.iter_content(chunk_size=1024*1024):
                    fd.write(chunk)
            endtime = datetime.now()
            CustomLogging.logOutput(f"[INFO] Time taken to download: {endtime-starttime} seconds", gediL2AFlag)
            return filename

        except requests.exceptions.HTTPError as e:
            # handle any errors here
            CustomLogging.logOutput(f"[ERR] {e}", gediL2AFlag)
            CustomLogging.logOutput(f"{i}", gediL2AFlag)
