export const colors = {
  primary: '#F5F0E8',
  secondary: '#D4A574',
  accent: '#C9B99A',
  green: '#7BA06E',
  orange: '#C4704E',
  gold: '#D4A843',
  text: '#4A3B32',
  textLight: '#6B5E54',
  background: '#FAF7F2',
  backgroundAlt: '#F0EDE5',
  white: '#FFFFFF',
  error: '#E74C3C',
  border: '#E8E0D8',
};

export const typography = {
  h1: { fontSize: 28, fontWeight: '700' as const, color: colors.text },
  h2: { fontSize: 22, fontWeight: '600' as const, color: colors.text },
  h3: { fontSize: 18, fontWeight: '600' as const, color: colors.text },
  body: { fontSize: 16, fontWeight: '400' as const, color: colors.text },
  bodySmall: { fontSize: 14, fontWeight: '400' as const, color: colors.textLight },
  caption: { fontSize: 12, fontWeight: '400' as const, color: colors.textLight },
};

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
};

export const borderRadius = {
  sm: 8,
  md: 16,
  lg: 24,
};
