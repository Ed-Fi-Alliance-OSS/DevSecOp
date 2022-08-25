# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

from datetime import datetime, timedelta
import pytest

from unittest.mock import MagicMock
from edfi_repo_auditor.auditor import ALERTS_WEEKS_SINCE_CREATED, audit_alerts
from edfi_repo_auditor.checklist import CHECKLIST
from edfi_repo_auditor.github_client import GitHubClient

ACCESS_TOKEN = "asd09uasdfu09asdfj;iolkasdfklj"
OWNER = "Ed-Fi-Alliance-OSS"
REPO = "Ed-Fi-ODS"
CLIENT = GitHubClient(ACCESS_TOKEN)


def describe_when_auditing_alerts() -> None:
    def describe_dependabot_alerts() -> None:
        def describe_given_is_not_enabled() -> None:
            ALERTS = []

            @pytest.fixture
            def results() -> dict:
                CLIENT.has_dependabot_enabled = MagicMock(return_value=False)
                return audit_alerts(CLIENT, OWNER, REPO, ALERTS)

            def it_returns_dependabot_enabled(results: dict) -> None:
                assert results[CHECKLIST.DEPENDABOT_ENABLED["description"]] == CHECKLIST.DEPENDABOT_ENABLED["error"]

            def it_returns_no_alerts(results: dict) -> None:
                assert results[CHECKLIST.DEPENDABOT_ALERTS["description"]] == CHECKLIST.DEPENDABOT_ALERTS["success"]

        def describe_given_is_enabled() -> None:
            ALERTS = []

            @pytest.fixture
            def results() -> dict:
                CLIENT.has_dependabot_enabled = MagicMock(return_value=True)
                return audit_alerts(CLIENT, OWNER, REPO, ALERTS)

            def it_returns_dependabot_enabled(results: dict) -> None:
                assert results[CHECKLIST.DEPENDABOT_ENABLED["description"]] == CHECKLIST.DEPENDABOT_ENABLED["success"]

        def describe_given_there_are_no_alerts() -> None:
            ALERTS = []

            @pytest.fixture
            def results() -> dict:
                CLIENT.has_dependabot_enabled = MagicMock(return_value=True)
                return audit_alerts(CLIENT, OWNER, REPO, ALERTS)

            def it_returns_no_alerts(results: dict) -> None:
                assert results[CHECKLIST.DEPENDABOT_ENABLED["description"]] == CHECKLIST.DEPENDABOT_ENABLED["success"]

        def describe_given_there_are_alerts_not_old() -> None:
            ALERTS = [
                {
                    "createdAt": (datetime.now() - timedelta((ALERTS_WEEKS_SINCE_CREATED - 1) * 7)).isoformat(),
                    "securityVulnerability": {
                        "package": {
                            "name": "minimist"
                        },
                        "advisory": {
                            "severity": "CRITICAL"
                        }
                    }
                }
            ]

            @pytest.fixture
            def results() -> dict:
                CLIENT.get_repository_information = MagicMock(return_value=True)
                return audit_alerts(CLIENT, OWNER, REPO, ALERTS)

            def it_returns_no_alerts(results: dict) -> None:
                assert results[CHECKLIST.DEPENDABOT_ALERTS["description"]] == CHECKLIST.DEPENDABOT_ALERTS["success"]

        def describe_given_there_are_old_alerts_not_severe() -> None:
            ALERTS = [
                {
                    "createdAt": (datetime.now() - timedelta((ALERTS_WEEKS_SINCE_CREATED + 1) * 7)).isoformat(),
                    "securityVulnerability": {
                        "package": {
                            "name": "minimist"
                        },
                        "advisory": {
                            "severity": "WARNING"
                        }
                    }
                },
                {
                    "createdAt": (datetime.now() - timedelta((ALERTS_WEEKS_SINCE_CREATED - 1) * 7)).isoformat(),
                    "securityVulnerability": {
                        "package": {
                            "name": "minimist"
                        },
                        "advisory": {
                            "severity": "HIGH"
                        }
                    }
                }
            ]

            @pytest.fixture
            def results() -> dict:
                CLIENT.get_repository_information = MagicMock(return_value=True)
                return audit_alerts(CLIENT, OWNER, REPO, ALERTS)

            def it_returns_no_alerts(results: dict) -> None:
                assert results[CHECKLIST.DEPENDABOT_ALERTS["description"]] == CHECKLIST.DEPENDABOT_ALERTS["success"]

        def describe_given_there_are_critical_risk_alerts_not_old() -> None:
            ALERTS = [
                {
                    "createdAt": (datetime.now() - timedelta((ALERTS_WEEKS_SINCE_CREATED - 1) * 7)).isoformat(),
                    "securityVulnerability": {
                        "package": {
                            "name": "minimist"
                        },
                        "advisory": {
                            "severity": "CRITICAL"
                        }
                    }
                }
            ]

            @pytest.fixture
            def results() -> dict:
                CLIENT.has_dependabot_enabled = MagicMock(return_value=True)
                return audit_alerts(CLIENT, OWNER, REPO, ALERTS)

            def it_returns_no_alerts(results: dict) -> None:
                assert results[CHECKLIST.DEPENDABOT_ALERTS["description"]] == CHECKLIST.DEPENDABOT_ALERTS["success"]

        def describe_given_there_are_old_critical_risk_alerts() -> None:
            ALERTS = [
                {
                    "createdAt": (datetime.now() - timedelta((ALERTS_WEEKS_SINCE_CREATED + 1) * 7)).isoformat(),
                    "securityVulnerability": {
                        "package": {
                            "name": "minimist"
                        },
                        "advisory": {
                            "severity": "CRITICAL"
                        }
                    }
                }
            ]

            @pytest.fixture
            def results() -> dict:
                CLIENT.get_repository_information = MagicMock(return_value=True)
                return audit_alerts(CLIENT, OWNER, REPO, ALERTS)

            def it_returns_warning(results: dict) -> None:
                assert results[CHECKLIST.DEPENDABOT_ALERTS["description"]] == CHECKLIST.DEPENDABOT_ALERTS["error"]

        def describe_given_there_are_old_high_risk_alerts() -> None:
            ALERTS = [
                {
                    "createdAt": (datetime.now() - timedelta((ALERTS_WEEKS_SINCE_CREATED + 1) * 7)).isoformat(),
                    "securityVulnerability": {
                        "package": {
                            "name": "minimist"
                        },
                        "advisory": {
                            "severity": "HIGH"
                        }
                    }
                }
            ]

            @pytest.fixture
            def results() -> dict:
                CLIENT.get_repository_information = MagicMock(return_value=True)
                return audit_alerts(CLIENT, OWNER, REPO, ALERTS)

            def it_returns_warning(results: dict) -> None:
                assert results[CHECKLIST.DEPENDABOT_ALERTS["description"]] == CHECKLIST.DEPENDABOT_ALERTS["error"]
