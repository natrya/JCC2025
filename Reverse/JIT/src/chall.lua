local pure_lua_bit = {}
do
    local max_bits = 31 
    local powers_of_2 = {}
    for i = 0, max_bits do powers_of_2[i] = 2^i end
    function pure_lua_bit.bxor(a, b)
        local res = 0
        for i = 0, max_bits do
            if (math.floor(a / powers_of_2[i]) % 2) ~= (math.floor(b / powers_of_2[i]) % 2) then
                res = res + powers_of_2[i]
            end
        end
        return res
    end
end

local bignum = (function()
    local bxor = pure_lua_bit.bxor
    local BASE = 2^24
    local MASK = BASE - 1

    local bn = {} 
    bn.__index = bn
    local bignum_module = {}

    local function copy(A)
        local B = {n=A.n, sign=A.sign}
        for i=1, A.n do B[i] = A[i] end
        return setmetatable(B, bn)
    end
  
    local function trim(A)
        while A.n > 1 and A[A.n] == 0 do A.n = A.n - 1 end
        if A.n==1 and A[1]==0 then A.sign = 1 end
        return A
    end
    
    local constructor

    local function add(A, B)
        if A.sign ~= B.sign then
            if A.sign == 1 then return bn.sub(A, -B) else return bn.sub(B, -A) end
        end
        local C = {sign = A.sign, n=math.max(A.n, B.n)}
        local carry = 0
        for i=1, C.n do
            local s = (A[i] or 0) + (B[i] or 0) + carry
            C[i] = s % BASE
            carry = math.floor(s / BASE)
        end
        if carry > 0 then C.n = C.n + 1; C[C.n] = carry end
        return setmetatable(C, bn)
    end

    local function cmp_abs(A, B)
        if A.n > B.n then return 1 end; if A.n < B.n then return -1 end
        for i = A.n, 1, -1 do
            if A[i] > B[i] then return 1 end; if A[i] < B[i] then return -1 end
        end
        return 0
    end
    
    local function sub(A, B)
        if A.sign ~= B.sign then
            if A.sign == 1 then return add(A, -B) else return -add(-A, B) end
        end
        if cmp_abs(A, B) == -1 then local C = sub(B, A); C.sign = -A.sign; return C end
        local C = {sign = A.sign, n = A.n}
        local borrow = 0
        for i=1, A.n do
            local d = (A[i] or 0) - (B[i] or 0) - borrow
            if d < 0 then d = d + BASE; borrow = 1 else borrow = 0 end
            C[i] = d
        end
        return trim(setmetatable(C, bn))
    end

    local function mul_s(A, s)
        local C = {sign=A.sign, n=A.n}
        local carry = 0
        for i = 1, A.n do
            local prod = (A[i] or 0) * s + carry
            C[i] = prod % BASE
            carry = math.floor(prod / BASE)
        end
        while carry > 0 do
            C.n = C.n + 1
            C[C.n] = carry % BASE
            carry = math.floor(carry / BASE)
        end
        return trim(setmetatable(C, bn))
    end

    local function mul(A, B)
        local final_sign = A.sign * B.sign
        A, B = bn.abs(A), bn.abs(B)
        
        local C = bignum_module.zero
        for i = 1, B.n do
            local term = mul_s(A, B[i])
            if term:iszero() then goto continue end
            
            local shifted_term = {n = term.n + i - 1, sign = term.sign}
            for j=1, i-1 do shifted_term[j] = 0 end
            for j=1, term.n do shifted_term[i+j-1] = term[j] end
            
            C = add(C, setmetatable(shifted_term, bn))
            ::continue::
        end
        C.sign = final_sign
        return trim(C)
    end
    
    bn.new = function(num_s, base)
        local A = {n=1, sign=1, [1]=0}
        setmetatable(A, bn)
        
        if type(num_s)=='number' then
            if num_s < 0 then A.sign = -1; num_s = -num_s end
            if num_s == 0 then return bignum_module.zero end
            local i = 1
            while num_s > 0 do
                A[i] = num_s % BASE
                num_s = math.floor(num_s/BASE)
                i = i+1
            end
            A.n = i - 1
            return trim(A)
        end
        
        num_s = tostring(num_s):gsub("%s","")
        if num_s:match('^%-') then A.sign = -1; num_s = num_s:sub(2) end
        
        base = base or 10
        
        if base == 16 then
            local hex_map = { a=10, b=11, c=12, d=13, e=14, f=15 }
            local b16 = constructor(16)
            for i=1, #num_s do
                local char = num_s:sub(i,i):lower()
                local val = tonumber(char) or hex_map[char]
                if not val then error("Invalid hex character: " .. char) end
                A = add(mul_s(A, 16), constructor(val))
            end
        else
            local log_conv = 7
            for i=1, #num_s, log_conv do
                local part_s = num_s:sub(i, i+log_conv-1)
                A = add(mul_s(A, 10^#part_s), constructor(tonumber(part_s)))
            end
        end

        if A:iszero() then A.sign = 1 end
        return A
    end
    
    constructor = function(x)
        if type(x) == 'table' and getmetatable(x) == bn then return x end
        if x == nil then return bignum_module.zero end
        return bn.new(x)
    end

    bn.iszero = function(self) return self.n==1 and self[1] == 0 end
    bignum_module.zero = {n=1, sign=1, [1]=0}; setmetatable(bignum_module.zero, bn)
    bignum_module.one = {n=1, sign=1, [1]=1}; setmetatable(bignum_module.one, bn)

    bn.abs = function(A) local B=copy(A); B.sign = 1; return B end
    bn.__add = function(a, b) return add(constructor(a), constructor(b)) end
    bn.__sub = function(a, b) return sub(constructor(a), constructor(b)) end
    bn.__mul = function(a, b) return mul(constructor(a), constructor(b)) end
    bn.__unm = function(A) local B=copy(A); B.sign = -B.sign; return B end

    bn.tohex = function(self)
        if self:iszero() then return "0" end
        local s, hex_chars = "", "0123456789abcdef"
        local A = bn.abs(self)
        local rem_tbl = {n=1, sign=1, [1]=0}
        setmetatable(rem_tbl, bn)

        while not A:iszero() do
            local rem = 0; local carry = 0
            for i = A.n, 1, -1 do
                local val = A[i] + carry * BASE
                A[i] = math.floor(val / 16)
                carry = val % 16
            end
            A = trim(A)
            s = hex_chars:sub(carry + 1, carry + 1) .. s
        end
        return (self.sign < 0 and "-" or "") .. s
    end
    
    bn.bxor = function(A, B)
      local C = {sign=1, n=math.max(A.n, B.n)}
      for i=1, C.n do C[i] = bxor(A[i] or 0, B[i] or 0) end
      return trim(setmetatable(C, bn))
    end
    
    setmetatable(bignum_module, { __call = function(self, ...) return constructor(...) end })
    bignum_module.fromhex = function(s) return bn.new(s, 16) end
    
    return bignum_module
end)()

function encrypt_as_bigint_to_hex(plaintext, key_str)
    if not plaintext or #plaintext == 0 then return "" end

    local pt_hex = ""
    for i = 1, #plaintext do
        pt_hex = pt_hex .. string.format("%02x", string.byte(plaintext, i))
    end

    local pt_bigint = bignum.fromhex(pt_hex)
    local key_bigint = bignum(key_str)
    local encrypted_bigint = pt_bigint:bxor(key_bigint)
    return encrypted_bigint:tohex()
end

local key = "37281856372975529869235043339326658186617449372818563760068146687874218416451296882367786923504"
local flag = 'JCC25{8b1dc37ae25e134daf09800b11e3b024}'

local enc_hex = encrypt_as_bigint_to_hex(flag, key)

print("Key (Decimal): " .. key)
print("Flag: " .. flag)
print("Encrypted (Hex): " .. enc_hex)
