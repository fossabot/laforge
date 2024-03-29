import pytest

from laforge.toolbox import flatten, is_reserved_word, verify_file_is_writable


class TestFlatten:
    @pytest.mark.parametrize(
        "incoming",
        [
            [],
            (),
            [[]],
            (()),
            [()],
            ([]),
            [[[]]],
            ((())),
            [[[]], [[]]],
            ([[]], [[]]),
            [([], [])],
            ((()), [[[]]]),
            ([[], []], [[[((((((([[]])))))))]]]),
            ([[], [[]], [[[]]], [[[[]]]]]),
        ],
    )
    def t_nothing_from_nothing_leaves_nothing(self, incoming):
        assert list(flatten(incoming)) == []

    @pytest.mark.parametrize(
        "incoming, output",
        [
            ([2], [2]),
            ([[2], [3]], [2, 3]),
            ([[3, [4]], 6], [3, 4, 6]),
            ([4, [4], 4, [4], 4, [[4]], [[]]], [4, 4, 4, 4, 4, 4]),
        ],
    )
    def t_flattens(self, incoming, output):
        assert list(flatten(incoming)) == output

    @pytest.mark.parametrize(
        "incoming, output",
        [
            (["spam"], ["spam"]),
            ([["spam"], ["eggs"]], ["spam", "eggs"]),
            ([["spam", ["eggs"]], "spam"], ["spam", "eggs", "spam"]),
            (
                ["spam", ["spam"], "spam", ["spam"], "spam", [["spam"]], [[]]],
                ["spam", "spam", "spam", "spam", "spam", "spam"],
            ),
        ],
    )
    def t_leaves_strings(self, incoming, output):
        assert list(flatten(incoming)) == output


class TestReservedWords:
    @pytest.mark.parametrize(
        "kw",
        [
            "else",
            "table",
            "row",
            "privileges",
            "view",
            "string",
            "time",
            "numeric",
            "close",
        ],
    )
    def t_reserved(self, kw):
        assert is_reserved_word(kw)

    @pytest.mark.parametrize(
        "kw", ["moomoo", "meowmeow", "woofwoof", "barkbark", "squeaksqueak", None]
    )
    def t_non_reserved(self, kw):
        assert not is_reserved_word(kw)


class TestVerifyFileIsWritable:
    def t_writable(self, tmpdir):
        writable_file = tmpdir / "harga's_house_of_ribs.txt"
        verify_file_is_writable(writable_file)

    @pytest.mark.xfail(reason="Need to sort out how to run this.")
    def t_unwritable(self, tmpdir):
        writable_file = tmpdir / "technical_journals.txt"
        with writable_file.open("a") as write_that:
            write_that.write("blah")
            with pytest.raises(PermissionError):
                verify_file_is_writable(writable_file)

