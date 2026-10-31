import React from 'react';
import styles from './ConfidenceMeter.module.css';

interface ConfidenceMeterProps {
  value: number; // 0 to 1
  verificationRequired?: boolean;
  className?: string;
}

export const ConfidenceMeter: React.FC<ConfidenceMeterProps> = ({
  value,
  verificationRequired = false,
  className = '',
}) => {
  const percent = Math.min(100, Math.max(0, Math.round(value * 100)));

  let statusClass = styles.high;
  let statusText = 'Độ tin cậy cao';

  if (verificationRequired || percent < 50) {
    statusClass = styles.uncertain;
    statusText = 'Cần xác minh';
  } else if (percent < 75) {
    statusClass = styles.medium;
    statusText = 'Độ tin cậy vừa';
  }

  return (
    <div
      className={`${styles.container} ${className}`}
      role="meter"
      aria-valuenow={percent}
      aria-valuemin={0}
      aria-valuemax={100}
      aria-label={`Độ tin cậy: ${percent}%, ${statusText}`}
    >
      <div className={styles.track}>
        <div
          className={`${styles.bar} ${statusClass}`}
          style={{ width: `${percent}%` }}
        />
      </div>
      <span className={`${styles.label} tabular-nums ${statusClass}`}>
        {percent}%
      </span>
    </div>
  );
};
