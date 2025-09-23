from algotutor.services.execution import code_execution_service


def test_tabs_inside_block_preserve_indent_depth():
    # Function line unindented, for-block with 4 spaces, inner body starts with a tab
    # This mirrors editors that mix spaces (outer) and tabs (inner)
    code = (
        "def foo(nums):\n"
        "    for x in nums:\n"  # 4 spaces
        "\treturn x\n"  # leading tab should expand to 8 spaces, deeper than 4
    )

    sanitized = code_execution_service.sanitize_code(code)
    # Should parse without SyntaxError
    result = code_execution_service.execute_python_code(
        sanitized,
        test_cases=[{"input": [[1, 2, 3]], "expected": 1}],
    )
    assert result["syntax_valid"] is True
    assert result["success"] is True

