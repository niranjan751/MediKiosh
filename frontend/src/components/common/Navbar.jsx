import { useState } from 'react'
import { ArrowRight, Heart, Menu, X } from 'lucide-react'

function Navbar() {
	const [isOpen, setIsOpen] = useState(false)
	const [activeLink, setActiveLink] = useState('Home')

	const selectLink = (label) => {
		setActiveLink(label)
		setIsOpen(false)
	}

	return (
		<header className="site-header">
			<nav className="navbar" aria-label="Main navigation">
				<a className="brand" href="#top" onClick={() => selectLink('Home')}>
					<span className="brand-mark" aria-hidden="true">
						<Heart size={21} strokeWidth={2.4} fill="currentColor" />
					</span>
					<strong>MediKiosk</strong>
				</a>

				<button
					className="menu-toggle"
					type="button"
					aria-expanded={isOpen}
					aria-controls="primary-navigation"
					aria-label={isOpen ? 'Close navigation menu' : 'Open navigation menu'}
					onClick={() => setIsOpen((open) => !open)}
				>
					{isOpen ? <X size={22} /> : <Menu size={22} />}
				</button>

				<div
					id="primary-navigation"
					className={`nav-content${isOpen ? ' is-open' : ''}`}
				>
					<div className="nav-links">
						<a className={activeLink === 'Home' ? 'is-active' : ''} href="#home" onClick={() => selectLink('Home')}>Home</a>
						<a className={activeLink === 'Features' ? 'is-active' : ''} href="#features" onClick={() => selectLink('Features')}>Features</a>
						<a className={activeLink === 'How It Works' ? 'is-active' : ''} href="#how-it-works" onClick={() => selectLink('How It Works')}>How It Works</a>
						<a className={activeLink === 'About' ? 'is-active' : ''} href="#about" onClick={() => selectLink('About')}>About</a>
						<a className={activeLink === 'Privacy' ? 'is-active' : ''} href="#privacy" onClick={() => selectLink('Privacy')}>Privacy</a>
					</div>
					<div className="nav-actions">
						<a className="login-link" href="#login" onClick={() => selectLink('Sign In')}>Sign In</a>
						<a className="nav-cta" href="#assessment" onClick={() => selectLink('Get Started')}>
							Get Started
							<ArrowRight size={17} aria-hidden="true" />
						</a>
					</div>
				</div>
			</nav>
		</header>
	)
}

export default Navbar
