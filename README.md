# jirahourplanner
UI for planning hours before automatically logging them to jira.
```
docker pull maximilianosapien/jirahourplanner:latest
```
-----
Start the container under a folder like "jirahourplanner" and set your Jira instance through the UI, please configure you ```data/user.env``` variables after that.
```
docker run --rm -d --name jirahourplanner -p 5001:5000 -v "$(pwd)/data:/app/data" maximilianosapien/jirahourplanner:latest
```
