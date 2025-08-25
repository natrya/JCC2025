import React, { useMemo, useState } from 'react'
import { VALIDATORS, runAllValidators } from './validators.js'

export default function App() {
  const [input, setInput] = useState('')
  const results = useMemo(() => runAllValidators(input), [input])

  const allPass = results.every(r => r.pass)

  return (
    <div className="container">
      <div className="card">
        <div className="header">
          <div className="hgroup">
            <h1>Flag Validator</h1>
            <p>At least you tried</p>
          </div>
          <span className="badge">Ez Pz Lemon Squeezy</span>
        </div>

        <div className="grid">
          <div className="panel">
            <div className="kv">
              <div>
                <strong>Input your candidate</strong>
                <div className="hint">Hint: IDK Just Reverse the Flow</div>
              </div>
              <div>
                <span className="badge" aria-live="polite">{allPass ? 'All checks passed' : 'Not valid yet'}</span>
              </div>
            </div>

            <textarea
              placeholder="Type your flag candidate here (no flag{ } wrapper)"
              value={input}
              onChange={e => setInput(e.target.value)}
              spellCheck={false}
              autoCapitalize="off"
              autoCorrect="off"
            />

            <div className="controls">
              <button className="primary" onClick={() => navigator.clipboard.writeText(input)}>Copy</button>
              <button className="secondary" onClick={() => setInput('')}>Reset</button>
            </div>
          </div>

        </div>
      </div>
    </div>
  )
}
