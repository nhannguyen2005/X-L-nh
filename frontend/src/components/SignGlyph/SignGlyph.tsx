import React from 'react';
import styles from './SignGlyph.module.css';

interface SignGlyphProps {
  group?: string | null;
  size?: number;
  className?: string;
}

export const SignGlyph: React.FC<SignGlyphProps> = ({ group, size = 24, className = '' }) => {
  const normGroup = (group || '').trim().toLowerCase();

  // Biển cấm: vòng tròn có gạch chéo
  if (normGroup.includes('cấm') || normGroup.includes('prohibitory')) {
    return (
      <svg
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill="none"
        className={`${styles.glyph} ${styles.prohibitory} ${className}`}
        aria-hidden="true"
      >
        <circle cx="12" cy="12" r="9" stroke="currentColor" strokeWidth="2.5" />
        <line x1="5.6" y1="5.6" x2="18.4" y2="18.4" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" />
      </svg>
    );
  }

  // Biển nguy hiểm: tam giác
  if (normGroup.includes('nguy hiểm') || normGroup.includes('cảnh báo') || normGroup.includes('danger')) {
    return (
      <svg
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill="none"
        className={`${styles.glyph} ${styles.danger} ${className}`}
        aria-hidden="true"
      >
        <path
          d="M12 3L21.5 19.5H2.5L12 3Z"
          stroke="currentColor"
          strokeWidth="2.5"
          strokeLinejoin="round"
        />
        <line x1="12" y1="9" x2="12" y2="13" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" />
        <circle cx="12" cy="16.5" r="1.2" fill="currentColor" />
      </svg>
    );
  }

  // Biển hiệu lệnh: hình tròn đặc / viền dày
  if (normGroup.includes('hiệu lệnh') || normGroup.includes('mandatory')) {
    return (
      <svg
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill="none"
        className={`${styles.glyph} ${styles.mandatory} ${className}`}
        aria-hidden="true"
      >
        <circle cx="12" cy="12" r="9.5" fill="currentColor" fillOpacity="0.15" stroke="currentColor" strokeWidth="2.5" />
        <path d="M12 7V17M12 7L8 11M12 7L16 11" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    );
  }

  // Biển chỉ dẫn: hình vuông / chữ nhật
  if (normGroup.includes('chỉ dẫn') || normGroup.includes('guide')) {
    return (
      <svg
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill="none"
        className={`${styles.glyph} ${styles.guide} ${className}`}
        aria-hidden="true"
      >
        <rect x="3" y="3" width="18" height="18" rx="3" stroke="currentColor" strokeWidth="2.5" />
        <path d="M8 12H16M13 8L16 12L13 16" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    );
  }

  // Unknown: Dấu hỏi
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      className={`${styles.glyph} ${styles.unknown} ${className}`}
      aria-hidden="true"
    >
      <circle cx="12" cy="12" r="9" stroke="currentColor" strokeWidth="2" strokeDasharray="3 3" />
      <path d="M9.5 9C9.5 7.6 10.6 6.5 12 6.5C13.4 6.5 14.5 7.6 14.5 9C14.5 10.2 13.5 11 12 12V13.5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
      <circle cx="12" cy="16.5" r="1" fill="currentColor" />
    </svg>
  );
};
