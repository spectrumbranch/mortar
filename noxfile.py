import nox


@nox.session()
def lint(session):
    session.run('flake8', 'mortar', 'test', external=True)


@nox.session()
def typing(session):
    session.run('mypy', external=True)


@nox.session()
def tests(session):
    session.run('coverage', 'run', '-m', 'pytest', external=True)
    session.run('coverage', 'report', external=True)
