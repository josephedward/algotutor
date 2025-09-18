"""Code execution service for CB Algorithm Tutor."""

import ast
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
            results["errors"] = f"Syntax Error: {str(e)}"
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
    
    def analyze_complexity(self, code: str) -> Dict[str, str]:
        """Analyze time and space complexity of code (basic analysis)."""
        # Simple heuristic-based complexity analysis
        time_complexity = "O(1)"
        space_complexity = "O(1)"
        
        try:
            tree = ast.parse(code)
            
            has_nested_loops = False
            has_single_loop = False
            has_recursion = False
            has_sorting = False
            creates_new_data_structures = False
            
            for node in ast.walk(tree):
                if isinstance(node, ast.For):
                    # Check for nested loops
                    for child in ast.walk(node):
                        if isinstance(child, ast.For) and child != node:
                            has_nested_loops = True
                        else:
                            has_single_loop = True
                
                elif isinstance(node, ast.While):
                    has_single_loop = True
                
                elif isinstance(node, ast.FunctionDef):
                    # Check for recursive calls
                    for child in ast.walk(node):
                        if (isinstance(child, ast.Call) and 
                            isinstance(child.func, ast.Name) and 
                            child.func.id == node.name):
                            has_recursion = True
                
                elif isinstance(node, ast.Call):
                    if (isinstance(node.func, ast.Attribute) and 
                        node.func.attr in ["sort", "sorted"]):
                        has_sorting = True
                    elif (isinstance(node.func, ast.Name) and 
                          node.func.id in ["sorted"]):
                        has_sorting = True
                
                elif isinstance(node, (ast.List, ast.Dict, ast.Set)):
                    if len(node.elts if hasattr(node, 'elts') else 
                           (node.keys if hasattr(node, 'keys') else [])) > 0:
                        creates_new_data_structures = True
            
            # Determine time complexity
            if has_nested_loops:
                time_complexity = "O(n²)"
            elif has_single_loop:
                time_complexity = "O(n)"
            elif has_recursion:
                time_complexity = "O(n)" # Simplified assumption
            elif has_sorting:
                time_complexity = "O(n log n)"
            
            # Determine space complexity
            if creates_new_data_structures or has_recursion:
                space_complexity = "O(n)"
                
        except Exception:
            pass  # Fall back to default values
        
        return {
            "time_complexity": time_complexity,
            "space_complexity": space_complexity
        }
    
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
