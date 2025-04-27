def inject_addon_env(lua_runtime):
    lua_runtime.execute("""
    select = function(index, ...)
        if index == 2 then
            return WeakAuras.Private
        end
        return nil
    end
    """)
    print("Addon select(2, ...) environment injected.")
