-- Isaac ER Bridge mod v0.1
-- A minimal Lua companion that writes Isaac pickup and room events to a local JSONL bridge log.

local bridgeConfig = {
    logPath = "C:/Games/IsaacERBridge/isaac_er_bridge.log",
    enabled = true,
    lastRoomIndex = nil,
    lastRoomClearState = false,
}

local function escape_json(value)
    if type(value) == "string" then
        value = string.gsub(value, "\\", "\\\\")
        value = string.gsub(value, "\"", '\\"')
        value = string.gsub(value, "\n", "\\n")
        value = string.gsub(value, "\r", "\\r")
        value = string.gsub(value, "\t", "\\t")
        return value
    end
    return tostring(value)
end

local function encode_json(data)
    if type(data) == "table" then
        local keys = {}
        for key in pairs(data) do
            table.insert(keys, key)
        end
        table.sort(keys)

        local parts = {}
        for _, key in ipairs(keys) do
            local value = data[key]
            table.insert(parts, string.format("\"%s\":%s", escape_json(key), encode_json(value)))
        end
        return "{" .. table.concat(parts, ",") .. "}"
    elseif type(data) == "string" then
        return string.format("\"%s\"", escape_json(data))
    elseif type(data) == "number" then
        return tostring(data)
    elseif type(data) == "boolean" then
        return data and "true" or "false"
    elseif data == nil then
        return "null"
    end
    return "\"\""
end

local function appendLog(eventType, payload)
    if not bridgeConfig.enabled then
        return
    end

    local timestamp = os.date("!%Y-%m-%dT%H:%M:%SZ")
    local line = string.format(
        "%s\n",
        encode_json({
            ts = timestamp,
            event = eventType,
            payload = payload,
        })
    )

    local file = io.open(bridgeConfig.logPath, "a")
    if file then
        file:write(line)
        file:close()
    end
end

local function getCurrentRoomIndex()
    local game = Game()
    if not game or not game:GetLevel then
        return 0
    end

    local level = game:GetLevel()
    if not level or not level.GetCurrentRoomIndex then
        return 0
    end

    return level:GetCurrentRoomIndex()
end

local function getPlayer()
    return Isaac.GetPlayer(0)
end

local function onGameStart()
    appendLog("bridge_start", {
        status = "online",
        mod = "isaac_er_bridge",
        version = "0.1",
    })
end

local function onPickup(pickup)
    if not pickup then
        return
    end

    local player = getPlayer()
    local roomIndex = getCurrentRoomIndex()
    local itemType = tostring(pickup.Type or pickup.Variant or "unknown")

    appendLog("pickup", {
        type = itemType,
        variant = tonumber(pickup.Variant) or 0,
        roomIndex = roomIndex,
        player = player and player:GetName() or "unknown",
    })
end

local function onRoomClear()
    local roomIndex = getCurrentRoomIndex()
    appendLog("room_clear", {
        roomIndex = roomIndex,
        status = "clear",
    })
end

local function onNewRoom()
    local roomIndex = getCurrentRoomIndex()
    appendLog("room_enter", {
        roomIndex = roomIndex,
        status = "entered",
    })
end

if RegisterMod then
    local mod = RegisterMod("isaac_er_bridge", 1)
    mod:AddCallback(ModCallbacks.MC_POST_GAME_STARTED, onGameStart)
    mod:AddCallback(ModCallbacks.MC_POST_PICKUP_UPDATE, onPickup)
    mod:AddCallback(ModCallbacks.MC_POST_NEW_ROOM, onNewRoom)
    mod:AddCallback(ModCallbacks.MC_POST_ROOM_CLEAR, onRoomClear)
end

print("[isaac_er_bridge] ready")
