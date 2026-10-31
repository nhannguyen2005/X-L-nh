import React, { useState, useEffect } from 'react';
import { ChartBar, Info, Table as TableIcon, Image as ImageIcon } from '@phosphor-icons/react';
import { EmptyState } from '../../components/EmptyState/EmptyState';
import { api } from '../../api/client';
import type { MetricsResponse } from '../../api/types';
import styles from './EvaluationPage.module.css';

export const EvaluationPage: React.FC = () => {
  const [data, setData] = useState<MetricsResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .getMetrics()
      .then(setData)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className={styles.page}>
        <div className="container">
          <div className={styles.loadingBox}>
            <p>Đang đọc dữ liệu đánh giá thực tế từ artifacts/metrics...</p>
          </div>
        </div>
      </div>
    );
  }

  const hasData = data?.has_data && data?.metrics;
  const metrics = data?.metrics?.metrics;
  const experiment = data?.metrics?.experiment;
  const latency = data?.metrics?.latency;
  const classes = data?.metrics?.classes;
  const plots = data?.available_plots || [];

  return (
    <div className={styles.page}>
      <div className="container">
        {/* Header */}
        <div className={styles.header}>
          <h1 className={styles.title}>Đánh giá thực nghiệm mô hình</h1>
          <p className={styles.description}>
            Báo cáo định lượng về độ chính xác (Precision, Recall, mAP) và độ trễ xử lý (Latency)
            đo lường trên tập dữ liệu kiểm thử độc lập (Test Set) theo chuẩn kiểm thử học thuật.
          </p>
        </div>

        {!hasData ? (
          <div className={`ui-card ${styles.emptyCard}`}>
            <EmptyState
              icon={<ChartBar size={40} />}
              title="Chưa có kết quả đánh giá trên tập test độc lập"
              description={
                data?.message ||
                'Dữ liệu số liệu thực nghiệm sẽ tự động hiển thị tại đây sau khi bạn hoàn thành chạy script evaluate.py và tạo tệp artifacts/metrics/evaluation.json. Hệ thống tuân thủ nguyên tắc trung thực học thuật, không tạo số liệu giả.'
              }
            />
          </div>
        ) : (
          <div className={styles.bentoGrid}>
            {/* Cell 1: Experiment Info (2 cols) */}
            <div className={`ui-card ${styles.bentoCell} ${styles.colSpan2}`}>
              <div className={styles.cellHeader}>
                <Info size={18} className={styles.cellIcon} />
                <h3 className={styles.cellTitle}>Thông tin thiết lập thực nghiệm</h3>
              </div>
              <div className={styles.infoGrid}>
                <div>
                  <span className={styles.infoLabel}>Bộ dữ liệu:</span>
                  <p className={styles.infoVal}>{experiment?.dataset || 'Biển báo giao thông VN'}</p>
                </div>
                <div>
                  <span className={styles.infoLabel}>Phiên bản:</span>
                  <p className={`${styles.infoVal} font-mono`}>{experiment?.version || 'v1.0'}</p>
                </div>
                <div>
                  <span className={styles.infoLabel}>Mô hình:</span>
                  <p className={`${styles.infoVal} font-mono`}>{experiment?.model || 'YOLOv8n'}</p>
                </div>
                <div>
                  <span className={styles.infoLabel}>Thiết bị đo:</span>
                  <p className={styles.infoVal}>{experiment?.device || 'CPU'}</p>
                </div>
                <div>
                  <span className={styles.infoLabel}>Số ảnh test:</span>
                  <p className={`${styles.infoVal} font-mono tabular-nums`}>{experiment?.test_images ?? 'N/A'}</p>
                </div>
                <div>
                  <span className={styles.infoLabel}>Số vật thể test:</span>
                  <p className={`${styles.infoVal} font-mono tabular-nums`}>{experiment?.test_instances ?? 'N/A'}</p>
                </div>
              </div>
            </div>

            {/* Cells 2-6: Primary Metrics (1 col each) */}
            <div className={`ui-card ${styles.bentoCell} ${styles.metricCard}`}>
              <span className={styles.metricLabel}>Precision</span>
              <span className={`${styles.metricVal} font-mono tabular-nums`}>
                {metrics?.precision !== undefined ? (metrics.precision * 100).toFixed(1) + '%' : 'N/A'}
              </span>
              <span className={styles.metricSub}>TP / (TP + FP)</span>
            </div>

            <div className={`ui-card ${styles.bentoCell} ${styles.metricCard}`}>
              <span className={styles.metricLabel}>Recall</span>
              <span className={`${styles.metricVal} font-mono tabular-nums`}>
                {metrics?.recall !== undefined ? (metrics.recall * 100).toFixed(1) + '%' : 'N/A'}
              </span>
              <span className={styles.metricSub}>TP / (TP + FN)</span>
            </div>

            <div className={`ui-card ${styles.bentoCell} ${styles.metricCard}`}>
              <span className={styles.metricLabel}>F1-Score</span>
              <span className={`${styles.metricVal} font-mono tabular-nums`}>
                {metrics?.f1 !== undefined ? (metrics.f1 * 100).toFixed(1) + '%' : 'N/A'}
              </span>
              <span className={styles.metricSub}>Trung bình điều hòa</span>
            </div>

            <div className={`ui-card ${styles.bentoCell} ${styles.metricCard}`}>
              <span className={styles.metricLabel}>mAP@0.5</span>
              <span className={`${styles.metricVal} font-mono tabular-nums`}>
                {metrics?.map50 !== undefined ? (metrics.map50 * 100).toFixed(1) + '%' : 'N/A'}
              </span>
              <span className={styles.metricSub}>IoU ngưỡng 0.5</span>
            </div>

            <div className={`ui-card ${styles.bentoCell} ${styles.metricCard}`}>
              <span className={styles.metricLabel}>mAP@0.5:0.95</span>
              <span className={`${styles.metricVal} font-mono tabular-nums`}>
                {metrics?.map50_95 !== undefined ? (metrics.map50_95 * 100).toFixed(1) + '%' : 'N/A'}
              </span>
              <span className={styles.metricSub}>IoU 0.5 đến 0.95</span>
            </div>

            {/* Cell 7: Latency Measurement (2 cols) */}
            <div className={`ui-card ${styles.bentoCell} ${styles.colSpan2}`}>
              <div className={styles.cellHeader}>
                <ChartBar size={18} className={styles.cellIcon} />
                <h3 className={styles.cellTitle}>Độ trễ xử lý (Latency Benchmark)</h3>
              </div>
              <div className={styles.latencyGrid}>
                <div className={styles.latencyItem}>
                  <span className={styles.latencyLabel}>Tiền xử lý</span>
                  <span className={`${styles.latencyVal} font-mono tabular-nums`}>
                    {latency?.preprocess_ms !== undefined ? `${latency.preprocess_ms.toFixed(1)} ms` : '--'}
                  </span>
                </div>
                <div className={styles.latencyItem}>
                  <span className={styles.latencyLabel}>Suy luận (Inference)</span>
                  <span className={`${styles.latencyVal} font-mono tabular-nums`}>
                    {latency?.inference_ms !== undefined ? `${latency.inference_ms.toFixed(1)} ms` : '--'}
                  </span>
                </div>
                <div className={styles.latencyItem}>
                  <span className={styles.latencyLabel}>Hậu xử lý / NMS</span>
                  <span className={`${styles.latencyVal} font-mono tabular-nums`}>
                    {latency?.postprocess_ms !== undefined ? `${latency.postprocess_ms.toFixed(1)} ms` : '--'}
                  </span>
                </div>
                <div className={`${styles.latencyItem} ${styles.totalLatency}`}>
                  <span className={styles.latencyLabel}>Tổng thời gian</span>
                  <span className={`${styles.latencyVal} font-mono tabular-nums`}>
                    {latency?.total_ms !== undefined ? `${latency.total_ms.toFixed(1)} ms` : '--'}
                  </span>
                </div>
              </div>
            </div>

            {/* Cells 8 & 9: Plots (Confusion Matrix & PR Curve) */}
            {plots.map((plotName) => (
              <div key={plotName} className={`ui-card ${styles.bentoCell} ${styles.colSpan2}`}>
                <div className={styles.cellHeader}>
                  <ImageIcon size={18} className={styles.cellIcon} />
                  <h3 className={styles.cellTitle}>{plotName}</h3>
                </div>
                <div className={styles.plotImgWrap}>
                  <img
                    src={api.getPlotUrl(plotName)}
                    alt={`Biểu đồ đánh giá ${plotName}`}
                    className={styles.plotImg}
                    loading="lazy"
                  />
                </div>
              </div>
            ))}

            {/* Cell 10: Per-class Metrics Table (Full Width) */}
            {classes && classes.length > 0 && (
              <div className={`ui-card ${styles.bentoCell} ${styles.colSpanFull}`}>
                <div className={styles.cellHeader}>
                  <TableIcon size={18} className={styles.cellIcon} />
                  <h3 className={styles.cellTitle}>Chỉ số chi tiết theo từng lớp biển báo</h3>
                </div>
                <div className={styles.tableScroll}>
                  <table className={styles.classTable}>
                    <thead>
                      <tr>
                        <th>Mã lớp</th>
                        <th>Tên nhãn lớp</th>
                        <th className={styles.numCol}>Số vật thể</th>
                        <th className={styles.numCol}>Precision</th>
                        <th className={styles.numCol}>Recall</th>
                        <th className={styles.numCol}>F1-Score</th>
                        <th className={styles.numCol}>mAP@0.5</th>
                        <th className={styles.numCol}>mAP@0.5:0.95</th>
                      </tr>
                    </thead>
                    <tbody>
                      {classes.map((c) => (
                        <tr key={c.class_id}>
                          <td className="font-mono tabular-nums">{c.class_id}</td>
                          <td className={styles.classNameCell}>{c.class_name}</td>
                          <td className={`${styles.numCol} font-mono tabular-nums`}>{c.instances}</td>
                          <td className={`${styles.numCol} font-mono tabular-nums`}>
                            {(c.precision * 100).toFixed(1)}%
                          </td>
                          <td className={`${styles.numCol} font-mono tabular-nums`}>
                            {(c.recall * 100).toFixed(1)}%
                          </td>
                          <td className={`${styles.numCol} font-mono tabular-nums`}>
                            {(c.f1 * 100).toFixed(1)}%
                          </td>
                          <td className={`${styles.numCol} font-mono tabular-nums`}>
                            {(c.map50 * 100).toFixed(1)}%
                          </td>
                          <td className={`${styles.numCol} font-mono tabular-nums`}>
                            {(c.map50_95 * 100).toFixed(1)}%
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
