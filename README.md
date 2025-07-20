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
<img width="1919" height="956" alt="image" src="https://github.com/user-attachments/assets/ca14d09d-59b2-496c-af83-77f652028425" />
<img width="1919" height="955" alt="image" src="https://github.com/user-attachments/assets/a7815a26-3cd2-40ec-b43f-bc961e4a3164" />
<img width="1919" height="955" alt="image" src="https://github.com/user-attachments/assets/0be376c8-0849-466d-b970-dd940e12bdeb" />
<img width="1919" height="956" alt="image" src="https://github.com/user-attachments/assets/ce95e308-35e0-4ca7-a442-4cdc85c88686" />

## Future-development
This was a fun project to develop and I intend to work on the interface/navigation or any bugs that are reported.<br>
[Support cool projects like this one! :)](https://www.paypal.com/donate/?hosted_button_id=SRATUX8VNHC9G)
