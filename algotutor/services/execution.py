"""Code execution service for CB Algorithm Tutor."""

import ast
import re
import sys
import subprocess
import tempfile
import os
from typing import Dict, Any, Tuple, List
from contextlib import contextmanager
import io


class CodeExecutionService:
    """Service for safe code execution and testing."""
    
    def __init__(self):
        self.timeout_seconds = 10
        
    def execute_python_code(self, code: str, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute Python code with test cases and return results."""
        # Normalize indentation to avoid tab/space mix issues
        code = self.sanitize_code(code)
        results = {
            "success": False,
            "output": "",
            "errors": "",
            "test_results": [],
            "execution_time": 0,
            "syntax_valid": False
        }
        
        # First, check syntax
        try:
            ast.parse(code)
            results["syntax_valid"] = True
        except SyntaxError as e:
            msg = str(e)
            if "inconsistent use of tabs and spaces" in msg:
                msg += "\nHint: Your code mixes tabs and spaces. We try to auto-fix by converting tabs to 4 spaces; ensure your editor uses spaces for indentation."
            results["errors"] = f"Syntax Error: {msg}"
            return results
        
        # Execute code with test cases
        try:
            # Create a safe execution environment
            exec_globals = {
                "__builtins__": {
                    "len": len, "range": range, "enumerate": enumerate,
                    "zip": zip, "map": map, "filter": filter, "sorted": sorted,
                    "min": min, "max": max, "sum": sum, "abs": abs,
                    "print": print, "str": str, "int": int, "float": float,
                    "list": list, "dict": dict, "set": set, "tuple": tuple,
                }
            }
            
            # Execute the code
            exec_locals = {}
            exec(code, exec_globals, exec_locals)
            
            # Find the main function (assume first function defined)
            main_function = None
            for name, obj in exec_locals.items():
                if callable(obj) and not name.startswith('_'):
                    main_function = obj
                    break
            
            if main_function is None:
                results["errors"] = "No callable function found in code"
                return results
            
            # Run test cases
            passed_tests = 0
            for i, test_case in enumerate(test_cases):
                try:
                    input_args = test_case.get("input", [])
                    expected_output = test_case.get("expected", None)
                    
                    # Handle different input formats
                    if isinstance(input_args, list):
                        actual_output = main_function(*input_args)
                    else:
                        actual_output = main_function(input_args)
                    
                    test_passed = actual_output == expected_output
                    if test_passed:
                        passed_tests += 1
                    
                    results["test_results"].append({
                        "test_case": i + 1,
                        "input": input_args,
                        "expected": expected_output,
                        "actual": actual_output,
                        "passed": test_passed
                    })
                    
                except Exception as e:
                    results["test_results"].append({
                        "test_case": i + 1,
                        "input": input_args,
                        "expected": expected_output,
                        "actual": None,
                        "passed": False,
                        "error": str(e)
                    })
            
            results["success"] = passed_tests == len(test_cases)
            results["output"] = f"Passed {passed_tests}/{len(test_cases)} test cases"
            
        except Exception as e:
            results["errors"] = str(e)
        
        return results

    def sanitize_code(self, code: str) -> str:
        """Normalize user code prior to parsing/execution.

        - Normalize newlines to \n
        - Expand tabs to spaces using a width of 8 columns (Python's
          indentation semantics treat tabs as advancing to the next
          multiple of 8 columns). This preserves intended block depth
          when users indent with tabs inside already-indented blocks.
        """
        normalized = code.replace("\r\n", "\n").replace("\r", "\n")
        # Use Python-compatible tab expansion to avoid reducing indent depth
        return normalized.expandtabs(8)
    
    def analyze_complexity(self, code: str) -> Dict[str, str]:
        """Analyze time and space complexity of code (basic analysis)."""
        time_complexity = "O(1)"
        space_complexity = "O(1)"

        try:
            src = self.sanitize_code(code)
            tree = ast.parse(src)

            func_names = {n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}

            max_loop_depth = 0
            has_sorting = False
            has_recursion = False
            creates_new_data_structures = False

            def visit(node, depth):
                nonlocal max_loop_depth, has_sorting, has_recursion, creates_new_data_structures
                if isinstance(node, (ast.For, ast.While)):
                    depth += 1
                    max_loop_depth = max(max_loop_depth, depth)

                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Attribute) and node.func.attr in {"sort", "sorted"}:
                        has_sorting = True
                    if isinstance(node.func, ast.Name) and node.func.id in {"sorted"}:
                        has_sorting = True
                    if isinstance(node.func, ast.Name) and node.func.id in func_names:
                        has_recursion = True

                if isinstance(node, (ast.List, ast.Dict, ast.Set, ast.ListComp, ast.DictComp, ast.SetComp)):
                    creates_new_data_structures = True

                for child in ast.iter_child_nodes(node):
                    visit(child, depth)

            visit(tree, 0)

            if max_loop_depth >= 2:
                time_complexity = "O(n²)"
            elif max_loop_depth == 1:
                time_complexity = "O(n)"
            elif has_sorting:
                time_complexity = "O(n log n)"
            elif has_recursion:
                time_complexity = "O(n)"

            if creates_new_data_structures or has_recursion:
                space_complexity = "O(n)"

        except Exception:
            pass

        return {"time_complexity": time_complexity, "space_complexity": space_complexity}
    
    def run_with_timeout(self, code: str, timeout: int = None) -> Dict[str, Any]:
        """Run code with timeout protection."""
        if timeout is None:
            timeout = self.timeout_seconds
            
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            # Execute with timeout
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "errors": result.stderr,
                "timeout": False
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "output": "",
                "errors": f"Code execution timed out after {timeout} seconds",
                "timeout": True
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "errors": str(e),
                "timeout": False
            }
        finally:
            # Clean up temporary file
            if 'temp_file' in locals():
                try:
                    os.unlink(temp_file)
                except OSError:
                    pass


# Global code execution service instance
code_execution_service = CodeExecutionService()
