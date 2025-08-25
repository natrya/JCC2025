// Validation logic for the reverse engineering CTF

// The target phrase (unknown to players) is validated by obfuscated checks.
// We avoid storing the flag plainly; instead we store derived constants.

function toCodes(str) {
	const arr = []
	for (let i = 0; i < str.length; i++) arr.push(str.charCodeAt(i))
	return arr
}

function fromCodes(arr) {
	return String.fromCharCode(...arr)
}

function xorAll(arr) {
	return arr.reduce((acc, v) => acc ^ v, 0)
}

function sumAll(arr) {
	return arr.reduce((acc, v) => acc + v, 0)
}

function chunk(str, size) {
	const out = []
	for (let i = 0; i < str.length; i += size) out.push(str.slice(i, i + size))
	return out
}

// Precomputed constants derived from the real flag through reversible transforms
// Chunks: [0..5], [6..11], [12..17], [18..23], [24..25]
const MASK0 = [5, 7, 9, 11, 13, 15]
const TARGET0 = [87, 52, 61, 104, 121, 80] // codes[0..5] XOR MASK0

const MASK1 = [17, 23, 5, 31, 7, 11]
const TARGET1 = [127, 75, 89, 80, 125, 62] // (codes[6..11] + MASK1) & 0x7F

const MASK2 = [9, 4, 12, 1, 3, 7]
const TARGET2 = [86, 110, 39, 117, 98, 107] // (codes[12..17] - MASK2) & 0x7F

const MASK3 = [13, 26, 39, 52, 65, 78]
const TARGET3 = [126, 41, 120, 92, 32, 60] // codes[18..23] XOR MASK3

const MASK4_CONST = 0x2A
const TARGET4 = [117, 28] // (codes[24..25] ^ 0x2A) + 7

const TOTAL_SUM = 2259 // sum of all char codes
const TOTAL_XOR = 7 // xor of all char codes
const LENGTH = 26
const UNDERSCORE_POS = [5, 12, 20] // 0-based
const UPPERCASE_COUNT = 3

const WEIGHTED_MOD97 = [43, 6, 3, 50, 0] // per-chunk sum((i+1)*code) % 97

function getCodesSlice(input, start, end) {
	return toCodes(input.slice(start, end))
}

function checkChunk0(input) {
	const c = getCodesSlice(input, 0, 6)
	if (c.length !== 6) return false
	for (let i = 0; i < 6; i++) {
		if ((c[i] ^ MASK0[i]) !== TARGET0[i]) return false
	}
	return true
}

function checkChunk1(input) {
	const c = getCodesSlice(input, 6, 12)
	if (c.length !== 6) return false
	for (let i = 0; i < 6; i++) {
		if (((c[i] + MASK1[i]) & 0x7F) !== TARGET1[i]) return false
	}
	return true
}

function checkChunk2(input) {
	const c = getCodesSlice(input, 12, 18)
	if (c.length !== 6) return false
	for (let i = 0; i < 6; i++) {
		if (((c[i] - MASK2[i]) & 0x7F) !== TARGET2[i]) return false
	}
	return true
}

function checkChunk3(input) {
	const c = getCodesSlice(input, 18, 24)
	if (c.length !== 6) return false
	for (let i = 0; i < 6; i++) {
		if ((c[i] ^ MASK3[i]) !== TARGET3[i]) return false
	}
	return true
}

function checkChunk4(input) {
	const c = getCodesSlice(input, 24, 26)
	if (c.length !== 2) return false
	for (let i = 0; i < 2; i++) {
		if ((((c[i] ^ MASK4_CONST) + 7) & 0x7F) !== TARGET4[i]) return false
	}
	return true
}

function checkLength(input) {
	return input.length === LENGTH
}

function checkUnderscores(input) {
	if (input.length < LENGTH) return false
	return UNDERSCORE_POS.every(pos => input[pos] === '_')
}

function checkLastUpperCounts(input) {
	if (input.length < LENGTH) return false
	const last = input[input.length - 1]
	const uc = [...input].filter(ch => ch >= 'A' && ch <= 'Z').length
	return last === '?' && uc === UPPERCASE_COUNT
}

function checkTotals(input) {
	const codes = toCodes(input)
	return sumAll(codes) === TOTAL_SUM && xorAll(codes) === TOTAL_XOR
}

function checkWeightedMods(input) {
	if (input.length !== LENGTH) return false
	const chunks = [
		getCodesSlice(input, 0, 6),
		getCodesSlice(input, 6, 12),
		getCodesSlice(input, 12, 18),
		getCodesSlice(input, 18, 24),
		getCodesSlice(input, 24, 26),
	]
	if (chunks.some(c => c.length === 0)) return false
	for (let ci = 0; ci < chunks.length; ci++) {
		const c = chunks[ci]
		let s = 0
		for (let i = 0; i < c.length; i++) s += (i + 1) * c[i]
		if (s % 97 !== WEIGHTED_MOD97[ci]) return false
	}
	return true
}

function checkDigitCounts(input) {
	const counts = { '0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0 }
	for (const ch of input) if (counts.hasOwnProperty(ch)) counts[ch]++
	return counts['3'] === 4 && counts['4'] === 2 && counts['1'] === 1
}

function checkReversePrefix(input) {
	if (input.length < 5) return false
	const pref = input.slice(0, 5)
	return pref.split('').reverse().join('') === 'tc43R'
}

export const VALIDATORS = [
	{ name: 'Length must match', hint: 'Exact number of characters', check: checkLength },
	{ name: 'Underscores in place', hint: 'Positions matter (0-index: 5,12,20)', check: checkUnderscores },
	{ name: 'Ending and uppercase', hint: 'Ends with a symbol, few caps', check: checkLastUpperCounts },
	{ name: 'Totals: sum & xor', hint: 'Aggregate constraints', check: checkTotals },
	{ name: 'Chunk#0 transform', hint: 'XOR mask on first 6', check: checkChunk0 },
	{ name: 'Chunk#1 transform', hint: 'Add-and-wrap on next 6', check: checkChunk1 },
	{ name: 'Chunk#2 transform', hint: 'Subtract-and-wrap on next 6', check: checkChunk2 },
	{ name: 'Chunk#3 transform', hint: 'XOR with stepped mask', check: checkChunk3 },
	{ name: 'Chunk#4 transform', hint: 'Small tail tweak', check: checkChunk4 },
	{ name: 'Weighted mod checks', hint: 'Per-chunk rolling weights', check: checkWeightedMods },
	{ name: 'Digit frequencies', hint: 'How many 3, 4, and 1?', check: checkDigitCounts },
	{ name: 'Reverse prefix', hint: 'First five reversed equals tc43R', check: checkReversePrefix },
]

export function runAllValidators(input) {
	return VALIDATORS.map(v => ({ pass: !!v.check(input) }))
}
