# WAStudio/stubs/wow_api.py

def inject_wow_api(lua_runtime):
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
