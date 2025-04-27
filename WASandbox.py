from get_dependencies import ensure_wa_repo
from stubs.libstub import inject_libstub
from stubs.wow_api import inject_wow_api
from stubs.weak_auras_private import inject_weak_auras_private
from stubs.addon_env import inject_addon_env
from stubs.sandbox_stubs import inject_sandbox_stubs
from wa_getlibs import getlibs

from wase_core.engine import WASEngine
from wase_api.math import register_math

import wase_core
print("WASEngine loaded from:", wase_core.__file__)


import sys
import os
import glob

# Ensure WASEngine is recognized properly in sys.path
wase_path = os.path.abspath("./WASEngine")
if wase_path not in sys.path:
    sys.path.insert(0, wase_path)

# Step 1: Ensure latest WeakAuras2, WASEngine repos and WeakAuras Libraries
ensure_wa_repo()
getlibs()

# Initialize WASEngine
engine = WASEngine()
lua_runtime = engine.lua
lua_globals = lua_runtime.globals()

# Force-inject IsRetail
lua_runtime.execute("""
  _G.IsRetail = function() return true end
  IsRetail = _G.IsRetail
  """)

# Inject Stubs
inject_libstub(lua_runtime)
inject_sandbox_stubs(lua_runtime)

print("WeakAuras.Private initialized:", lua_runtime.execute("return type(WeakAuras.Private)"))
print("_G.Private initialized:", lua_runtime.execute("return type(_G.Private)"))

inject_wow_api(lua_runtime)
inject_weak_auras_private(lua_runtime)
inject_addon_env(lua_runtime)

lib_files = sorted(glob.glob('./libs/**/*.lua', recursive=True))
# Prioritize ChatThrottleLib if embedded
priority_files = [
    "./libs/AceTimer-3.0/AceTimer-3.0.lua",
    #"./WeakAuras2/WeakAuras/RegionTypes/init.lua",
    "./WeakAuras2/WeakAurasOptions/RegionOptions/Icon.lua",
    "./WeakAuras2/WeakAuras/SubRegionTypes/Glow.lua",
    #"./libs/LibCustomGlow-1.0/LibCustomGlow-1.0.lua",
    "./WeakAuras2/WeakAuras/RegionTypes/Icon.lua",
    "./WeakAuras2/WeakAuras/WeakAuras.lua",
    "./libs/LibDBIcon-1.0/LibDBIcon-1.0.lua",
    "./libs/AceComm-3.0/AceComm-3.0.lua",
    "./libs/AceConfig-3.0/AceConfigRegistry-3.0/AceConfigRegistry-3.0.lua",
    "./libs/LibGetFrame-1.0/LibGetFrame-1.0.lua",
    "./libs/LibRangeCheck-3.0/LibRangeCheck-3.0/LibRangeCheck-3.0.lua",
    "./WeakAuras2/WeakAuras/Prototypes.lua",
    "./libs/AceConfig-3.0/AceConfigCmd-3.0/AceConfigCmd-3.0.lua",
    "./libs/LibSerialize/LibSerialize.lua",
    "./WeakAuras2/WeakAuras/Transmission.lua",
    "./WeakAuras2/WeakAuras/AuraEnvironment.lua",
    "./libs/Archivist/Archivist.lua",
    "./libs/LibSpellRange-1.0/LibSpellRange-1.0.lua",
    "./WeakAuras2/WeakAuras/Profiling.lua",
    "./WeakAuras2/WeakAuras/BuffTrigger2.lua",
    "./WeakAuras2/WeakAuras/LibSpecializationWrapper.lua",
    "./WeakAuras2/WeakAurasOptions/OptionsFrames/CodeReview.lua",
    "./WeakAuras2/WeakAurasOptions/RegionOptions/Text.lua",
    "./WeakAuras2/WeakAuras/SubRegionTypes/SubText.lua",
    "./WeakAuras2/WeakAuras/RegionTypes/DynamicGroup.lua",
    "./WeakAuras2/WeakAurasOptions/ConditionOptions.lua",
    "./WeakAuras2/WeakAurasOptions/AceGUI-Widgets/AceGuiWidget-WeakAurasMediaSound.lua",
    "./libs/AceGUI-3.0-SharedMediaWidgets/SoundWidget.lua",
    "./WeakAuras2/WeakAurasOptions/OptionsFrames/TextEditor.lua",
    "./libs/AceGUI-3.0-SharedMediaWidgets/BackgroundWidget.lua",
]


