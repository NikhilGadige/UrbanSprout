import { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import {
  Menu, X, LogOut, History as HistoryIcon, Globe, ChevronDown,
  Sprout, Wrench, Leaf, MessageCircle, BookOpen, Users, Calendar, KeyRound,
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { useApiKey } from '../context/ApiKeyContext';

const TOOLS = [
  { key: 'calendar', path: '/calendar', icon: Calendar },
  { key: 'companion', path: '/companion', icon: Users },
  { key: 'guides', path: '/guides', icon: BookOpen },
  { key: 'chat', path: '/chat', icon: MessageCircle },
];

export default function Navbar() {
  const { user, logout } = useAuth();
  const { language, setLanguage, t, languages } = useLanguage();
  const { hasKey } = useApiKey();
  const location = useLocation();
  const navigate = useNavigate();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [profileOpen, setProfileOpen] = useState(false);
  const [langOpen, setLangOpen] = useState(false);
  const [toolsOpen, setToolsOpen] = useState(false);

  const isActive = (path) => location.pathname === path;
  const isToolActive = () => TOOLS.some((t) => location.pathname === t.path);

  const mainLinks = [
    { key: 'home', path: '/', icon: Sprout },
    { key: 'planner', path: '/planner', icon: Leaf },
    { key: 'myGarden', path: '/my-garden', icon: Sprout },
    { key: 'detect', path: '/detect', icon: Leaf },
  ];

  const handleLogout = async () => {
    await logout();
    setProfileOpen(false);
    navigate('/');
  };

  return (
    <nav className="sticky top-0 z-50 border-b border-forest-700 bg-forest-950/80 backdrop-blur-md select-none">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">

          {/* Brand */}
          <div className="flex items-center">
            <Link to="/" className="flex items-center gap-2" onClick={() => setMobileOpen(false)}>
              <span className="text-2xl">🌱</span>
              <span className="font-display font-extrabold text-xl tracking-tight bg-gradient-to-r from-accent-green to-accent-mint bg-clip-text text-transparent">
                UrbanSprout
              </span>
            </Link>
          </div>

          {/* Desktop nav */}
          <div className="hidden md:flex items-center space-x-1">
            {mainLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                className={`px-3 py-2 rounded-lg font-body font-medium text-sm transition-all duration-200 ${
                  isActive(link.path)
                    ? 'text-accent-green bg-accent-green/10'
                    : 'text-forest-600 hover:text-accent-mint hover:bg-forest-900'
                }`}
              >
                {t(`nav.${link.key}`)}
              </Link>
            ))}

            {/* Tools dropdown */}
            <div className="relative">
              <button
                onClick={() => setToolsOpen(!toolsOpen)}
                className={`flex items-center gap-1.5 px-3 py-2 rounded-lg font-body font-medium text-sm transition-all duration-200 ${
                  isToolActive()
                    ? 'text-accent-green bg-accent-green/10'
                    : 'text-forest-600 hover:text-accent-mint hover:bg-forest-900'
                }`}
              >
                <Wrench className="w-3.5 h-3.5" />
                {t('nav.tools')}
                <ChevronDown className={`w-3 h-3 transition-transform ${toolsOpen ? 'rotate-180' : ''}`} />
              </button>
              {toolsOpen && (
                <>
                  <div className="fixed inset-0 z-10" onClick={() => setToolsOpen(false)} />
                  <div className="absolute left-0 mt-2 w-52 rounded-xl border border-forest-700 bg-forest-900 shadow-glow-green p-1 z-20">
                    {TOOLS.map((tool) => {
                      const Icon = tool.icon;
                      return (
                        <Link
                          key={tool.path}
                          to={tool.path}
                          onClick={() => setToolsOpen(false)}
                          className={`flex items-center gap-2.5 w-full px-3 py-2.5 text-sm font-medium rounded-lg transition-colors ${
                            isActive(tool.path)
                              ? 'bg-forest-800 text-accent-green'
                              : 'text-forest-600 hover:bg-forest-800 hover:text-accent-mint'
                          }`}
                        >
                          <Icon className="w-4 h-4" />
                          {t(`nav.${tool.key}`)}
                        </Link>
                      );
                    })}
                  </div>
                </>
              )}
            </div>

            {user && (
              <Link
                to="/history"
                className={`px-3 py-2 rounded-lg font-body font-medium text-sm transition-all duration-200 ${
                  isActive('/history')
                    ? 'text-accent-green bg-accent-green/10'
                    : 'text-forest-600 hover:text-accent-mint hover:bg-forest-900'
                }`}
              >
                {t('nav.history')}
              </Link>
            )}
          </div>

          {/* Right: lang + auth */}
          <div className="hidden md:flex items-center gap-2">
            {/* API key status */}
            <Link
              to="/settings"
              title={hasKey ? 'API key connected' : 'Add your API key'}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl border transition-all text-xs font-semibold font-body ${
                hasKey
                  ? 'border-accent-green/40 text-accent-green hover:bg-accent-green/5'
                  : 'border-accent-amber/40 text-accent-amber hover:bg-accent-amber/5'
              }`}
            >
              <KeyRound className="w-3.5 h-3.5" />
              <span>{hasKey ? 'Key set' : 'Add key'}</span>
            </Link>

            {/* Language picker */}
            <div className="relative">
              <button
                onClick={() => setLangOpen(!langOpen)}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-forest-700 hover:border-accent-green hover:bg-forest-900 transition-all text-xs font-semibold font-body text-forest-50"
              >
                <Globe className="w-3.5 h-3.5 text-accent-green" />
                <span>{languages[language].flag} {languages[language].nativeName}</span>
                <ChevronDown className={`w-3 h-3 text-forest-600 transition-transform ${langOpen ? 'rotate-180' : ''}`} />
              </button>
              {langOpen && (
                <>
                  <div className="fixed inset-0 z-10" onClick={() => setLangOpen(false)} />
                  <div className="absolute right-0 mt-3 w-40 rounded-xl border border-forest-700 bg-forest-900 shadow-glow-green p-1 z-20">
                    {Object.keys(languages).map((key) => (
                      <button
                        key={key}
                        onClick={() => { setLanguage(key); setLangOpen(false); }}
                        className={`flex items-center gap-2.5 w-full px-3 py-2 text-xs font-medium rounded-lg transition-colors ${
                          language === key ? 'bg-forest-800 text-accent-green' : 'text-forest-600 hover:bg-forest-800 hover:text-accent-mint'
                        }`}
                      >
                        <span>{languages[key].flag}</span>
                        <span>{languages[key].nativeName}</span>
                      </button>
                    ))}
                  </div>
                </>
              )}
            </div>

            {/* Auth */}
            {user ? (
              <div className="relative">
                <button
                  onClick={() => setProfileOpen(!profileOpen)}
                  className="flex items-center gap-2 p-1.5 rounded-full border border-forest-700 hover:border-accent-green bg-forest-900 transition-all"
                >
                  <img src={user.photoURL} alt={user.displayName} className="w-8 h-8 rounded-full border border-forest-700 object-cover" />
                </button>
                {profileOpen && (
                  <>
                    <div className="fixed inset-0 z-10" onClick={() => setProfileOpen(false)} />
                    <div className="absolute right-0 mt-3 w-56 rounded-xl border border-forest-700 bg-forest-900 shadow-glow-green p-2 z-20">
                      <div className="px-3 py-2.5 border-b border-forest-800">
                        <p className="font-body font-semibold text-sm text-forest-50 truncate">{user.displayName}</p>
                        <p className="font-body text-xs text-forest-600 truncate">{user.email || user.phoneNumber}</p>
                      </div>
                      <div className="p-1 space-y-1 mt-1">
                        <Link to="/history" onClick={() => setProfileOpen(false)}
                          className="flex items-center gap-2.5 w-full px-3 py-2 text-sm font-medium text-forest-600 rounded-lg hover:bg-forest-800 hover:text-accent-mint transition-colors">
                          <HistoryIcon className="w-4 h-4" />{t('nav.myHistory')}
                        </Link>
                        <Link to="/my-garden" onClick={() => setProfileOpen(false)}
                          className="flex items-center gap-2.5 w-full px-3 py-2 text-sm font-medium text-forest-600 rounded-lg hover:bg-forest-800 hover:text-accent-mint transition-colors">
                          <Sprout className="w-4 h-4" />{t('nav.myGarden')}
                        </Link>
                        <button onClick={handleLogout}
                          className="flex items-center gap-2.5 w-full px-3 py-2 text-sm font-medium text-accent-red rounded-lg hover:bg-accent-red/10 transition-colors text-left">
                          <LogOut className="w-4 h-4" />{t('nav.logout')}
                        </button>
                      </div>
                    </div>
                  </>
                )}
              </div>
            ) : (
              <Link to="/login"
                className="font-body font-semibold text-xs uppercase tracking-wider text-accent-green hover:text-forest-950 px-4 py-2 border border-accent-green hover:bg-accent-green rounded-lg transition-all">
                {t('nav.login')}
              </Link>
            )}
          </div>

          {/* Mobile hamburger */}
          <div className="flex items-center md:hidden">
            <button onClick={() => setMobileOpen(!mobileOpen)} className="text-forest-600 hover:text-accent-green p-1">
              {mobileOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile drawer */}
      {mobileOpen && (
        <div className="md:hidden border-t border-forest-700 bg-forest-950">
          <div className="px-4 pt-2 pb-4 space-y-1">
            {mainLinks.map((link) => (
              <Link key={link.path} to={link.path} onClick={() => setMobileOpen(false)}
                className={`block px-4 py-2.5 rounded-lg font-body font-semibold text-sm transition-all ${
                  isActive(link.path) ? 'bg-forest-800 text-accent-green border-l-4 border-accent-green' : 'text-forest-600 hover:bg-forest-900 hover:text-accent-mint'
                }`}>
                {t(`nav.${link.key}`)}
              </Link>
            ))}
            <div className="pt-1 pb-1">
              <p className="px-4 text-[10px] font-bold font-display text-forest-600 uppercase tracking-widest mb-1">{t('nav.tools')}</p>
              {TOOLS.map((tool) => (
                <Link key={tool.path} to={tool.path} onClick={() => setMobileOpen(false)}
                  className={`block px-4 py-2.5 rounded-lg font-body font-semibold text-sm transition-all ${
                    isActive(tool.path) ? 'bg-forest-800 text-accent-green border-l-4 border-accent-green' : 'text-forest-600 hover:bg-forest-900 hover:text-accent-mint'
                  }`}>
                  {t(`nav.${tool.key}`)}
                </Link>
              ))}
            </div>

            {/* API key */}
            <Link to="/settings" onClick={() => setMobileOpen(false)}
              className={`flex items-center gap-2 w-full px-4 py-2.5 rounded-lg font-body font-semibold text-sm transition-all ${
                hasKey ? 'text-accent-green hover:bg-forest-900' : 'text-accent-amber hover:bg-forest-900'
              }`}>
              <KeyRound className="w-4 h-4" />{hasKey ? 'API Key — connected' : 'Add your API Key'}
            </Link>

            {/* Language grid */}
            <div className="border-t border-forest-800 pt-3">
              <div className="grid grid-cols-3 gap-2">
                {Object.keys(languages).map((key) => (
                  <button key={key} onClick={() => setLanguage(key)}
                    className={`flex flex-col items-center py-2 rounded-xl border text-xs font-semibold transition-all ${
                      language === key ? 'border-accent-green bg-accent-green/10 text-accent-green' : 'border-forest-800 bg-forest-900/40 text-forest-600'
                    }`}>
                    <span className="text-lg">{languages[key].flag}</span>
                    <span className="text-[10px] mt-0.5">{languages[key].nativeName}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Auth */}
            <div className="border-t border-forest-800 pt-3">
              {user ? (
                <div className="space-y-2">
                  <div className="flex items-center gap-3 px-4 py-2">
                    <img src={user.photoURL} alt={user.displayName} className="w-10 h-10 rounded-full border border-forest-700" />
                    <div>
                      <p className="font-body text-sm font-semibold text-forest-50">{user.displayName}</p>
                      <p className="font-body text-xs text-forest-600 truncate max-w-[200px]">{user.email || user.phoneNumber}</p>
                    </div>
                  </div>
                  {user && (
                    <Link to="/history" onClick={() => setMobileOpen(false)}
                      className="flex items-center gap-2 w-full px-4 py-2.5 rounded-lg font-body font-semibold text-sm text-forest-600 hover:bg-forest-900 hover:text-accent-mint">
                      <HistoryIcon className="w-4 h-4" />{t('nav.history')}
                    </Link>
                  )}
                  <button onClick={() => { setMobileOpen(false); handleLogout(); }}
                    className="flex items-center gap-2 w-full px-4 py-2.5 rounded-lg font-body font-semibold text-sm text-accent-red hover:bg-accent-red/10">
                    <LogOut className="w-4 h-4" />{t('nav.logout')}
                  </button>
                </div>
              ) : (
                <Link to="/login" onClick={() => setMobileOpen(false)}
                  className="block text-center w-full bg-accent-green hover:bg-accent-mint text-forest-950 font-body font-bold py-2.5 rounded-lg transition-colors">
                  {t('nav.login')}
                </Link>
              )}
            </div>
          </div>
        </div>
      )}
    </nav>
  );
}
