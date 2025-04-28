# WAStudio/stubs/wow_api.py

def register_wow_stubs(lua_runtime):
    lua_runtime.execute("""
    WeakAuras = WeakAuras or {}
    function GetAddOnMetadata(addon, field)
        return "FakeMetaData"
    end
    function IsAddOnLoaded(addon)
        return true
    end
    """)
    print("Basic WoW API stubs injected.")
