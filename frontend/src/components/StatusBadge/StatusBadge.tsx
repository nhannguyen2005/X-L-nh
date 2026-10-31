import React from 'react';
import styles from './StatusBadge.module.css';

interface StatusBadgeProps {
  status: 'ready' | 'not-ready' | 'uncertain' | 'info';
  label: string;
  sublabel?: string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, label, sublabel }) => {
  return (
    <div className={`${styles.badge} ${styles[status]}`}>
      <span className={styles.dot} aria-hidden="true" />
      <span className={styles.label}>{label}</span>
      {sublabel && <span className={`${styles.sublabel} font-mono`}>{sublabel}</span>}
    </div>
  );
};
