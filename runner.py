import sys
import io
import builtins
import time

def run_code(code, user_input=""):
    old_stdout = sys.stdout
    old_stdin = sys.stdin
    redirected_output = sys.stdout = io.StringIO()
    sys.stdin = io.StringIO(user_input)

    input_lines = user_input.splitlines()
    input_index = [0]

    original_input = builtins.input

    def fake_input(prompt=''):
        print(prompt, end='')
        if input_index[0] < len(input_lines):
            user_value = input_lines[input_index[0]]
            print(user_value)
            input_index[0] += 1
            return user_value
        return ''

    builtins.input = fake_input

    try:
        start_time = time.time()  # ⏱ Start timing
        exec(code, {})
        end_time = time.time()    # ⏱ End timing
        elapsed = end_time - start_time
        print(f"\n⏱ Execution Time: {elapsed:.4f} seconds")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Restore
    builtins.input = original_input
    sys.stdout = old_stdout
    sys.stdin = old_stdin

    return redirected_output.getvalue()
