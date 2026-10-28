import { useState } from 'react'
import { api } from '../api'
import {useNavigate} from 'react-router-dom'

function BrandMark({ small = false }) {
  return (
    <div className="flex items-center gap-3">
      <div className={`grid place-items-center rounded-xl bg-blue-600 shadow-sm shadow-blue-200 ${small ? 'h-9 w-9' : 'h-11 w-11'}`}>
        <svg viewBox="0 0 24 24" className="h-6 w-6 text-white" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
          <path d="M3.5 20V10.5L12 4l8.5 6.5V20" strokeLinecap="round" strokeLinejoin="round" />
          <path d="M7.5 20v-7h9v7M9.5 13v7M14.5 13v7M3.5 20h17" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </div>
      {!small && <span className="text-2xl font-bold tracking-tight text-white">ReplyHome</span>}
    </div>
  )
}

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [rememberMe, setRememberMe] = useState(true)
  const navigate = useNavigate()


  async function handleSubmit(event) {
    event.preventDefault()
    setError('')
    try {
      const data = await api('/auth/login', {
        method: 'POST',
        body: JSON.stringify({email, password}),
      })
      localStorage.setItem('token', data.token)
      navigate('/dashboard')
    } catch (err) {
      setError(err.message)
    }

  }

  return (
    <main className="min-h-screen bg-[#f5f7fa] text-slate-900 lg:grid lg:grid-cols-[1.12fr_0.88fr]">
      <section className="relative hidden overflow-hidden bg-slate-900 lg:block ">
        <img
          src="https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1600&q=85"
          alt="Modern luxury home with a pool"
          className="absolute inset-0 h-full w-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-black/80" />
        <div className="relative flex h-full flex-col justify-between p-12 xl:p-16">
          <BrandMark />
          <div className="max-w-xl">
            <p className="mb-4 text-sm font-semibold uppercase tracking-[0.18em] text-blue-200 ">LISTINGS. LEADS. FOLLOW-UPS.</p>
            <h1 className="text-4xl font-semibold leading-tight text-white xl:text-5xl">Welcome back to a smarter way of managing real estate.</h1>
          </div>
        </div>
      </section>

      <section className="flex min-h-screen flex-col px-6 py-7 sm:px-10 lg:px-12 xl:px-16">
        <div className="lg:hidden"><BrandMark small /></div>

        <div className="flex flex-1 items-center justify-center py-12 lg:py-0">
          <div className="w-full max-w-md">
            <div className="mb-9">
              <p className="mb-3 text-sm font-semibold text-blue-600 lg:hidden">Haven</p>
              <h2 className="text-3xl font-bold tracking-tight text-slate-950">Log in to your account</h2>
              <p className="mt-2 text-[15px] text-slate-500">Enter your details to access your property workspace.</p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-5">
              <div>
                <h2> {error && <p className='text-sm text-red-600'> {error} </p>} </h2>
                <label htmlFor="email" className="mb-2 block text-sm font-semibold text-slate-700">Email address</label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  onChange={(e) =>   setEmail(e.target.value)}
                  autoComplete="email"
                  placeholder="name@company.com"
                  value={email}
                  className="h-12 w-full rounded-lg border border-slate-200 bg-white px-4 text-[15px] text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                />
              </div>

              <div>
                <div className="mb-2 flex items-center justify-between">
                  <label htmlFor="password" className="text-sm font-semibold text-slate-700">Password</label>
                  <a href="#" className="text-sm font-semibold text-blue-600 hover:text-blue-700">Forgot password?</a>
                </div>
                <div className="relative">
                  <input
                    id="password"
                    name="password"
                    type={showPassword ? 'text' : 'password'}
                    autoComplete="current-password"
                    placeholder="Enter your password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="h-12 w-full rounded-lg border border-slate-200 bg-white px-4 pr-12 text-[15px] text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword((visible) => !visible)}
                    className="absolute right-3 top-1/2 grid h-8 w-8 -translate-y-1/2 place-items-center rounded-md text-slate-400 hover:bg-slate-100 hover:text-slate-600"
                    aria-label={showPassword ? 'Hide password' : 'Show password'}
                  >
                    <svg viewBox="0 0 24 24" className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
                      <path d="M2.5 12s3.5-6 9.5-6 9.5 6 9.5 6-3.5 6-9.5 6-9.5-6-9.5-6Z" strokeLinecap="round" strokeLinejoin="round" />
                      <circle cx="12" cy="12" r="2.5" />
                    </svg>
                  </button>
                </div>
              </div>

              <button
                type="submit"
                className="h-12 w-full rounded-lg bg-blue-600 text-sm font-semibold text-white shadow-sm shadow-blue-200 transition hover:bg-blue-700 focus:outline-none focus:ring-4 focus:ring-blue-200 active:bg-blue-800"
              >
                Sign in
              </button>
            </form>

            <p className="mt-7 text-center text-sm text-slate-500">
              New to Haven?{' '}
              <a href="#" className="font-semibold text-blue-600 hover:text-blue-700">Create an agency account</a>
            </p>

            <div className="mt-10 flex items-center justify-center gap-2 text-xs text-slate-400">
              <svg viewBox="0 0 24 24" className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
                <rect x="5" y="10" width="14" height="10" rx="2" />
                <path d="M8 10V7a4 4 0 0 1 8 0v3" />
              </svg>
              Secure, encrypted access
            </div>
          </div>
        </div>
      </section>
    </main>
  )
}
