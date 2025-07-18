# JiraHourPlanner
UI for planning hours before automatically logging them to jira.
```
docker pull maximilianosapien/jirahourplanner:latest
```
-----
Start the container under a folder like "jirahourplanner" and set your Jira instance, email and Jira-token through the UI.
```
docker run --rm -d --name jirahourplanner -p 5001:5000 -v "$(pwd)/data:/app/data" maximilianosapien/jirahourplanner:latest
```
## Features
- Time logging per day
- Time logging for past days
- Jump back/forward by N weeks
- Edit & delete activities
- Daily totals
- Jira integration
- Time loggin duplication detection per day
-----
<img width="1918" height="957" alt="image" src="https://github.com/user-attachments/assets/d2a4066a-529d-4a59-96b0-f3669182c044" />
<img width="1330" height="682" alt="image" src="https://github.com/user-attachments/assets/81952370-31db-4542-a9d6-34fd6668cacc" />
<img width="1326" height="793" alt="image" src="https://github.com/user-attachments/assets/4cf9f54e-5a1e-4100-ac9b-404d2331d665" />
