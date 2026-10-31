import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Info, CircleNotch } from '@phosphor-icons/react';
import { Dropzone } from '../../components/Dropzone/Dropzone';
import { ResultCanvas } from '../../components/ResultCanvas/ResultCanvas';
import { DetectionCard } from '../../components/DetectionCard/DetectionCard';
import { EmptyState } from '../../components/EmptyState/EmptyState';
import { InlineError } from '../../components/InlineError/InlineError';
import { api } from '../../api/client';
import type { DetectionResponse, HealthResponse, ApiError } from '../../api/types';
import styles from './ScanPage.module.css';

interface ScanPageProps {
  health: HealthResponse | null;
}

export const ScanPage: React.FC<ScanPageProps> = ({ health }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [confidence, setConfidence] = useState<number>(0.25);
  const [saveHistory, setSaveHistory] = useState<boolean>(false);

  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [elapsedSeconds, setElapsedSeconds] = useState<number>(0);
  const [result, setResult] = useState<DetectionResponse | null>(null);
  const [error, setError] = useState<ApiError | Error | null>(null);
  const [selectedDetectionIdx, setSelectedDetectionIdx] = useState<number | null>(null);

  const timerRef = useRef<number | null>(null);

  // Set default confidence from backend health config if available
  useEffect(() => {
    if (health?.confidence_range?.default) {
      setConfidence(health.confidence_range.default);
    }
  }, [health]);

  // Clean up object URLs
  useEffect(() => {
    return () => {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
      if (timerRef.current) {
        window.clearInterval(timerRef.current);
      }
    };
  }, [previewUrl]);

  const handleFileSelect = async (file: File) => {
    setError(null);
    setSelectedFile(file);

    // Create local object URL for preview
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    const objUrl = URL.createObjectURL(file);
    setPreviewUrl(objUrl);

    // Start timer & analysis immediately
    setIsLoading(true);
    setElapsedSeconds(0);
    const startTime = Date.now();
    timerRef.current = window.setInterval(() => {
      setElapsedSeconds(Math.floor((Date.now() - startTime) / 1000));
    }, 100);

    try {
      const data = await api.detectSigns(file, confidence, saveHistory);
      setResult(data);
    } catch (err: any) {
      setError(err);
      setResult(null);
    } finally {
      setIsLoading(false);
      if (timerRef.current) {
        window.clearInterval(timerRef.current);
        timerRef.current = null;
      }
    }
  };

  const handleReset = () => {
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setPreviewUrl(null);
    setSelectedFile(null);
    setResult(null);
    setError(null);
    setSelectedDetectionIdx(null);
  };

  return (
    <div className={styles.pageContainer}>
      <div className="container">
        {/* State 1: Initial View / Hero (No image analyzed yet) */}
        {!result && !isLoading && (
          <section className={styles.heroSection} aria-labelledby="scan-title">
            <div className={styles.textStack}>
              <h1 id="scan-title" className={styles.mainHeading}>
                Nhận diện biển báo giao thông từ ảnh
              </h1>
              <p className={styles.subHeading}>
                Tải ảnh đường phố lên để phát hiện vị trí biển báo, tra cứu ý nghĩa
                và xem khuyến nghị an toàn được đối chiếu theo QCVN 41:2019/BGTVT.
              </p>
            </div>

            {error && (
              <div className={styles.errorWrapper}>
                <InlineError
                  error={error}
                  onRetry={() => selectedFile && handleFileSelect(selectedFile)}
                  onDismiss={() => setError(null)}
                />
              </div>
            )}

            <div className={styles.dropzoneWrapper}>
              <Dropzone
                onFileSelect={handleFileSelect}
                maxUploadMb={health?.max_upload_mb || 10}
                confidence={confidence}
                onConfidenceChange={setConfidence}
                minConfidence={health?.confidence_range?.min || 0.05}
                maxConfidence={health?.confidence_range?.max || 0.95}
                saveHistory={saveHistory}
                onSaveHistoryChange={setSaveHistory}
                disabled={health?.model_loaded === false}
              />
            </div>

            <div className={styles.supportedLinkWrap}>
              <Link to="/signs" className={styles.supportedLink}>
                <span>Xem danh mục 23 lớp biển báo hệ thống hỗ trợ</span>
                <ArrowRight size={16} />
              </Link>
            </div>
          </section>
        )}

        {/* State 2: Processing State */}
        {isLoading && (
          <section className={styles.processingSection} aria-live="polite">
            <div className={styles.processingLayout}>
              <div className={styles.previewCard}>
                {previewUrl && (
                  <img src={previewUrl} alt="Ảnh đang phân tích" className={styles.processingThumb} />
                )}
                <div className={styles.loadingOverlay}>
                  <CircleNotch size={36} className={styles.spinner} />
                  <p className={styles.loadingText}>Đang phân tích ảnh…</p>
                  <span className={`${styles.timerBadge} font-mono tabular-nums`}>
                    {elapsedSeconds}s
                  </span>
                </div>
              </div>

              <div className={styles.skeletonCol}>
                <div className={styles.skeletonHeader} />
                <div className={styles.skeletonCard} />
                <div className={styles.skeletonCard} />
              </div>
            </div>
          </section>
        )}

        {/* State 3: Results State */}
        {result && previewUrl && (
          <section className={styles.resultSection} aria-label="Kết quả nhận diện">
            {/* Summary Bar */}
            <div className={styles.summaryBar}>
              <div className={styles.summaryStats}>
                <span className={styles.statCount}>
                  <strong>{result.summary.detection_count}</strong> biển báo được phát hiện
                </span>
                <span className={styles.statDot}>·</span>
                <span className={`${styles.statTime} font-mono tabular-nums`}>
                  {result.summary.processing_ms} ms
                </span>
                <span className={styles.statDot}>·</span>
                <span className={`${styles.statVersion} font-mono`}>
                  Model v{health?.model_version || '1.0'}
                </span>
              </div>
              <span className={styles.summaryNote}>Thời gian xử lý phía server</span>
            </div>

            {/* Warnings list if any */}
            {result.warnings && result.warnings.length > 0 && (
              <div className={styles.warningsList}>
                {result.warnings.map((warn, i) => (
                  <div key={i} className={styles.warnItem}>
                    <Info size={16} />
                    <span>{warn}</span>
                  </div>
                ))}
              </div>
            )}

            {/* Main Result Grid: 7 cols Image (Sticky) + 5 cols Results Cards */}
            <div className={styles.resultGrid}>
              {/* Left Column: Canvas Sticky */}
              <div className={styles.canvasCol}>
                <ResultCanvas
                  originalImageUrl={previewUrl}
                  detectionData={result}
                  selectedIdx={selectedDetectionIdx}
                  onSelectDetection={setSelectedDetectionIdx}
                  onReset={handleReset}
                />
              </div>

              {/* Right Column: Cards or Empty State */}
              <div className={styles.cardsCol}>
                {result.summary.detection_count === 0 ? (
                  <div className={`ui-card ${styles.emptyBox}`}>
                    <EmptyState
                      title="Không phát hiện biển báo trong phạm vi hỗ trợ"
                      description="Biển báo trong ảnh có thể ở quá xa, bị che khuất, thiếu sáng hoặc không thuộc tập 23 lớp biển báo mô hình đã được huấn luyện."
                      action={
                        <button
                          type="button"
                          className="btn btn-primary btn-sm"
                          onClick={handleReset}
                        >
                          Thử ảnh khác
                        </button>
                      }
                    />
                  </div>
                ) : (
                  <div className={styles.cardsList}>
                    {result.detections.map((det, idx) => (
                      <DetectionCard
                        key={idx}
                        detection={det}
                        index={idx}
                        isSelected={selectedDetectionIdx === idx}
                        isDimmed={
                          selectedDetectionIdx !== null && selectedDetectionIdx !== idx
                        }
                        onHover={() => setSelectedDetectionIdx(idx)}
                        onLeave={() => setSelectedDetectionIdx(null)}
                      />
                    ))}
                  </div>
                )}

                {/* Collapsible Limitation Notice per UI_UX.md §14.6.3 */}
                <details className={styles.limitDetails}>
                  <summary className={styles.limitSummary}>
                    <Info size={15} />
                    <span>Lưu ý về phạm vi và tính pháp lý</span>
                  </summary>
                  <p className={styles.limitContent}>
                    Kết quả chỉ mang tính tham khảo phục vụ học tập. Ngữ cảnh đường sá, vạch kẻ đường
                    và biển phụ có thể thay đổi hiệu lực của biển. Không phát hiện biển báo không đồng
                    nghĩa ảnh hoàn toàn không có biển báo.
                  </p>
                </details>
              </div>
            </div>
          </section>
        )}
      </div>
    </div>
  );
};
