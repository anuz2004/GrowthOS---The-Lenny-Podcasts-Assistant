1. USERS :- 

id
name
email
created_at

2. WORKSPACES :-

id
user_id
title
description
model
created_at

3. SESSIONS :-

id
workspace_id
created_at

4. MESSAGES :-

id
session_id
role
content
citations
confidence
created_at

5. ARTIFACTS :-

id
workspace_id
type
markdown/html/react
title
content
version
created_at

6. NOTEBOOK :-

id
workspace_id
title
content
category

7. TRANSCRIPT_CHUNKS:-

id
episode
speaker
chunk
embedding

8. AGENT LOGS:-

id
agent
input
output
execution_time

9. SETTINGS:-

id
workspace_id
selected_model
temperature
system_prompt