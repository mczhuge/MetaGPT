#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio

import fire

from metagpt.roles import (
    Architect,
    Engineer,
    ProductManager,
    ProjectManager,
    QaEngineer,
)
from metagpt.software_company import SoftwareCompany


async def startup(
    idea: str,
    investment: float = 3.0,
    n_round: int = 5,
    code_review: bool = False,
    run_tests: bool = False,
    implement: bool = True,
    self_improvement: bool = False,
):
    """Run a startup. Be a boss."""
    company = SoftwareCompany()
    company.invest(investment)

    company.hire(
        [
            ProductManager(feedback = self_improvement),
            Architect(feedback = self_improvement),
            ProjectManager(feedback = self_improvement),
        ]
    )

    # if implement or code_review
    if implement or code_review:
        # developing features: implement the idea
        company.hire([Engineer(n_borg=5, use_code_review=code_review, feedback = self_improvement)])

    if run_tests:
        # developing features: run tests on the spot and identify bugs
        # (bug fixing capability comes soon!)
        company.hire([QaEngineer()])
    
    if self_improvement:
        company.improvement(initial=True)

    company.start_project(idea)
    await company.run(n_round=n_round)

    if self_improvement:
        company.improvement(roles = company.environment.get_roles())


def main(
    idea: str,
    investment: float = 3.0,
    n_round: int = 5,
    code_review: bool = True,
    run_tests: bool = False,
    implement: bool = True,
):
    """
    We are a software startup comprised of AI. By investing in us,
    you are empowering a future filled with limitless possibilities.
    :param idea: Your innovative idea, such as "Creating a snake game."
    :param investment: As an investor, you have the opportunity to contribute
    a certain dollar amount to this AI company.
    :param n_round:
    :param code_review: Whether to use code review.
    :return:
    """
    asyncio.run(startup(idea, investment, n_round, code_review, run_tests, implement))


if __name__ == "__main__":
    fire.Fire(main)
