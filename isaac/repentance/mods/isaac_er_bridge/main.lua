-- Isaac ER Bridge mod v0.1
-- Lightweight Lua scaffold for recording Isaac pickups and room states when the bridge is active.

local bridgeConfig = {
    logPath = "C:/Games/IsaacERBridge/isaac_er_bridge.log",
    enabled = true,
    lastRoomIndex = nil,
    lastRoomClearState = false,
}

local function appendLog(eventType, payload)
    if not bridgeConfig.enabled then
        return
    end

    local timestamp = os.date("!%Y-%m-%dT%H:%M:%SZ")
    local line = string.format(
        '{"ts":"%s","event":"%s","payload":%s}\n',
        timestamp,
        eventType,
        payload or '{}'
    )

    local file = io.open(bridgeConfig.logPath, "a")
    if file then
        file:write(line)
        file:close()
    end
end

local function normalizePickupName(pickup)
    if pickup == nil then
        return "unknown"
    end

    local pickupType = tostring(pickup.Type or pickup.type or "unknown")
    return pickupType
end

local function onPickup(pickup)
    local payload = string.format(
        '{"type":"%s","variant":%d,"roomIndex":%d}',
        normalizePickupName(pickup),
        pickup and pickup.Variant or 0,
        Game() and Game():GetLevel() and Game():GetLevel():GetCurrentRoomIndex() or 0
    )
    appendLog("pickup", payload)
end

local function onRoomClear()
    local roomIndex = Game() and Game():GetLevel() and Game():GetLevel():GetCurrentRoomIndex() or 0
    local payload = string.format('{"roomIndex":%d,"status":"clear"}', roomIndex)
    appendLog("room_clear", payload)
end

local function onGameStart()
    appendLog("bridge_start", '{"status":"online","mod":"isaac_er_bridge","version":"0.1"}')
end

-- Placeholder event hooks. These are intentionally lightweight because actual Isaac mod
-- event names vary by build and the roster of hook APIs. They are written to guide the
-- runtime implementation without coupling the design to a single mod loader version.

if RegisterMod then
    local mod = RegisterMod("isaac_er_bridge", 1)
    mod:AddCallback(ModCallbacks.MC_POST_GAME_STARTED, onGameStart)
    mod:AddCallback(ModCallbacks.MC_POST_PICKUP_UPDATE, onPickup)
    mod:AddCallback(ModCallbacks.MC_POST_ROOM_CLEAR, onRoomClear)
end

print("[isaac_er_bridge] ready")
