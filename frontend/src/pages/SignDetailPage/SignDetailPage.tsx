import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { CaretRight, ArrowLeft, WarningOctagon, Warning, Info, CalendarCheck, Scales } from '@phosphor-icons/react';
import { SignGlyph } from '../../components/SignGlyph/SignGlyph';
import { SignGroupChip } from '../../components/SignGroupChip/SignGroupChip';
import { InlineError } from '../../components/InlineError/InlineError';
import { api } from '../../api/client';
import type { SignItem } from '../../api/types';
import styles from './SignDetailPage.module.css';

export const SignDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [sign, setSign] = useState<SignItem | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<any>(null);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    setError(null);
    api
      .getSignById(parseInt(id, 10))
      .then(setSign)
      .catch((err) => setError(err))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) {
    return (
      <div className={styles.page}>
        <div className="container">
          <div className={styles.loadingBox}>
            <p>Đang tải thông tin biển báo...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error || !sign) {
    return (
      <div className={styles.page}>
        <div className="container">
          <InlineError error={error || new Error('Không tìm thấy thông tin biển báo.')} />
          <div style={{ marginTop: '16px' }}>
            <Link to="/signs" className="btn btn-secondary btn-sm">
              <ArrowLeft size={16} />
              <span>Quay lại danh mục</span>
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.page}>
      <div className={`container ${styles.container}`}>
        {/* Breadcrumb Navigation */}
        <nav className={styles.breadcrumb} aria-label="Breadcrumb">
          <Link to="/" className={styles.breadLink}>Quét ảnh</Link>
          <CaretRight size={14} className={styles.breadSep} />
          <Link to="/signs" className={styles.breadLink}>Danh mục biển báo</Link>
          <CaretRight size={14} className={styles.breadSep} />
          <span className={styles.breadCurrent}>{sign.sign_code}</span>
        </nav>

        {/* Back Link */}
        <Link to="/signs" className={styles.backBtn}>
          <ArrowLeft size={16} />
          <span>Quay lại danh sách biển báo</span>
        </Link>

        {/* Main Sign Detail Card */}
        <article className={`ui-card ${styles.detailCard}`}>
          {/* Header Info */}
          <div className={styles.cardHeader}>
            <div className={styles.visualBox}>
              {sign.image_url ? (
                <img src={sign.image_url} alt={sign.name} className={styles.signImg} />
              ) : (
                <SignGlyph group={sign.group_name} size={64} />
              )}
            </div>

            <div className={styles.titleStack}>
              <div className={styles.tagRow}>
                <span className={`${styles.codeBadge} font-mono`}>{sign.sign_code}</span>
                <SignGroupChip group={sign.group_name} />
              </div>
              <h1 className={styles.signName}>{sign.name}</h1>
            </div>
          </div>

          {/* Section: Meaning */}
          <section className={styles.section}>
            <h2 className={styles.sectionHeading}>1. Ý nghĩa quy chuẩn</h2>
            <div className={styles.sectionBody}>
              <p>{sign.meaning}</p>
            </div>
          </section>

          {/* Section: Recommended Action */}
          <section className={styles.section}>
            <h2 className={styles.sectionHeading}>2. Hành vi tuân thủ &amp; khuyến nghị an toàn</h2>
            <div className={styles.actionBox}>
              <div className={styles.actionHeader}>
                <span className={styles.actionSub}>Yêu cầu đối với người tham gia giao thông:</span>
                <span className={`${styles.warnBadge} ${styles[sign.warning_level]}`}>
                  {sign.warning_level === 'high' && <WarningOctagon size={16} />}
                  {sign.warning_level === 'medium' && <Warning size={16} />}
                  {(sign.warning_level === 'low' || sign.warning_level === 'info') && <Info size={16} />}
                  <span>Cảnh báo mức: {sign.warning_level}</span>
                </span>
              </div>
              <p className={styles.actionDesc}>{sign.recommended_action}</p>
            </div>
          </section>

          {/* Section: Legal Source & Verification */}
          <section className={styles.section}>
            <h2 className={styles.sectionHeading}>3. Căn cứ pháp lý &amp; kiểm chứng nguồn</h2>
            <div className={styles.legalBox}>
              <div className={styles.legalItem}>
                <Scales size={18} className={styles.legalIcon} />
                <div>
                  <span className={styles.legalLabel}>Văn bản viện dẫn:</span>
                  <p className={styles.legalVal}>{sign.legal_source}</p>
                </div>
              </div>

              <div className={styles.legalItem}>
                <CalendarCheck size={18} className={styles.legalIcon} />
                <div>
                  <span className={styles.legalLabel}>Ngày đối chiếu văn bản:</span>
                  <p className={`${styles.legalVal} font-mono`}>{sign.source_checked_at}</p>
                </div>
              </div>
            </div>
          </section>
        </article>
      </div>
    </div>
  );
};
