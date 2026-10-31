import React, { useState } from 'react';
import { WarningCircle, Copy, Check } from '@phosphor-icons/react';
import type { ApiError } from '../../api/types';
import styles from './InlineError.module.css';

interface InlineErrorProps {
  error: ApiError | Error | null;
  onRetry?: () => void;
  onDismiss?: () => void;
}

export const InlineError: React.FC<InlineErrorProps> = ({ error, onRetry, onDismiss }) => {
  const [copied, setCopied] = useState(false);
  if (!error) return null;

  const apiErr = 'code' in error ? (error as ApiError) : null;
  const code = apiErr?.code || 'ERROR';
  const requestId = apiErr?.request_id;
  const message = error.message || 'Đã xảy ra lỗi khi thực hiện thao tác.';

  const handleCopyRequestId = () => {
    if (requestId) {
      navigator.clipboard.writeText(requestId);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className={styles.errorBox} role="alert">
      <div className={styles.iconWrap}>
        <WarningCircle size={22} weight="fill" />
      </div>

      <div className={styles.contentWrap}>
        <div className={styles.header}>
          <span className={styles.errorCode}>{code}</span>
          <p className={styles.errorMessage}>{message}</p>
        </div>

        {requestId && (
          <div className={styles.reqIdRow}>
            <span>Request ID:</span>
            <code className={`${styles.reqIdCode} font-mono`}>{requestId}</code>
            <button
              type="button"
              className={styles.copyBtn}
              onClick={handleCopyRequestId}
              title="Sao chép Request ID"
            >
              {copied ? <Check size={14} /> : <Copy size={14} />}
              <span>{copied ? 'Đã chép' : 'Sao chép'}</span>
            </button>
          </div>
        )}

        <div className={styles.actions}>
          {onRetry && (
            <button
              type="button"
              className="btn btn-secondary btn-sm"
              onClick={onRetry}
            >
              Thử lại
            </button>
          )}
          {onDismiss && (
            <button
              type="button"
              className="btn btn-ghost btn-sm"
              onClick={onDismiss}
            >
              Đóng
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
