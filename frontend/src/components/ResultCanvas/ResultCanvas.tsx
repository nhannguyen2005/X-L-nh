import React, { useState } from 'react';
import { DownloadSimple, ArrowCounterClockwise, Eye, Image as ImageIcon } from '@phosphor-icons/react';
import type { DetectionResponse } from '../../api/types';
import styles from './ResultCanvas.module.css';

interface ResultCanvasProps {
  originalImageUrl: string;
  detectionData: DetectionResponse;
  selectedIdx: number | null;
  onSelectDetection: (index: number | null) => void;
  onReset: () => void;
}

// BGR / Hex colors for sign groups
const GROUP_COLORS: Record<string, string> = {
  'Biển cấm': '#C8102E',
  'Biển nguy hiểm và cảnh báo': '#F2B705',
  'Biển hiệu lệnh': '#0B5CAD',
  'Biển chỉ dẫn': '#1E3A8A',
};
const DEFAULT_COLOR = '#52525B';

export const ResultCanvas: React.FC<ResultCanvasProps> = ({
  originalImageUrl,
  detectionData,
  selectedIdx,
  onSelectDetection,
  onReset,
}) => {
  const [viewMode, setViewMode] = useState<'annotated' | 'original'>('annotated');
  const { width, height, annotated_image } = detectionData.image;

  const handleDownload = () => {
    const a = document.createElement('a');
    a.href = annotated_image;
    a.download = `trafficsign_result_${detectionData.request_id.slice(0, 8)}.jpg`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  return (
    <div className={styles.wrapper}>
      {/* View Switcher Controls */}
      <div className={styles.controlsBar}>
        <div className={styles.segmentedControl} role="radiogroup" aria-label="Chế độ hiển thị ảnh">
          <button
            type="button"
            className={`${styles.segmentBtn} ${viewMode === 'annotated' ? styles.segmentActive : ''}`}
            onClick={() => setViewMode('annotated')}
            aria-checked={viewMode === 'annotated'}
            role="radio"
          >
            <Eye size={16} />
            <span>Kết quả phân tích</span>
          </button>
          <button
            type="button"
            className={`${styles.segmentBtn} ${viewMode === 'original' ? styles.segmentActive : ''}`}
            onClick={() => setViewMode('original')}
            aria-checked={viewMode === 'original'}
            role="radio"
          >
            <ImageIcon size={16} />
            <span>Ảnh gốc</span>
          </button>
        </div>

        <div className={styles.actionBtns}>
          <button
            type="button"
            className="btn btn-secondary btn-sm"
            onClick={handleDownload}
            title="Tải ảnh kết quả về máy"
          >
            <DownloadSimple size={16} />
            <span>Tải ảnh</span>
          </button>
          <button
            type="button"
            className="btn btn-secondary btn-sm"
            onClick={onReset}
            title="Quét ảnh khác"
          >
            <ArrowCounterClockwise size={16} />
            <span>Quét lại</span>
          </button>
        </div>
      </div>

      {/* Main Responsive Canvas with SVG Interactive Overlay */}
      <div
        className={styles.canvasContainer}
        style={{ aspectRatio: `${width} / ${height}` }}
      >
        <img
          src={originalImageUrl}
          alt={`Ảnh đã phân tích: phát hiện ${detectionData.summary.detection_count} biển báo`}
          className={styles.baseImage}
        />

        {viewMode === 'annotated' && (
          <svg
            className={styles.svgOverlay}
            viewBox={`0 0 ${width} ${height}`}
            preserveAspectRatio="none"
          >
            {detectionData.detections.map((det, idx) => {
              const { x1, y1, x2, y2 } = det.bbox;
              const boxW = Math.max(1, x2 - x1);
              const boxH = Math.max(1, y2 - y1);
              const isSelected = selectedIdx === idx;
              const isDimmed = selectedIdx !== null && !isSelected;

              const groupName = det.sign?.group || '';
              const strokeColor = GROUP_COLORS[groupName] || DEFAULT_COLOR;
              const confPct = Math.round(det.confidence * 100);
              const signName = det.sign?.name || det.class_name;
              const labelText = `${idx + 1} · ${confPct}%`;

              // Badge size proportional to image resolution
              const badgeH = Math.max(22, Math.round(height * 0.035));
              const badgeW = Math.max(48, Math.round(badgeH * 2.4));
              const badgeY = Math.max(0, y1 - badgeH - 2);

              return (
                <g
                  key={idx}
                  className={`${styles.boxGroup} ${isSelected ? styles.boxSelected : ''} ${
                    isDimmed ? styles.boxDimmed : ''
                  }`}
                  tabIndex={0}
                  role="button"
                  aria-label={`Biển ${idx + 1}: ${signName}, độ tin cậy ${confPct}%`}
                  onMouseEnter={() => onSelectDetection(idx)}
                  onMouseLeave={() => onSelectDetection(null)}
                  onFocus={() => onSelectDetection(idx)}
                  onBlur={() => onSelectDetection(null)}
                  onClick={() => {
                    onSelectDetection(idx);
                    const el = document.getElementById(`det-card-${idx}`);
                    el?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                  }}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                      e.preventDefault();
                      onSelectDetection(idx);
                      const el = document.getElementById(`det-card-${idx}`);
                      el?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                    }
                  }}
                >
                  {/* Bounding box rectangle */}
                  <rect
                    x={x1}
                    y={y1}
                    width={boxW}
                    height={boxH}
                    fill={isSelected ? strokeColor : 'transparent'}
                    fillOpacity={isSelected ? 0.15 : 0}
                    stroke={strokeColor}
                    strokeWidth={isSelected ? 4 : 3}
                    strokeDasharray={det.verification_required ? '6 4' : 'none'}
                    vectorEffect="non-scaling-stroke"
                    rx={2}
                  />

                  {/* Top Badge for Order & Confidence */}
                  <rect
                    x={x1}
                    y={badgeY}
                    width={badgeW}
                    height={badgeH}
                    fill={strokeColor}
                    rx={3}
                  />
                  <text
                    x={x1 + badgeW / 2}
                    y={badgeY + badgeH / 2 + 1}
                    fill="#FFFFFF"
                    fontSize={Math.max(11, Math.round(badgeH * 0.55))}
                    fontWeight="600"
                    fontFamily="var(--font-mono)"
                    textAnchor="middle"
                    dominantBaseline="middle"
                  >
                    {labelText}
                  </text>
                </g>
              );
            })}
          </svg>
        )}
      </div>
    </div>
  );
};
