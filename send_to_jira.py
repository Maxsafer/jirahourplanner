from jira import JIRA

def send_to_jira(activities: list[dict], jira_url: str, email: str, api_token: str):
    jira = JIRA(server=jira_url, basic_auth=(email, api_token))
    logs = []

    for activity in activities:
        issue_key  = activity.get("id")
        hours      = activity.get("hours")
        comment    = activity.get("description")

        if not issue_key or hours is None or not comment:
            logs.append(f"❌ Skipping incomplete activity: {activity!r}")
            continue

        # Fetch the issue
        try:
            issue = jira.issue(issue_key)
        except Exception as e:
            msg = getattr(e, 'text', None)
            logs.append(f"❌ Could not fetch issue {issue_key}: {msg}")
            continue
        
        # Fetch existing worklogs for that issue
        try:
            existing = jira.worklogs(issue_key)
        except Exception as e:
            msg = getattr(e, 'text', None)
            logs.append(f"❌ Could not load worklogs for {issue_key}: {msg}")
            existing = []
        
        # Check for a duplicate (same hours & comment by you)
        dup = False
        target_seconds = int(hours * 3600)
        for wl in existing:
            # wl.timeSpentSeconds, wl.comment, wl.author.emailAddress
            wl_sec  = getattr(wl, "timeSpentSeconds", None)
            wl_comm = getattr(wl, "comment", "").strip()
            wl_auth = getattr(wl.author, "emailAddress", None)
            if wl_sec == target_seconds and wl_comm == comment and wl_auth == email:
                logs.append(f"⚠️ Already logged {hours}h to {issue_key} with comment: “{comment}”")
                dup = True
                break
        if dup:
            continue

        # No duplicate, log it
        try:
            timeSpentFormatted=f"{str(hours).split(".")[0]}h {6*int(str(hours).split(".")[1])}m"
            print(timeSpentFormatted)
            jira.add_worklog(
                issue=issue,
                timeSpent=timeSpentFormatted,
                comment=comment
            )
            logs.append(f"✅ Logged {hours}h to {issue_key}: “{comment}”")
        except Exception as e:
            logs.append(f"❌ Failed to log work on {issue_key}: {e}")

    return logs