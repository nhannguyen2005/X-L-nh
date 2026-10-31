import React, { useState, useRef } from 'react';
import { UploadSimple, Camera, Sliders, ShieldCheck } from '@phosphor-icons/react';
import styles from './Dropzone.module.css';

interface DropzoneProps {
  onFileSelect: (file: File) => void;
  maxUploadMb: number;
  confidence: number;
  onConfidenceChange: (val: number) => void;
  minConfidence: number;
  maxConfidence: number;
  saveHistory: boolean;
  onSaveHistoryChange: (val: boolean) => void;
  disabled?: boolean;
}

export const Dropzone: React.FC<DropzoneProps> = ({
  onFileSelect,
  maxUploadMb,
  confidence,
  onConfidenceChange,
  minConfidence,
  maxConfidence,
  saveHistory,
  onSaveHistoryChange,
  disabled = false,
}) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const [activeTab, setActiveTab] = useState<'upload' | 'camera'>('upload');
  const [cameraError, setCameraError] = useState<string | null>(null);
  const [streamActive, setStreamActive] = useState(false);

  const videoRef = useRef<HTMLVideoElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    if (disabled) return;
    setIsDragOver(true);
  };

  const handleDragLeave = () => {
    setIsDragOver(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    if (disabled) return;

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      onFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      onFileSelect(e.target.files[0]);
    }
  };

  // Camera handling (FR-11)
  const startCamera = async () => {
    setCameraError(null);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } },
      });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
        setStreamActive(true);
      }
    } catch (err: any) {
      setCameraError('Không thể truy cập camera. Vui lòng cấp quyền trong trình duyệt hoặc sử dụng tính năng tải ảnh.');
      setStreamActive(false);
    }
  };

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream;
      stream.getTracks().forEach((track) => track.stop());
      videoRef.current.srcObject = null;
      setStreamActive(false);
    }
  };

  const capturePhoto = () => {
    if (!videoRef.current) return;
    const canvas = document.createElement('canvas');
    canvas.width = videoRef.current.videoWidth || 640;
    canvas.height = videoRef.current.videoHeight || 480;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
    canvas.toBlob((blob) => {
      if (blob) {
        const file = new File([blob], `camera_${Date.now()}.jpg`, { type: 'image/jpeg' });
        stopCamera();
        setActiveTab('upload');
        onFileSelect(file);
      }
    }, 'image/jpeg', 0.92);
  };

  const switchTab = (tab: 'upload' | 'camera') => {
    if (tab === 'camera') {
      setActiveTab('camera');
      startCamera();
    } else {
      stopCamera();
      setActiveTab('upload');
    }
  };

  return (
    <div className={styles.wrapper}>
      {/* Tab Switcher: Upload vs Camera */}
      <div className={styles.tabBar} role="tablist">
        <button
          type="button"
          role="tab"
          aria-selected={activeTab === 'upload'}
          className={`${styles.tabBtn} ${activeTab === 'upload' ? styles.tabActive : ''}`}
          onClick={() => switchTab('upload')}
        >
          <UploadSimple size={18} />
          <span>Tải ảnh lên</span>
        </button>

        <button
          type="button"
          role="tab"
          aria-selected={activeTab === 'camera'}
          className={`${styles.tabBtn} ${activeTab === 'camera' ? styles.tabActive : ''}`}
          onClick={() => switchTab('camera')}
        >
          <Camera size={18} />
          <span>Chụp ảnh (Webcam)</span>
        </button>
      </div>

      {activeTab === 'upload' ? (
        /* Upload Area */
        <label
          htmlFor="traffic-sign-file-input"
          className={`${styles.dropzone} ${isDragOver ? styles.dragOver : ''} ${
            disabled ? styles.disabled : ''
          }`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          tabIndex={0}
          onKeyDown={(e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault();
              fileInputRef.current?.click();
            }
          }}
        >
          <input
            id="traffic-sign-file-input"
            ref={fileInputRef}
            type="file"
            accept="image/jpeg,image/png"
            className="visually-hidden"
            onChange={handleInputChange}
            disabled={disabled}
          />

          <div className={styles.iconCircle}>
            <UploadSimple size={32} weight="regular" />
          </div>

          <div className={styles.textStack}>
            <p className={styles.primaryText}>
              Kéo thả ảnh vào đây hoặc <span className={styles.highlightText}>Chọn ảnh</span>
            </p>
            <p className={styles.secondaryText}>
              JPG, PNG · tối đa {maxUploadMb} MB
            </p>
          </div>
        </label>
      ) : (
        /* Camera Area */
        <div className={styles.cameraBox}>
          {cameraError ? (
            <div className={styles.cameraErrorBox}>
              <p>{cameraError}</p>
              <button
                type="button"
                className="btn btn-secondary btn-sm"
                onClick={startCamera}
              >
                Thử lại
              </button>
            </div>
          ) : (
            <div className={styles.videoWrap}>
              <video ref={videoRef} autoPlay playsInline muted className={styles.video} />
              {streamActive && (
                <div className={styles.cameraActions}>
                  <button
                    type="button"
                    className="btn btn-primary"
                    onClick={capturePhoto}
                  >
                    <Camera size={18} />
                    <span>Chụp ảnh này</span>
                  </button>
                  <button
                    type="button"
                    className="btn btn-secondary"
                    onClick={() => switchTab('upload')}
                  >
                    Hủy
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* Privacy Notice per UI_UX.md §14.6.1 */}
      <div className={styles.privacyNote}>
        <ShieldCheck size={16} />
        <span>Ảnh được xử lý trong bộ nhớ và không được lưu mặc định.</span>
      </div>

      {/* Advanced Options Details */}
      <details className={styles.advancedOptions}>
        <summary className={styles.summaryTitle}>
          <Sliders size={16} />
          <span>Tùy chọn nâng cao (ngưỡng &amp; lưu lịch sử)</span>
        </summary>

        <div className={styles.optionsContent}>
          {/* Confidence Slider */}
          <div className={styles.optionItem}>
            <div className={styles.optionHeader}>
              <label htmlFor="conf-slider" className={styles.optionLabel}>
                Ngưỡng độ tin cậy (Confidence Threshold):
              </label>
              <span className={`${styles.sliderValue} font-mono tabular-nums`}>
                {Math.round(confidence * 100)}% ({confidence.toFixed(2)})
              </span>
            </div>
            <input
              id="conf-slider"
              type="range"
              min={minConfidence}
              max={maxConfidence}
              step={0.05}
              value={confidence}
              onChange={(e) => onConfidenceChange(parseFloat(e.target.value))}
              className={styles.slider}
            />
            <span className={styles.optionHelper}>
              Giữ các phát hiện có độ tin cậy cao hơn ngưỡng này (mặc định 25%).
            </span>
          </div>

          {/* Save History Switch */}
          <div className={styles.optionItem}>
            <label className={styles.switchLabel}>
              <input
                type="checkbox"
                checked={saveHistory}
                onChange={(e) => onSaveHistoryChange(e.target.checked)}
                className={styles.switchInput}
              />
              <span className={styles.switchSlider} />
              <span className={styles.switchText}>Lưu kết quả vào lịch sử quét</span>
            </label>
            <span className={styles.optionHelper}>
              Chỉ lưu metadata (tên file, số lượng phát hiện, thời gian); không lưu tệp ảnh gốc.
            </span>
          </div>
        </div>
      </details>
    </div>
  );
};
