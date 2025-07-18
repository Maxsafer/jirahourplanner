from jira import JIRA
from datetime import datetime, date
from zoneinfo import ZoneInfo

def send_to_jira(activities: list[dict], jira_url: str, email: str, api_token: str, log_date: date):
    logs = []
    if not jira_url or not email or not api_token:
        return ["Environment variable missing..."]
    jira = JIRA(server=jira_url, basic_auth=(email, api_token))

    for activity in activities:
        issue_key  = activity.get("id")
        hours      = activity.get("hours")
        comment    = activity.get("description")
        htmlurlkey = f"<a href='{jira_url}/browse/{issue_key}' target='_blank'>{issue_key}</a>:"

        if not issue_key or hours is None or not comment:
            logs.append(f"❌ Skipping incomplete activity: {activity!r}")
            continue

        # Fetch the issue
        try:
            issue = jira.issue(issue_key)
        except Exception as e:
            msg = getattr(e, 'text', None)
            logs.append(f"❌ Could not fetch issue {htmlurlkey}: {msg}")
            continue
        
        # Fetch existing worklogs for that issue
        try:
            existing = jira.worklogs(issue_key)
        except Exception as e:
            msg = getattr(e, 'text', None)
            logs.append(f"❌ Could not load worklogs for {htmlurlkey}: {msg}")
            existing = []
        
        # Check for a duplicate (same hours & comment by you)
        dup = False
        target_seconds = int(hours * 3600)
        for wl in existing:
            try:
                wl_date = datetime.strptime(wl.started[:10], '%Y-%m-%d').date()
            except Exception:
                continue

            # skip if it's not the same day
            if wl_date != log_date:
                continue

            # wl.timeSpentSeconds, wl.comment, wl.author.emailAddress
            wl_sec  = getattr(wl, "timeSpentSeconds", None)
            wl_comm = getattr(wl, "comment", "").strip()
            wl_auth = getattr(wl.author, "emailAddress", None)

            if wl_sec == target_seconds and wl_comm == comment and wl_auth == email:
                logs.append(f"⚠️ Already logged {hours}h to {htmlurlkey} with comment: “{comment}”")
                dup = True
                break
        if dup:
            continue

        # No duplicate, log it
        try:
            timeSpentFormatted=f"{str(hours).split(".")[0]}h {6*int(str(hours).split(".")[1])}m"
            tz = datetime.now().astimezone().tzinfo
            started_dt = datetime(
                log_date.year,
                log_date.month,
                log_date.day,
                9, 0,  # 9:00 AM
                tzinfo=tz
            )

            jira.add_worklog(
                issue=issue,
                timeSpent=timeSpentFormatted,
                comment=comment,
                started=started_dt
            )
            logs.append(f"✅ Logged {hours}h to {htmlurlkey}: “{comment}”")
        except Exception as e:
            logs.append(f"❌ Failed to log work on {htmlurlkey}: {e}")

    return logs