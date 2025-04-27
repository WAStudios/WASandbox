# WAStudio/stubs/weak_auras_private.py

def inject_weak_auras_private(lua_runtime):
    lua_runtime.execute("""
    WeakAuras = WeakAuras or {}
    WeakAuras.Private = WeakAuras.Private or {}
    local Private = WeakAuras.Private  -- << This makes 'local Private' available globally in all files

    Private.options = Private.options or {}
    Private.glow = Private.glow or {}
    Private.regionPrototype = Private.regionPrototype or {}
    Private.cooldownFrame = Private.cooldownFrame or {}
    """)
    print("WeakAuras.Private with common fields (and global) injected.")
