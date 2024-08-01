# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from settings import Configuration, load_from_env
from jira_browser import JiraBrowser, IssuePage, EdFiIssue

from github import Github
from github import Auth
import time


config: Configuration = load_from_env()
jira: JiraBrowser = JiraBrowser(config)

gh_auth = Auth.Token(config.github_token)
gh_client = Github(auth=gh_auth)

repo = gh_client.get_repo(config.github_repository)


def create_github_issue(issue: EdFiIssue) -> None:
    if len(issue.attachments) > 0:
        config.info(f"Attachments found in {issue.issue_key}")

    gh_issue = repo.create_issue(
        title=issue.title,
        body=issue.create_gh_description(),
        labels=issue.get_gh_labels()
        # milestone needs to exist first
        # milestone=i.fixVersion
    )
    # GitHub recommends: "wait at least one second between each request. This will help you avoid secondary rate limits."
    time.sleep(2)

    if issue.status == "Done":
        gh_issue.edit(state="closed")
        time.sleep(1)

    for c in issue.comments:
        gh_issue.create_comment(c.create_gh_comment())
        time.sleep(1)


begin = ""
while True:
    page: IssuePage = jira.get_page_of_issues(config.project_key, begin)

    for i in range(len(page.issue_list)):
        create_github_issue(page.issue_list[i])

    if page.last_key == "":
        break

    # Next request to get_issues needs to look for items _after_ the last one received
    begin = page.last_key or ""
