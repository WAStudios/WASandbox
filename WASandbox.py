import os
import lupa
from lupa import LuaRuntime

from stubs.wa_getlibs import getlibs
from stubs.get_dependencies import ensure_wa_repo
from stubs.wow_api import register_wow_stubs
from stubs.libstub import inject_libstub
from stubs.weak_auras_private import inject_weak_auras_private
from stubs.sandbox_stubs import inject_sandbox_stubs
from stubs.addon_env import inject_addon_env
from stubs.toc_parse import parse_toc

# Step 1: Prepare libraries and assets
getlibs()
ensure_wa_repo()

# Step 2: Initialize Lua runtime
lua_runtime = LuaRuntime(unpack_returned_tuples=True)

# Step 3: Set up Blizzard WoW API stubs
register_wow_stubs(lua_runtime)

# Step 4: Inject necessary environments and WeakAuras-specific hooks
inject_libstub(lua_runtime)
inject_weak_auras_private(lua_runtime)
inject_sandbox_stubs(lua_runtime)
inject_addon_env(lua_runtime)

# Step 5: Parse the TOC file for Lua load order
weak_auras_base_path = os.path.join(os.getcwd(), "WeakAuras2", "WeakAuras")
toc_path = os.path.join(weak_auras_base_path, "WeakAuras.toc")
lua_files_order = parse_toc(toc_path)

# Step 6: Load all Lua files in the correct order, handling WeakAuras.lua specially
def load_wa_lua_files(lua_env, lua_files):
    for filepath in lua_files:
        full_path = os.path.join(weak_auras_base_path, filepath)

        if filepath.endswith("WeakAuras.lua"):
            with open(full_path, 'r', encoding='utf-8') as f:
                code = f.read()
            lines = code.splitlines()
            execenv_index = next((i for i, line in enumerate(lines) if "ExecEnv = setmetatable(" in line), -1)
            if execenv_index != -1:
                pre_execenv = "\n".join(lines[:execenv_index])
                post_execenv = "\n".join(lines[execenv_index:])
                wrapped_post_execenv = f"""
                local WeakAuras = _G.WeakAuras
                local Private = WeakAuras.Private
                local _G = _G
                {post_execenv}
                """
                print(f"--- Loading pre-ExecEnv for {filepath} ---")
                lua_env.execute(pre_execenv)
                print(f"--- Loading post-ExecEnv for {filepath} ---")
                lua_env.execute(wrapped_post_execenv)
            else:
                print(f"Could not locate ExecEnv in {filepath}, executing whole file")
                lua_env.execute(code)
        else:
            try:
                print(f"Attempting to load: {full_path}")
                with open(full_path, 'r', encoding='utf-8') as f:
                    lua_env.execute(f.read())
                print(f"--- Finished loading {filepath} ---\n")
            except Exception as e:
                print(f"Error loading {filepath}: {e}")


load_wa_lua_files(lua_runtime, lua_files_order)

# --- Old hardcoded loader (REPLACED by TOC-based loading) ---
"""
priority_files = [
    "libs/AceTimer-3.0/AceTimer-3.0.lua",
    "libs/CallbackHandler-1.0/CallbackHandler-1.0.lua",
    # ... (and more)
]

def load_wa_lua_files(lua_env):
    for filepath in priority_files:
        # Static loading logic (deprecated)
        pass
"""

# Optional update loop (can be refined later)
print("Update loop started")
while True:
    pass