other_files = [f for f in lib_files if 'ChatThrottleLib.lua' not in f]

print("Expecting AceTimer-3.0 at:", os.path.abspath("./libs/AceTimer-3.0/AceTimer-3.0.lua"))
print("Exists:", os.path.exists("./libs/AceTimer-3.0/AceTimer-3.0.lua"))


# Load Lua Files
for lib_file in priority_files + other_files:
    full_path = os.path.abspath(lib_file)

    if "AceTimer-3.0.lua" in full_path:
        print(f"DEBUG: About to load AceTimer-3.0 from {full_path}")

    print(f"Attempting to load: {full_path}")  # Debug: Full resolved path

    # Re-inject math to ensure it's available
    register_math(lua_runtime)

    try:
        print(f"--- Loading {lib_file} ---")
        print("math.min pre-load:", lua_runtime.execute("return math.min(5, 4)"))

        with open(full_path, 'r', encoding='utf-8') as f:

            if "RegionTypes/Icon.lua" in lib_file:
                lua_runtime.execute("""
                print("Injecting DEBUG stub for AddProgressSourceToDefault")
                WeakAuras = WeakAuras or {}
                WeakAuras.AddProgressSourceToDefault = WeakAuras.AddProgressSourceToDefault or function(...) print("Stub: WeakAuras.AddProgressSourceToDefault called", ...) end
                Private = Private or {}
                Private.regionPrototype = Private.regionPrototype or {}
                Private.regionPrototype.AddProgressSourceToDefault = function(...) print("Stub: Private.regionPrototype.AddProgressSourceToDefault called", ...) end
                """)

            lua_runtime.execute(f.read())

        print("Lua LibStub type:", engine.lua.eval("type(LibStub)"))  # should be 'table'
        print(f"--- Finished loading {lib_file} ---\n")

    except Exception as e:
        print(f"Error loading {lib_file}: {e}")
        import traceback
        traceback.print_exc()
        break  # Optionally stop on the first error



# Load WeakAuras Files with Special Handling for WeakAuras.lua
def load_wa_lua_files(lua_env, base_path="WeakAuras2/WeakAuras"):
    lua_files = [
        "WeakAuras.lua",
        "Transmission.lua",
        "Core.lua",
        "RegionTypes/init.lua"
    ]

    for file in lua_files:
        full_path = os.path.join(base_path, file)
        if os.path.exists(full_path):
            if file == "WeakAuras.lua":
                with open(full_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    pre_execenv = "".join(lines[:406])
                    post_execenv = "".join(lines[406:])

                    # Load part 1
                    lua_env.execute(pre_execenv)

                    # Re-inject ExecEnv and frames
                    lua_env.execute("""
                    local Private = WeakAuras.Private
                    Private.ExecEnv = Private.ExecEnv or {}
                    local ExecEnv = Private.ExecEnv
                    WeakAuras.ExecEnv = ExecEnv

                    Private.frames = Private.frames or {}
                    WeakAuras.frames = Private.frames
                    """)

                    # Re-inject IsRetail before part 2
                    lua_env.execute("""
                    _G.IsRetail = function() return true end
                    IsRetail = _G.IsRetail
                    """)

                    # Load part 2
                    wrapped_post_execenv = f"""
                    local Private = WeakAuras.Private
                    local ExecEnv = Private.ExecEnv
                    {post_execenv}
                    """
                    lua_env.execute(wrapped_post_execenv)
            else:
                with open(full_path, "r", encoding="utf-8") as f:
                    lua_env.execute(f.read())
        else:
            print(f"{file} not found!")

# Let WASEngine process updates
engine.start_main_loop(duration=3)

# Load Lua Files
load_wa_lua_files(lua_runtime)

# Simulate Addon Load Events
lua_globals.TriggerEvent("ADDON_LOADED", "WeakAuras")
lua_globals.TriggerEvent("PLAYER_LOGIN")