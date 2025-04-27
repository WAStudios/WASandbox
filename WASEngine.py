from wase_core.engine import WASEngine
import time

# Initialize WASEngine
engine = WASEngine()
lua = engine.lua.globals()

# --- TEST FRAMES ---
f = lua.CreateFrame("Frame", "TestFrame")
f.SetScript("OnEvent", lambda self, event, *args: print(f"[Event] {event}, args: {args}"))
lua.RegisterEvent("PLAYER_ENTERING_WORLD", f)
lua.TriggerEvent("PLAYER_ENTERING_WORLD")

# --- TEST UNIT ---
print("Is player in combat?", lua.UnitAffectingCombat("player"))
lua.EnterCombatForUnit("player")
print("Is player in combat?", lua.UnitAffectingCombat("player"))
lua.ExitCombatForUnit("player")

# --- TEST SPELL INFO ---
print("GetSpellInfo(133):", lua.GetSpellInfo(133))
lua.LearnSpell(133)
print("IsSpellKnown(133):", lua.IsSpellKnown(133))
lua.SetSpellCooldown(133, 2)
print("GetSpellCooldown(133):", lua.GetSpellCooldown(133))

# --- TEST CVARS ---
lua.SetCVar("nameplateShowEnemies", "1")
print("GetCVarBool(nameplateShowEnemies):", lua.GetCVarBool("nameplateShowEnemies"))

# --- TEST ACTION BAR ---
lua.SetAction(1, "spell", 133, "Spell_Fire_FlameBolt")
print("GetActionInfo(1):", lua.GetActionInfo(1))
lua.UseAction(1)
print("GetActionCooldown(1):", lua.GetActionCooldown(1))

# --- TEST MACROS ---
lua.set_slash("HELLO", 1, "/hello")
lua.set_slash_handler("HELLO", lambda msg: print("Slash executed with:", msg))
lua.RunMacroText("/hello world")

# --- TEST INVENTORY ---
lua.EquipItem(1, 12345, "Mighty Helmet", "INV_Helmet_03")
print("GetInventoryItemTexture('player', 1):", lua.GetInventoryItemTexture("player", 1))

# --- TEST COMBAT LOG ---
lua.RegisterCombatLogListener(lambda data: print("[CombatLog]", data))
lua.SimulateAttack("player", "target", 133, "Fireball", 1000)

# --- TEST MAP/ZONES ---
lua.SetZone("Stormwind", "Trade District")
print("GetZoneText():", lua.GetZoneText())

# --- TEST TIMERS / UPDATES ---
update_frame = lua.CreateFrame("Frame", "UpdateFrame")
update_frame.SetScript("OnUpdate", lambda self, elapsed: print(f"[OnUpdate] Elapsed: {elapsed:.3f}") or lua.RemoveUpdateFrame(self))
lua.AddUpdateFrame(update_frame)
lua.StartUpdateThread()

# --- WAIT FOR ASYNC ---
time.sleep(0.5)

print("\n--- FINAL TEST COMPLETE ---")