#!/usr/bin/env python3
"""Download a user-authorised APKM from a short-lived HTTPS URL stored in a secret."""
import os, urllib.request, urllib.parse
url=os.environ.get("APK_SOURCE_URL","")
parsed=urllib.parse.urlparse(url)
if parsed.scheme!="https" or not parsed.netloc or parsed.username or parsed.password:
    raise SystemExit("APK_SOURCE_URL must be a direct HTTPS URL")
req=urllib.request.Request(url,headers={"User-Agent":"YouTubeTVPatchLab/0.1"})
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if urllib.parse.urlparse(newurl).scheme!="https":
            raise ValueError("Refusing non-HTTPS redirect")
        return super().redirect_request(req,fp,code,msg,headers,newurl)
opener=urllib.request.build_opener(NoRedirect)
with opener.open(req,timeout=90) as response, open("input.apkm","wb") as out:
    total=0
    while True:
        chunk=response.read(1024*1024)
        if not chunk: break
        total+=len(chunk)
        if total>250*1024*1024: raise ValueError("Bundle exceeds 250 MiB limit")
        out.write(chunk)
print("Downloaded input bundle; size:",total,"bytes")
