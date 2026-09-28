export default function LoginForm() {
  return (
    <form style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      <div>
        <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>Email</label>
        <input type="email" placeholder="Enter your email" style={{ width: '100%', padding: '12px', border: '1px solid #e2e8f0', borderRadius: '8px' }} />
      </div>
      <div>
        <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>Password</label>
        <input type="password" placeholder="Enter your password" style={{ width: '100%', padding: '12px', border: '1px solid #e2e8f0', borderRadius: '8px' }} />
      </div>
      <button type="submit" style={{ padding: '12px', backgroundColor: '#3b82f6', color: 'white', border: 'none', borderRadius: '8px', fontWeight: 'bold', cursor: 'pointer' }}>Login</button>
    </form>
  )
}
