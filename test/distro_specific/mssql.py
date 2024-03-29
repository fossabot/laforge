import pytest
from laforge.sql import Channel, Table, Script, execute
from laforge.distros import Distro


@pytest.mark.mssql
def test_do_not_add_foolish_semicolon(make_channel):
    c = make_channel("mssql")
    Script(
        """
    SELECT 1 FROM SYS.TABLES;
    GO
    SELECT 1 FROM SYS.TABLES
    GO""",
        channel=c,
    ).execute()


@pytest.mark.mssql
@pytest.mark.xfail
def test_errors_being_swallowed(test_channel):
    raw = """
    use IRISpii;

    select * from linkage.sodifjsd;

    if object_id('IRISpii.linkage.setup_for_reparsing') is not null drop table IRISpii.linkage.setup_for_reparsing;

    CREATE TABLE [linkage].[setup_for_reparsing](
        [display_id] [int] NULL,
        [new_emp_number] [varchar](200) NULL,
        [last_name] [varchar](50) NULL,
        [first_name] [varchar](50) NULL,
        [middle_name] [varchar](50) NULL,
        [full_name] [varchar](200) NOT NULL
    ) ON [PRIMARY];

    with fulled as (
        select
            *,
            concat(rtrim(replace(emp_last_name, ',', '')), ', ', rtrim(emp_first_name), ' '+rtrim(middle_name)) as full_name
        from linkage.sdaoifjs
    )
    insert into linkage.setup_for_reparsing (display_id, new_emp_number, last_name, first_name, middle_name, full_name)
    select * from fulled;

    go """
    with pytest.raises(Exception):
        Script(raw, channel=test_channel).execute()


@pytest.mark.mssql
def test_do_not_add_foolish_semicolon(make_channel):
    c = make_channel("mssql")
    Script(
        """
    SELECT 1 FROM SYS.TABLES;
    GO
    SELECT 1 FROM SYS.TABLES
    GO""",
        channel=c,
    ).execute()


STATEMENTS = {
    "mssql": "select top 10 name, schema_id, type_desc from sys.tables;",
    "postgresql": "select * from pg_class where oid >= 13015;",
}


def test_script_or_execute_to_df(secrets):
    c = Channel(**secrets["sql"])
    stmt = STATEMENTS.get(c.distro.name)
    if not stmt:
        pytest.skip()
    scripted_r = Script(stmt).read()
    executed_r = execute(stmt, fetch="df")
    assert scripted_r.equals(executed_r)

    scripted_t = list(Script(stmt).read().itertuples(name=None, index=False))
    executed_t = list(tuple(x) for x in execute(stmt, fetch="tuples"))
    assert scripted_t == executed_t


@pytest.mark.mssql
def test_do_not_add_foolish_semicolon(make_channel):
    c = make_channel("mssql")
    Script(
        """
    SELECT 1 FROM SYS.TABLES;
    GO
    SELECT 1 FROM SYS.TABLES
    GO""",
        channel=c,
    ).execute()
