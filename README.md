# Procyon

<a href="https://twitter.com/padres_watch" target="blank"><img src="https://img.shields.io/twitter/follow/padres_watch?logo=twitter&style=for-the-badge" alt="padres_watch" /></a> </p>

## **Bot post schedule**

| Day                   |                               |
| --------------------- | ----------------------------- |
| Mon 1030 EST          | Last week's hitting leaders   |
| Mon 1100 EST          | Last week's pitching leaders  |
| Tue 1100 EST          | Season series results         |
| Wed 1100 EST          | Postseason update             |
| Thu 1100 EST          | Season team stats             |
| Fri 1230 EST          | Season series results         |
| Sat 1230 EST          | Postseason update             |
| 1st of month 1500 EST | Last month's hitting leaders  |
| 1st of month 1530 EST | Last month's pitching leaders |

<br />

> ### Resources used:
>
> - [AWS CDK](https://aws.amazon.com/cdk/) - Software development kit
>
> - [Twitter API](https://developer.twitter.com/en/docs/twitter-api) - API for Twitter access
>
> - [Baseball-Reference.com](https://www.baseball-reference.com/leagues/majors/2022-playoff-odds.shtml) - MLB data for playoff odds
>
> - [MLB.com](https://www.mlb.com/) - MLB data for team statistics and roster transactions
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
