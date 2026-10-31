import React from 'react';
import { NavLink } from 'react-router-dom';
import { StatusBadge } from '../StatusBadge/StatusBadge';
import type { HealthResponse } from '../../api/types';
import styles from './Navbar.module.css';

interface NavbarProps {
  health: HealthResponse | null;
  healthLoading: boolean;
  healthError: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({ health, healthLoading, healthError }) => {
  return (
    <header className={styles.header}>
      <div className={`container ${styles.container}`}>
        {/* Brand */}
        <NavLink to="/" className={styles.brand}>
          <div className={styles.logoIcon}>
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2.5" />
              <line x1="7" y1="12" x2="17" y2="12" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" />
            </svg>
          </div>
          <span className={styles.brandTitle}>TrafficSign AI</span>
        </NavLink>

        {/* Desktop Navigation Links */}
        <nav className={styles.nav} aria-label="Điều hướng chính">
          <NavLink
            to="/"
            end
            className={({ isActive }) => `${styles.navLink} ${isActive ? styles.active : ''}`}
          >
            Quét ảnh
          </NavLink>
          <NavLink
            to="/signs"
            className={({ isActive }) => `${styles.navLink} ${isActive ? styles.active : ''}`}
          >
            Tra cứu
          </NavLink>
          <NavLink
            to="/history"
            className={({ isActive }) => `${styles.navLink} ${isActive ? styles.active : ''}`}
          >
            Lịch sử
          </NavLink>
          <NavLink
            to="/evaluation"
            className={({ isActive }) => `${styles.navLink} ${isActive ? styles.active : ''}`}
          >
            Đánh giá
          </NavLink>
          <NavLink
            to="/about"
            className={({ isActive }) => `${styles.navLink} ${isActive ? styles.active : ''}`}
          >
            Giới thiệu
          </NavLink>
        </nav>

        {/* Status Indicator */}
        <div className={styles.statusWrap}>
          {healthLoading ? (
            <StatusBadge status="info" label="Đang kết nối..." />
          ) : healthError || !health?.model_loaded ? (
            <StatusBadge
              status="not-ready"
              label="Model chưa sẵn sàng"
              sublabel={health?.model_version}
            />
          ) : (
            <StatusBadge
              status="ready"
              label="Model sẵn sàng"
              sublabel={health.model_version}
            />
          )}
        </div>
      </div>
    </header>
  );
};
