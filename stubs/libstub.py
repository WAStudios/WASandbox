# WAStudio/stubs/libstub.py

def inject_libstub(lua_runtime):
    lua_runtime.execute('''
-- Begin LibStub
local LIBSTUB_MAJOR, LIBSTUB_MINOR = "LibStub", 2
_G[LIBSTUB_MAJOR] = _G[LIBSTUB_MAJOR] or {}

local libstub = _G[LIBSTUB_MAJOR]

libstub.libs = libstub.libs or {}
libstub.minors = libstub.minors or {}

function libstub:NewLibrary(major, minor)
    assert(type(major) == "string", "Bad argument #2 to `NewLibrary` (string expected)")
    minor = assert(tonumber(minor), "Bad argument #3 to `NewLibrary` (number expected)")

    local oldminor = self.minors[major]
    if oldminor and oldminor >= minor then return nil end

    local lib = self.libs[major] or {}
    self.libs[major], self.minors[major] = lib, minor
    return lib, oldminor
end

function libstub:GetLibrary(major, silent)
    if not self.libs[major] and not silent then
        error(("Cannot find a library instance of %q."):format(tostring(major)), 2)
    end
    return self.libs[major], self.minors[major]
end

function libstub:IterateLibraries()
    return pairs(self.libs)
end

function libstub:IsNewVersion(minor)
    local oldminor = self.minors[LIBSTUB_MAJOR]
    return not oldminor or oldminor < minor
end

setmetatable(libstub, {
    __call = libstub.GetLibrary
})

-- Register LibStub itself
local stub = libstub:NewLibrary(LIBSTUB_MAJOR, LIBSTUB_MINOR)

if stub then
    for n, v in next, libstub do
        stub[n] = v
    end
end
-- End LibStub
''')
    print("LibStub injected.")