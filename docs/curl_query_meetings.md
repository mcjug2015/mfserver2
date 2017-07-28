# grabbing meetings with curl
You do not need to authenticate to get meetings. There are many differnt queries available
```
# grab meetings withing distance(in miles) from lat and long:
curl -f -k -v "https://127.0.0.1/mfserver2/api/v1/meeting/?lat=39&long=-77&distance=0.8"
```