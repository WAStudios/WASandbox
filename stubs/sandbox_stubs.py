# stubs/sandbox_stubs.py

import random

def inject_sandbox_stubs(lua_runtime):
    lua_runtime.execute("""
    -- WeakAuras + Private globals
    _G.WeakAuras = _G.WeakAuras or {}
    WeakAuras = _G.WeakAuras
    WeakAuras.Private = WeakAuras.Private or {}    
    _G.Private = WeakAuras.Private
    
    WeakAuras.callbacks = WeakAuras.callbacks or {}
    WeakAuras.callbacks.RegisterCallback = function(self, event, handler)
        print("Stubbed WeakAuras.callbacks:RegisterCallback called for event:", event)
    end
    WeakAuras.Private.callbacks = WeakAuras.Private.callbacks or WeakAuras.callbacks
    Private.callbacks = WeakAuras.Private.callbacks
    
    WeakAuras.L = WeakAuras.L or {}
    WeakAuras.ExecEnv = WeakAuras.ExecEnv or {}
    WeakAuras.Private.ExecEnv = WeakAuras.Private.ExecEnv or WeakAuras.ExecEnv
    WeakAuras.frames = WeakAuras.frames or {}
    Private.ExecEnv = WeakAuras.Private.ExecEnv
    _G.StaticPopupDialogs = _G.StaticPopupDialogs or {}
    StaticPopupDialogs = _G.StaticPopupDialogs
    _G.GetScreenWidth = function() return 1920 end
    _G.GetScreenHeight = function() return 1080 end


    math = math or {}
    math.min = math.min or function(a, b) if a < b then return a else return b end end
    math.max = math.max or function(a, b) if a > b then return a else return b end end
    math.floor = math.floor or function(x) return x - (x % 1) end
    math.ceil = math.ceil or function(x) if x % 1 == 0 then return x else return x - (x % 1) + 1 end end
    math.abs = math.abs or function(x) if x < 0 then return -x else return x end end
    _G.math = math

    -- select(2, ...) environment simulation
    select = function(index, ...)
        if index == 2 then
            return WeakAuras.Private
        end
        return nil
    end

    -- C_AddOns stub
    _G.C_AddOns = _G.C_AddOns or {}
    C_AddOns = _G.C_AddOns
    C_AddOns.IsAddOnLoaded = function(name)
        print("Stubbed IsAddOnLoaded check for:", name)
        return false -- Force fallback logic for optional addons like CustomNames
    end
    C_AddOns.LoadAddOn = function(name) return true end
    C_AddOns.GetAddOnMetadata = function(addon, field)
        if field == "Version" then
            return "Dev"
        elseif field == "X-Flavor" then
            return "Mainline"
        end
        return nil
    end

    -- getfenv stub (simplified for most addons)
    _G.getfenv = function(f)
        return _G
    end
    getfenv = _G.getfenv

    -- Force Mainline flavor (Retail)
    _G.flavor = 10

    -- WeakAuras flavor detection stubs
    WeakAuras.BuildInfo = 110000
    WeakAuras.IsRetail = function() return true end
    WeakAuras.IsClassicEra = function() return false end
    WeakAuras.IsCataClassic = function() return false end
    WeakAuras.IsClassicOrCata = function() return false end
    WeakAuras.IsCataOrRetail = function() return true end
    WeakAuras.IsTWW = function() return true end

    if not _G.IsRetail then
        local isRetailFunc = function() return true end
        _G.IsRetail = isRetailFunc
        IsRetail = isRetailFunc
    end

    -- SlashCmdList stub
    _G.SlashCmdList = _G.SlashCmdList or {}
    SlashCmdList = _G.SlashCmdList

    -- WeakAuras misc stubs
    WeakAuras.IsLibsOK = function() return true end
    WeakAuras.prettyPrint = function(msg) print("[WA]", msg) end
    WeakAuras.versionString = "WAStudioSim"

    -- WeakAuras.RegisterSubRegionType stub
    WeakAuras.RegisterSubRegionType = function(name, data)
        print("Registered SubRegionType:", name)
    end

    WeakAuras.RegisterRegionType = function(name, createFunc, modifyFunc, default, getPropsFunc, validateFunc)
        print("Stubbed WeakAuras.RegisterRegionType called for:", name)
        return true
    end

    Private.RegisterRegionType = WeakAuras.RegisterRegionType

    -- Stub AddProgressSourceToDefault
    WeakAuras.AddProgressSourceToDefault = function(...) 
        print("Stub: AddProgressSourceToDefault called", ...)
    end

    WeakAuras.regionPrototype = WeakAuras.regionPrototype or {}
    WeakAuras.regionPrototype.AddProgressSourceToDefault = function(default)
        print("Stubbed AddProgressSourceToDefault called")
    end
    WeakAuras.regionPrototype.AddAlphaToDefault = function(default)
        print("Stubbed AddAlphaToDefault called")
    end
    WeakAuras.regionPrototype.AddProperties = function(properties, default)
        print("Stubbed AddProperties called")
    end

    Private.regionPrototype = Private.regionPrototype or {}
    Private.regionPrototype.AddProgressSourceToDefault = function(default)
        print("Stubbed Private.AddProgressSourceToDefault called")
    end
    Private.regionPrototype.AddAlphaToDefault = function(default)
        print("Stubbed Private.AddAlphaToDefault called")
    end
    Private.regionPrototype.AddProperties = function(properties, default)
        print("Stubbed Private.AddProperties called")
    end

    UnitLevel = function(unit) return 80 end

    -- LDB (LibDataBroker) simulation
    _G.LDB = {
        NewDataObject = function(name, tbl)
            return tbl
        end
    }

    -- Global localization fallback stub
    _G.L = _G.L or setmetatable({}, {
        __index = function(_, key)
            return key
        end
    })

    -- Simulate LibCustomGlow-1.0
    _G.LibStub:NewLibrary("LibCustomGlow-1.0", 1)
    _G.LibStub.libs["LibCustomGlow-1.0"] = {
        -- Add mocked functions if needed, or leave as a basic table
        -- Example mock:
        PixelGlow_Start = function(...) end,
        PixelGlow_Stop = function(...) end,
    }

    -- LibDBIcon-1.0 stub
    _G.LibStub:NewLibrary("LibDBIcon-1.0", 1)
    _G.LibStub.libs["LibDBIcon-1.0"] = {
        Register = function(...) end,
        Hide = function(...) end,
        Show = function(...) end,
        IsRegistered = function(...) return false end,
        Unregister = function(...) end,
    }

    -- LibRangeCheck-3.0 stub
    _G.LibStub:NewLibrary("LibRangeCheck-3.0", 1)
    _G.LibStub.libs["LibRangeCheck-3.0"] = {
        GetRange = function(...) return 5, 40 end,
        IsInRange = function(...) return true end,
    }

    -- LibDeflate stub
    _G.LibStub:NewLibrary("LibDeflate", 1)
    _G.LibStub.libs["LibDeflate"] = {
        CompressDeflate = function(data, level) return data end,
        CompressZlib = function(data, level) return data end,
        CompressGzip = function(data, level) return data end,
        CompressDeflateBase64 = function(data) return data end,
        DecompressDeflate = function(data) return data, true end,
        DecompressDeflateBase64 = function(data) return data, true end,
        CompressTable = function(tbl) return tbl end,
        DecompressTable = function(tbl) return tbl end,
    }

    -- LibSerialize stub
    _G.LibStub:NewLibrary("LibSerialize", 1)
    _G.LibStub.libs["LibSerialize"] = {
        Serialize = function(...) return "serialized" end,
        Deserialize = function(str) return true, "deserialized" end,
    }

    -- LibCompress stub
    _G.LibStub:NewLibrary("LibCompress", 1)
    _G.LibStub.libs["LibCompress"] = {
        Compress = function(data) return data end,
        Decompress = function(data) return data end,
        CompressHuffman = function(data) return data end,
        DecompressHuffman = function(data) return data end,
    }

    -- LibSharedMedia-3.0 stub
    _G.LibStub:NewLibrary("LibSharedMedia-3.0", 1)
    _G.LibStub.libs["LibSharedMedia-3.0"] = {
        Register = function(...) end,
        Fetch = function(...) return "MockedMediaPath" end,
    }

    -- LibDataBroker-1.1 stub (for completeness)
    _G.LibStub:NewLibrary("LibDataBroker-1.1", 1)
    _G.LibStub.libs["LibDataBroker-1.1"] = {
        NewDataObject = function(name, obj) return obj end,
    }

    -- AceComm-3.0 stub
    _G.LibStub:NewLibrary("AceComm-3.0", 1)
    _G.LibStub.libs["AceComm-3.0"] = {
        RegisterComm = function(...) end,
        SendCommMessage = function(...) end,
    }

    -- AceSerializer-3.0 stub
    _G.LibStub:NewLibrary("AceSerializer-3.0", 1)
    _G.LibStub.libs["AceSerializer-3.0"] = {
        Serialize = function(...) return "serialized" end,
        Deserialize = function(str) return true, "deserialized" end,
    }

    -- LibGetFrame-1.0 stub
    _G.LibStub:NewLibrary("LibGetFrame-1.0", 1)
    _G.LibStub.libs["LibGetFrame-1.0"] = {
        GetFrame = function(...) return {} end,
    }

    _G.LGF = {
        GetFrame = function(...) return {} end,
    }

    WeakAuras.ExecEnv = WeakAuras.ExecEnv or {}
    _G.ExecEnv = WeakAuras.ExecEnv

    _G.RegisterCallback = function(...) print("Stubbed RegisterCallback", ...) end
    WeakAuras.RegisterCallback = _G.RegisterCallback

    """)

    # Python -> Lua random integration
    def lua_random(*args):
        if len(args) == 0:
            return random.random()
        elif len(args) == 1:
            return random.randint(1, args[0])
        elif len(args) == 2:
            return random.randint(args[0], args[1])
        else:
            raise ValueError("random() accepts 0, 1, or 2 arguments in Lua")

    lua_runtime.globals()['random'] = lua_random
    lua_runtime.globals()['math']['random'] = lua_random
    lua_runtime.globals()['math']['randomseed'] = random.seed
