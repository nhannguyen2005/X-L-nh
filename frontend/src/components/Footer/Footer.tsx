import React from 'react';
import { Link } from 'react-router-dom';
import styles from './Footer.module.css';

export const Footer: React.FC = () => {
  return (
    <footer className={styles.footer}>
      <div className={`container ${styles.container}`}>
        <p className={styles.disclaimer}>
          Prototype phục vụ học tập. Không thay thế việc quan sát biển báo thực tế.
        </p>
        <div className={styles.links}>
          <Link to="/about" className={styles.link}>
            Giới thiệu &amp; nguồn dữ liệu
          </Link>
        </div>
      </div>
    </footer>
  );
};
