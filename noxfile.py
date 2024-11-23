import nox

nox.options.sessions = ['lint', 'typing', 'tests', 'coverage_report']


@nox.session(tags=['all'])
def lint(session):
    session.run('flake8', 'mortar', 'test', external=True)


@nox.session(tags=['all'])
def typing(session):
    session.run('mypy', external=True)


@nox.session(tags=['all'])
def tests(session):
    session.run('coverage', 'run', '--branch', '-m', 'pytest', external=True)


@nox.session(tags=['all'])
def data_tests(session):
    session.run('coverage', 'run', '--append', '--branch', '-m', 'pytest',
                'test/test_jp.py', external=True)


@nox.session(tags=['all'])
def coverage_report(session):
    session.run('coverage', 'report', external=True)
