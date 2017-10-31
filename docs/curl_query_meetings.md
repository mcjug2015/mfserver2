# grabbing meetings with curl
You do not need to authenticate to get meetings. There are many different queries available
```
# grab meetings withing distance(in miles) from lat and long:
curl -f -k -v "https://127.0.0.1/mfserver2/api/v1/meeting/?lat=39&long=-77&distance=0.8"

# wednesday meetings that start after 7pm within distance from a point
curl -f -k -v "https://127.0.0.1/mfserver2/api/v1/meeting/?lat=39&long=-77&distance=10&day_of_week=4&start_time__gte=19:00"

# second page of wednesday meetings that start after 7pm within distance from a point
curl -f -k -v "https://127.0.0.1/mfserver2/api/v1/meeting/?lat=39&offset=20&distance=10&limit=20&long=-77&start_time__gte=19%3A00&day_of_week=4"

# meetings with the word happy in the name within distance from a point
curl -f -k -v "https://127.0.0.1/mfserver2/api/v1/meeting/?lat=39&long=-77&distance=10&name__icontains=happy"
```