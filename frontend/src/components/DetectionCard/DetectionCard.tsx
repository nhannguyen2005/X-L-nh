import React from 'react';
import { Link } from 'react-router-dom';
import {
  WarningOctagon,
  Warning,
  Info,
  Question,
  ArrowSquareOut,
} from '@phosphor-icons/react';
import { SignGlyph } from '../SignGlyph/SignGlyph';
import { SignGroupChip } from '../SignGroupChip/SignGroupChip';
import { ConfidenceMeter } from '../ConfidenceMeter/ConfidenceMeter';
import type { DetectionItem, WarningLevel } from '../../api/types';
import styles from './DetectionCard.module.css';

interface DetectionCardProps {
  detection: DetectionItem;
  index: number;
  isSelected: boolean;
  isDimmed: boolean;
  onHover: () => void;
  onLeave: () => void;
}

function renderWarningBadge(level: WarningLevel) {
  switch (level) {
    case 'high':
      return (
        <span className={`${styles.warnBadge} ${styles.warnHigh}`}>
          <WarningOctagon size={16} weight="regular" />
          <span>Mức cao</span>
        </span>
      );
    case 'medium':
      return (
        <span className={`${styles.warnBadge} ${styles.warnMedium}`}>
          <Warning size={16} weight="regular" />
          <span>Trung bình</span>
        </span>
      );
    case 'low':
      return (
        <span className={`${styles.warnBadge} ${styles.warnLow}`}>
          <Info size={16} weight="regular" />
          <span>Thấp</span>
        </span>
      );
    case 'info':
    default:
      return (
        <span className={`${styles.warnBadge} ${styles.warnInfo}`}>
          <Info size={16} weight="regular" />
          <span>Thông tin</span>
        </span>
      );
  }
}

export const DetectionCard: React.FC<DetectionCardProps> = ({
  detection,
  index,
  isSelected,
  isDimmed,
  onHover,
  onLeave,
}) => {
  const { sign, class_name, confidence, verification_required } = detection;
  const isUnknown = !sign;

  let cardVariantClass = '';
  if (verification_required) {
    cardVariantClass = styles.uncertain;
  } else if (isUnknown) {
    cardVariantClass = styles.unknown;
  }

  // Display title per UI_UX.md §14.6.3
  let title = sign?.name || class_name;
  if (verification_required && sign) {
    title = `Có thể là: ${sign.name}`;
  }

  return (
    <article
      id={`det-card-${index}`}
      className={`ui-card ${styles.card} ${cardVariantClass} ${
        isSelected ? styles.cardSelected : ''
      } ${isDimmed ? styles.cardDimmed : ''}`}
      onMouseEnter={onHover}
      onMouseLeave={onLeave}
      tabIndex={0}
      onFocus={onHover}
      onBlur={onLeave}
    >
      {/* Verification / Uncertainty Banner */}
      {verification_required && (
        <div className={styles.uncertainBanner}>
          <Question size={15} weight="bold" />
          <span>Kết quả chưa chắc chắn — cần kiểm chứng thêm</span>
        </div>
      )}

      {/* Header Row: Order Number + Glyph + Name + Group Chip */}
      <div className={styles.headerRow}>
        <div className={styles.orderBadge}>{index + 1}</div>

        <div className={styles.glyphWrap}>
          {sign?.image_url ? (
            <img
              src={sign.image_url}
              alt={title}
              className={styles.signThumb}
              loading="lazy"
            />
          ) : (
            <SignGlyph group={sign?.group} size={36} />
          )}
        </div>

        <div className={styles.nameWrap}>
          <h3 className={styles.title}>{title}</h3>
          <div className={styles.metaRow}>
            {sign?.sign_code && (
              <span className={`${styles.signCode} font-mono`}>
                {sign.sign_code}
              </span>
            )}
            <SignGroupChip group={sign?.group} size="sm" />
          </div>
        </div>
      </div>

      {/* Confidence Row */}
      <div className={styles.confRow}>
        <span className={styles.metaLabel}>Độ tin cậy:</span>
        <ConfidenceMeter
          value={confidence}
          verificationRequired={verification_required}
        />
      </div>

      {/* Content depending on Catalog verification */}
      {isUnknown ? (
        <div className={styles.unknownNotice}>
          <p>
            Nhãn <code>{class_name}</code> chưa có thông tin quy chuẩn được kiểm chứng trong catalog.
          </p>
        </div>
      ) : (
        <>
          {/* Meaning */}
          <div className={styles.sectionBlock}>
            <h4 className={styles.sectionTitle}>Ý nghĩa quy chuẩn:</h4>
            <p className={styles.meaningText}>{sign.meaning}</p>
          </div>

          {/* Recommended Action */}
          <div className={styles.actionBlock}>
            <div className={styles.actionHeader}>
              <span className={styles.actionTitle}>Hành vi cần tuân thủ:</span>
              {renderWarningBadge(sign.warning_level)}
            </div>
            <p className={styles.actionText}>{sign.recommended_action}</p>
          </div>

          {/* Footer Metadata */}
          <div className={styles.footerRow}>
            <div className={styles.sourceMeta}>
              <span>Nguồn: {sign.source}</span>
              {sign.source_checked_at && (
                <span> · Kiểm tra ngày: {sign.source_checked_at}</span>
              )}
            </div>

            {sign.id && (
              <Link
                to={`/signs/${sign.id}`}
                className={styles.detailLink}
                title="Xem chi tiết biển báo này trong danh mục"
              >
                <span>Xem chi tiết</span>
                <ArrowSquareOut size={14} />
              </Link>
            )}
          </div>
        </>
      )}
    </article>
  );
};
