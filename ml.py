import datetime
from typing import List, TypedDict

import requests
_requests_response_cache = {}
_user_agent_cache = ""

def get_user_agent() -> str:
    """
    Returns the user agent of minecraft-launcher-lib
    """
    global _user_agent_cache
    if _user_agent_cache is not None:
        return _user_agent_cache
    else:
        _user_agent_cache = "minecraft-launcher-lib/2.0"
        return _user_agent_cache
def get_requests_response_cache(url: str) -> requests.models.Response:
    """
    Caches the result of request.get(). If a request was made to the same URL within the last hour, the cache will be used, so you don't need to make a request to a URl each timje you call a function.
    """
    global _requests_response_cache
    if url not in _requests_response_cache or (datetime.datetime.now() - _requests_response_cache[url]["datetime"]).total_seconds() / 60 / 60 >= 1:
        r = requests.get(url, headers={"user-agent": get_user_agent()})
        if r.status_code == 200:
            _requests_response_cache[url] = {}
            _requests_response_cache[url]["response"] = r
            _requests_response_cache[url]["datetime"] = datetime.datetime.now()
        return r
    else:
        return _requests_response_cache[url]["response"]

class MinecraftVersionInfo(TypedDict):
    id: str
    type: str
    releaseTime: datetime.datetime
    complianceLevel: int
    url: str

def get_version_list() -> List[MinecraftVersionInfo]:
    """
    Returns all versions that Mojang offers to download
    """
    vlist = get_requests_response_cache("https://launchermeta.mojang.com/mc/game/version_manifest_v2.json").json()
    returnlist = []
    for i in vlist["versions"]:
        returnlist.append({"id": i["id"], "type": i["type"], "releaseTime": datetime.fromisoformat(i["releaseTime"]), "complianceLevel": i["complianceLevel"],"url": i["url"]})
    return returnlist