# Procyon

<a href="https://twitter.com/padres_watch" target="blank"><img src="https://img.shields.io/twitter/follow/padres_watch?logo=twitter&style=for-the-badge" alt="padres_watch" /></a> </p>

**Bot posts weekly on Mondays and Thursdays at 1230pm EST.**

<br />

> ### Resources used:
>
> - [AWS CDK](https://aws.amazon.com/cdk/) - Software development kit
>
> - [Twitter API](https://developer.twitter.com/en/docs/twitter-api) - API for Twitter access
>
> - [Baseball Reference](https://www.baseball-reference.com/leagues/majors/2022-playoff-odds.shtml) - MLB data for playoff odds
>
> - [MLB-StatsAPI](https://github.com/toddrob99/MLB-StatsAPI) - MLB data for team records

<br />

### Useful commands

- `pytest` run tests
- `cdk synth` emit synthesized CFT
- `cdk deploy` synthesize and deploy stack
- `cdk docs` open CDK documentation

<hr />

`requirements-layer.txt` holds dependencies for site packages to go in `/layers/python`

To set up Lambda dependencies in a Lambda Layer:
- Copy `requirements-layer.txt` to a new local virtualenv
- Install the dependencies with `$ pip install -r requirements-layer.txt`
- Copy the packages to `layer/python` with `$ rsync -a .venv/lib/<python-version>/site-packages <path/to/procyon>/layers/python`
