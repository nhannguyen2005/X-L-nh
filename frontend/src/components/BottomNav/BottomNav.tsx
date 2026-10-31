import React from 'react';
import { NavLink } from 'react-router-dom';
import { Scan, BookOpen, ClockCounterClockwise, ChartBar, Info } from '@phosphor-icons/react';
import styles from './BottomNav.module.css';

export const BottomNav: React.FC = () => {
  return (
    <nav className={styles.bottomNav} aria-label="Điều hướng di động">
      <NavLink
        to="/"
        end
        className={({ isActive }) => `${styles.tab} ${isActive ? styles.active : ''}`}
      >
        <Scan size={22} weight="regular" />
        <span className={styles.tabLabel}>Quét ảnh</span>
      </NavLink>

      <NavLink
        to="/signs"
        className={({ isActive }) => `${styles.tab} ${isActive ? styles.active : ''}`}
      >
        <BookOpen size={22} weight="regular" />
        <span className={styles.tabLabel}>Tra cứu</span>
      </NavLink>

      <NavLink
        to="/history"
        className={({ isActive }) => `${styles.tab} ${isActive ? styles.active : ''}`}
      >
        <ClockCounterClockwise size={22} weight="regular" />
        <span className={styles.tabLabel}>Lịch sử</span>
      </NavLink>

      <NavLink
        to="/evaluation"
        className={({ isActive }) => `${styles.tab} ${isActive ? styles.active : ''}`}
      >
        <ChartBar size={22} weight="regular" />
        <span className={styles.tabLabel}>Đánh giá</span>
      </NavLink>

      <NavLink
        to="/about"
        className={({ isActive }) => `${styles.tab} ${isActive ? styles.active : ''}`}
      >
        <Info size={22} weight="regular" />
        <span className={styles.tabLabel}>Giới thiệu</span>
      </NavLink>
    </nav>
  );
};
