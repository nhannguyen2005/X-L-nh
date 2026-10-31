import React from 'react';
import { MagnifyingGlass } from '@phosphor-icons/react';
import styles from './EmptyState.module.css';

interface EmptyStateProps {
  icon?: React.ReactNode;
  title: string;
  description?: string;
  action?: React.ReactNode;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  icon,
  title,
  description,
  action,
}) => {
  return (
    <div className={styles.emptyContainer}>
      <div className={styles.iconCircle}>
        {icon || <MagnifyingGlass size={32} weight="regular" />}
      </div>
      <h3 className={styles.title}>{title}</h3>
      {description && <p className={styles.description}>{description}</p>}
      {action && <div className={styles.actionWrap}>{action}</div>}
    </div>
  );
};
