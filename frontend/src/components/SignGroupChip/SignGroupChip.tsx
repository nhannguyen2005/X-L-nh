import React from 'react';
import { SignGlyph } from '../SignGlyph/SignGlyph';
import styles from './SignGroupChip.module.css';

interface SignGroupChipProps {
  group?: string | null;
  size?: 'sm' | 'md';
}

export const SignGroupChip: React.FC<SignGroupChipProps> = ({ group, size = 'md' }) => {
  const normGroup = (group || '').trim().toLowerCase();

  let groupClass = styles.unknown;
  let label = group || 'Chưa có thông tin';

  if (normGroup.includes('cấm')) {
    groupClass = styles.prohibitory;
    label = 'Biển cấm';
  } else if (normGroup.includes('nguy hiểm') || normGroup.includes('cảnh báo')) {
    groupClass = styles.danger;
    label = 'Nguy hiểm';
  } else if (normGroup.includes('hiệu lệnh')) {
    groupClass = styles.mandatory;
    label = 'Hiệu lệnh';
  } else if (normGroup.includes('chỉ dẫn')) {
    groupClass = styles.guide;
    label = 'Chỉ dẫn';
  }

  return (
    <span className={`${styles.chip} ${groupClass} ${size === 'sm' ? styles.sm : ''}`}>
      <SignGlyph group={group} size={size === 'sm' ? 14 : 16} />
      <span>{label}</span>
    </span>
  );
};
