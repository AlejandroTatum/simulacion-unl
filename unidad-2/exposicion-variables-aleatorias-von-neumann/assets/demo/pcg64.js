/* PCG64 + SeedSequence, igual que numpy.random.default_rng(semilla).
   Reproduce en el navegador la misma secuencia de rng.uniform(0, 1) que el
   código Python de la exposición (codigo/beta22.py), sin red ni librerías.
   Uso: const rng = createNumpyRng(42); rng.uniform(); */
"use strict";
(function (root) {
  const M32 = 0xFFFFFFFF;
  const mul32 = (a, b) => Math.imul(a, b) >>> 0;

  // SeedSequence de numpy: mezcla la entropía en un pool de 4 palabras de 32 bits.
  function seedSequenceState(seed, words) {
    const INIT_A = 0x43b0d7e5, MULT_A = 0x931e8875, INIT_B = 0x8b51f9dd, MULT_B = 0x58f38ded;
    const MIX_L = 0xca01f9dd, MIX_R = 0x4973f715, XSHIFT = 16, POOL = 4;
    const entropy = [];
    let s = BigInt(seed);
    do { entropy.push(Number(s & 0xFFFFFFFFn)); s >>= 32n; } while (s > 0n);
    let hashConst = INIT_A;
    const hashmix = (value) => {
      value = (value ^ hashConst) >>> 0;
      hashConst = mul32(hashConst, MULT_A);
      value = mul32(value, hashConst);
      return (value ^ (value >>> XSHIFT)) >>> 0;
    };
    const mix = (x, y) => {
      let r = (mul32(MIX_L, x) - mul32(MIX_R, y)) >>> 0;
      return (r ^ (r >>> XSHIFT)) >>> 0;
    };
    const pool = [];
    for (let i = 0; i < POOL; i++) pool.push(hashmix(i < entropy.length ? entropy[i] : 0));
    for (let src = 0; src < POOL; src++)
      for (let dst = 0; dst < POOL; dst++)
        if (src !== dst) pool[dst] = mix(pool[dst], hashmix(pool[src]));
    for (let src = POOL; src < entropy.length; src++)
      for (let dst = 0; dst < POOL; dst++) pool[dst] = mix(pool[dst], hashmix(entropy[src]));
    let hashB = INIT_B;
    const out = [];
    for (let i = 0; i < words; i++) {
      let v = (pool[i % POOL] ^ hashB) >>> 0;
      hashB = mul32(hashB, MULT_B);
      v = mul32(v, hashB);
      out.push((v ^ (v >>> XSHIFT)) >>> 0);
    }
    return out;
  }

  const MASK64 = (1n << 64n) - 1n, MASK128 = (1n << 128n) - 1n;
  const MULT = 0x2360ED051FC65DA44385DF649FCCF645n;

  function createNumpyRng(seed) {
    const w = seedSequenceState(seed, 8);
    // generate_state(4, uint64): pares (bajo, alto) en little-endian.
    const u64 = [0, 2, 4, 6].map((i) => (BigInt(w[i + 1]) << 32n) | BigInt(w[i]));
    const initState = (u64[0] << 64n) | u64[1];
    const initSeq = (u64[2] << 64n) | u64[3];
    const inc = ((initSeq << 1n) | 1n) & MASK128;
    let state = 0n;
    const step = () => { state = (state * MULT + inc) & MASK128; };
    step(); state = (state + initState) & MASK128; step();
    function next64() {
      step();
      const x = ((state >> 64n) ^ state) & MASK64;
      const rot = Number(state >> 122n);
      return ((x >> BigInt(rot)) | (x << BigInt((64 - rot) & 63))) & MASK64;
    }
    // next_double de numpy: 53 bits altos / 2^53. uniform(0, 1) = 0 + 1 · next_double.
    return { uniform: () => Number(next64() >> 11n) / 9007199254740992 };
  }

  root.createNumpyRng = createNumpyRng;
  if (typeof module !== "undefined") module.exports = { createNumpyRng };
})(typeof window !== "undefined" ? window : globalThis);
