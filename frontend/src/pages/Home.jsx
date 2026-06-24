import { Link } from 'react-router-dom';
import {
  Leaf, Sprout, Calendar, Users, BookOpen, MessageCircle,
  FlaskConical, ArrowRight, Star,
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

const MODULES = [
  {
    icon: Leaf,
    key: 'planner',
    path: '/planner',
    color: 'text-accent-green',
    bg: 'bg-accent-green/10 border-accent-green/20',
    glow: 'hover:shadow-glow-green hover:border-accent-green/40',
    num: '01',
  },
  {
    icon: Calendar,
    key: 'calendar',
    path: '/calendar',
    color: 'text-accent-mint',
    bg: 'bg-accent-mint/10 border-accent-mint/20',
    glow: 'hover:shadow-[0_0_20px_rgba(134,239,172,0.15)] hover:border-accent-mint/40',
    num: '02',
  },
  {
    icon: Sprout,
    key: 'myGarden',
    path: '/my-garden',
    color: 'text-accent-green',
    bg: 'bg-accent-green/10 border-accent-green/20',
    glow: 'hover:shadow-glow-green hover:border-accent-green/40',
    num: '03',
  },
  {
    icon: FlaskConical,
    key: 'detect',
    path: '/detect',
    color: 'text-accent-amber',
    bg: 'bg-accent-amber/10 border-accent-amber/20',
    glow: 'hover:shadow-[0_0_20px_rgba(252,211,77,0.15)] hover:border-accent-amber/40',
    num: '04',
  },
  {
    icon: Users,
    key: 'companion',
    path: '/companion',
    color: 'text-accent-mint',
    bg: 'bg-accent-mint/10 border-accent-mint/20',
    glow: 'hover:shadow-[0_0_20px_rgba(134,239,172,0.15)] hover:border-accent-mint/40',
    num: '05',
  },
  {
    icon: BookOpen,
    key: 'guides',
    path: '/guides',
    color: 'text-accent-green',
    bg: 'bg-accent-green/10 border-accent-green/20',
    glow: 'hover:shadow-glow-green hover:border-accent-green/40',
    num: '06',
  },
  {
    icon: MessageCircle,
    key: 'chat',
    path: '/chat',
    color: 'text-accent-amber',
    bg: 'bg-accent-amber/10 border-accent-amber/20',
    glow: 'hover:shadow-[0_0_20px_rgba(252,211,77,0.15)] hover:border-accent-amber/40',
    num: '07',
  },
  {
    icon: Leaf,
    key: 'guides',
    path: '/guides#composting',
    color: 'text-accent-mint',
    bg: 'bg-accent-mint/10 border-accent-mint/20',
    glow: 'hover:shadow-[0_0_20px_rgba(134,239,172,0.15)] hover:border-accent-mint/40',
    num: '08',
    labelOverride: 'Composting Guide',
    descOverride: 'Turn kitchen scraps into rich compost for your containers — step by step.',
  },
];

const MODULE_TITLES = {
  planner: { label: 'Space Planner', desc: 'Tell us your balcony size and sunlight, and we\'ll pick the perfect plants for your setup.' },
  calendar: { label: 'Grow Calendar', desc: 'City-aware monthly guide telling you exactly what to sow, tend, and harvest right now.' },
  myGarden: { label: 'My Garden', desc: 'Track every plant you grow — log milestones, watering notes, and your harvest story.' },
  detect: { label: 'Disease Detector', desc: 'Upload a leaf photo and get an AI diagnosis with an exact treatment prescription.' },
  companion: { label: 'Companion Planting', desc: 'Discover which plants thrive together and which ones to keep far apart.' },
  guides: { label: 'Plant Guides', desc: 'Complete container growing guides — pot size, soil mix, watering, and harvest tips.' },
  chat: { label: 'AI Plant Doctor', desc: 'Describe your plant\'s symptoms in plain language and get an instant diagnosis + fix.' },
};

export default function Home() {
  const { t } = useLanguage();

  return (
    <div className="w-full min-h-screen bg-forest-950 flex flex-col items-center overflow-x-hidden relative">

      {/* Background glow */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-accent-green/8 rounded-full blur-[160px] pointer-events-none z-0" />
      <div className="absolute bottom-1/3 right-10 w-[300px] h-[300px] bg-accent-mint/5 rounded-full blur-[120px] pointer-events-none z-0" />

      {/* Hero */}
      <section className="relative w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-24 md:pt-32 md:pb-36 flex flex-col items-center text-center z-10">

        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-accent-green/30 bg-accent-green/5 text-accent-green text-[10px] font-display font-extrabold uppercase tracking-widest mb-6">
          <Star className="w-3 h-3" />
          {t('home.badge')}
        </div>

        <h1 className="font-display font-black text-5xl sm:text-7xl md:text-8xl text-forest-50 tracking-tight leading-none max-w-4xl">
          {t('home.heroTitle1')}<br />
          <span className="bg-gradient-to-r from-accent-green via-accent-mint to-accent-green bg-[length:200%_auto] animate-pulse bg-clip-text text-transparent">
            {t('home.heroTitle2')}
          </span>
        </h1>

        <p className="font-body text-base sm:text-xl text-forest-600 max-w-2xl mt-6 leading-relaxed">
          {t('home.heroSub')}
        </p>

        <div className="flex flex-col sm:flex-row items-center gap-4 mt-10 w-full sm:w-auto">
          <Link to="/planner"
            className="w-full sm:w-auto text-center bg-accent-green hover:bg-accent-mint text-forest-950 px-8 py-3.5 rounded-xl font-body font-bold text-sm uppercase tracking-wider transition-all duration-300 shadow-glow-green">
            {t('home.ctaPlanner')}
          </Link>
          <Link to="/detect"
            className="w-full sm:w-auto text-center border border-accent-green text-accent-green hover:bg-accent-green/5 px-8 py-3.5 rounded-xl font-body font-bold text-sm uppercase tracking-wider transition-all duration-300">
            {t('home.ctaDetect')}
          </Link>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-8 mt-16 w-full max-w-2xl pt-8 border-t border-forest-700/30">
          {[
            { val: t('home.stat1Val'), label: t('home.stat1Label') },
            { val: t('home.stat2Val'), label: t('home.stat2Label') },
            { val: t('home.stat3Val'), label: t('home.stat3Label') },
          ].map((s, i) => (
            <div key={i} className="flex flex-col items-center">
              <span className="font-display font-black text-3xl sm:text-4xl text-forest-50">{s.val}</span>
              <span className="font-body text-xs text-forest-600 mt-1 uppercase tracking-wider text-center">{s.label}</span>
            </div>
          ))}
        </div>
      </section>

      {/* Modules grid */}
      <section className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-24 z-10">
        <div className="text-center mb-14">
          <h2 className="font-display font-black text-3xl sm:text-4xl text-forest-50 tracking-tight">
            {t('home.howItWorks')}
          </h2>
          <p className="font-body text-sm text-forest-600 mt-3 max-w-xl mx-auto">{t('home.howItWorksSub')}</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {MODULES.map((mod, i) => {
            const Icon = mod.icon;
            const info = mod.labelOverride
              ? { label: mod.labelOverride, desc: mod.descOverride }
              : MODULE_TITLES[mod.key] || { label: mod.key, desc: '' };

            return (
              <Link
                key={i}
                to={mod.path}
                className={`group relative flex flex-col p-6 rounded-2xl border bg-forest-900/50 transition-all duration-300 hover:scale-[1.02] ${mod.glow} border-forest-700/60`}
              >
                <div className="flex items-start justify-between mb-5">
                  <div className={`p-2.5 rounded-xl border ${mod.bg}`}>
                    <Icon className={`w-5 h-5 ${mod.color}`} />
                  </div>
                  <span className="font-display font-black text-3xl text-forest-800 select-none">{mod.num}</span>
                </div>
                <h3 className="font-display font-extrabold text-base text-forest-50 tracking-tight mb-2">
                  {info.label}
                </h3>
                <p className="font-body text-xs leading-relaxed text-forest-600 flex-grow">
                  {info.desc}
                </p>
                <div className="mt-5 flex items-center gap-1.5 font-body font-bold text-xs uppercase tracking-wider text-forest-600 group-hover:text-accent-green transition-colors">
                  Explore <ArrowRight className="w-3.5 h-3.5" />
                </div>
              </Link>
            );
          })}
        </div>
      </section>

      {/* Footer */}
      <footer className="w-full border-t border-forest-800 bg-forest-950/60 backdrop-blur-sm mt-auto py-8 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <span className="text-xl">🌱</span>
            <span className="font-display font-extrabold text-sm text-accent-green tracking-wider">UrbanSprout</span>
            <span className="font-body text-[10px] text-forest-600">| {t('home.footerText')}</span>
          </div>
          <div className="font-body text-xs text-forest-600">{t('home.footerBuilt')}</div>
        </div>
      </footer>
    </div>
  );
}
