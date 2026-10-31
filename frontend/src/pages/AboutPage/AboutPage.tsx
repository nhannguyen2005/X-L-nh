import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  ShieldCheck,
  Scales,
  Cpu,
  Warning,
  Database,
  ArrowRight,
} from '@phosphor-icons/react';
import { SignGlyph } from '../../components/SignGlyph/SignGlyph';
import { api } from '../../api/client';
import type { SignItem, HealthResponse } from '../../api/types';
import styles from './AboutPage.module.css';

interface AboutPageProps {
  health: HealthResponse | null;
}

export const AboutPage: React.FC<AboutPageProps> = ({ health }) => {
  const [signs, setSigns] = useState<SignItem[]>([]);

  useEffect(() => {
    api.listSigns({ page_size: 50 }).then((res) => setSigns(res.items)).catch(console.error);
  }, []);

  return (
    <div className={styles.page}>
      <div className={`container ${styles.container}`}>
        {/* Header */}
        <header className={styles.header}>
          <h1 className={styles.title}>Giới thiệu &amp; Nguồn tài liệu</h1>
          <p className={styles.subtitle}>
            Hệ thống web nhận diện biển báo giao thông Việt Nam và giải thích ý nghĩa, khuyến nghị an toàn
            bằng kỹ thuật xử lý ảnh và học sâu.
          </p>
        </header>

        {/* Section 1: Mục đích & Phạm vi */}
        <section className={`ui-card ${styles.card}`}>
          <div className={styles.cardHeader}>
            <ShieldCheck size={22} className={styles.cardIcon} />
            <h2 className={styles.cardTitle}>1. Mục đích và phạm vi đề tài</h2>
          </div>
          <div className={styles.cardBody}>
            <p>
              Đồ án xây dựng một ứng dụng web minh họa quy trình từ ảnh đầu vào đến kết quả nhận diện và
              thông tin giải thích chi tiết. Bài toán cốt lõi là <strong>Object Detection</strong>: xác định
              đồng thời vị trí (bounding box) và lớp (class) của các biển báo xuất hiện trong ảnh đường phố.
            </p>
            <div className={styles.callout}>
              <strong>Phạm vi MVP:</strong> Xử lý ảnh tĩnh (JPG/PNG), xác thực dung lượng/định dạng, phát
              hiện và phân loại tập lớp biển báo đã chọn, vẽ bounding box và độ tin cậy, liên kết tra cứu
              nội dung quy chuẩn, và có trạng thái cảnh báo khi độ tin cậy thấp hoặc không phát hiện.
            </div>
          </div>
        </section>

        {/* Section 2: 23 Lớp biển báo hỗ trợ */}
        <section className={`ui-card ${styles.card}`}>
          <div className={styles.cardHeader}>
            <Database size={22} className={styles.cardIcon} />
            <h2 className={styles.cardTitle}>2. Danh mục 23 lớp biển báo hỗ trợ</h2>
          </div>
          <div className={styles.cardBody}>
            <p>
              Hệ thống được lập danh mục kiểm chứng đồng bộ từ nhãn huấn luyện đến hiển thị gồm{' '}
              <strong>{signs.length || 23} lớp</strong> thuộc 4 nhóm biển báo chính:
            </p>

            <div className={styles.signsGrid}>
              {signs.map((sign) => (
                <Link
                  key={sign.id}
                  to={`/signs/${sign.id}`}
                  className={styles.signPill}
                >
                  <SignGlyph group={sign.group_name} size={20} />
                  <span className={`${styles.signCode} font-mono`}>{sign.sign_code}</span>
                  <span className={styles.signName}>{sign.name}</span>
                </Link>
              ))}
            </div>

            <div style={{ marginTop: '16px' }}>
              <Link to="/signs" className="btn btn-secondary btn-sm">
                <span>Xem chi tiết tra cứu đầy đủ</span>
                <ArrowRight size={14} />
              </Link>
            </div>
          </div>
        </section>

        {/* Section 3: Giới hạn đã biết */}
        <section className={`ui-card ${styles.card}`}>
          <div className={styles.cardHeader}>
            <Warning size={22} className={styles.cardIcon} />
            <h2 className={styles.cardTitle}>3. Giới hạn đã biết &amp; khuyến cáo</h2>
          </div>
          <div className={styles.cardBody}>
            <ul className={styles.list}>
              <li>
                <strong>Mục đích học thuật:</strong> Hệ thống được thiết kế phục vụ nghiên cứu và hỗ trợ
                học tập, tuyệt đối không thay thế việc quan sát biển báo thực tế khi tham gia giao thông.
              </li>
              <li>
                <strong>Điều kiện ngoại cảnh:</strong> Chất lượng nhận diện có thể bị ảnh hưởng khi ảnh chụp
                ngược sáng mạnh, ban đêm thiếu sáng, biển báo bị mờ do chuyển động, hoặc bị che khuất một phần.
              </li>
              <li>
                <strong>Ngữ cảnh đường sá:</strong> Biển phụ, vạch kẻ đường và hiệu lệnh của người điều khiển
                giao thông có thể ưu tiên hoặc thay đổi ý nghĩa của biển báo trong tình huống cụ thể.
              </li>
            </ul>
          </div>
        </section>

        {/* Section 4: Căn cứ pháp lý */}
        <section className={`ui-card ${styles.card}`}>
          <div className={styles.cardHeader}>
            <Scales size={22} className={styles.cardIcon} />
            <h2 className={styles.cardTitle}>4. Căn cứ pháp lý và kiểm chứng nội dung</h2>
          </div>
          <div className={styles.cardBody}>
            <p>
              Toàn bộ tên gọi, ý nghĩa, mã biển báo và khuyến nghị hành vi tuân thủ được trích xuất và đối
              chiếu trực tiếp từ:
            </p>
            <div className={styles.legalQuote}>
              <strong>Quy chuẩn kỹ thuật Quốc gia về báo hiệu đường bộ — QCVN 41:2019/BGTVT</strong>
              <br />
              (Ban hành kèm theo Thông tư số 54/2019/TT-BGTVT ngày 31 tháng 12 năm 2019 của Bộ Giao thông vận tải).
            </div>
            <p style={{ fontSize: '13px', color: 'var(--color-text-muted)' }}>
              Ngày cập nhật và kiểm chứng cơ sở dữ liệu: <strong>30/10/2026</strong>. Không tự suy đoán
              hoặc sử dụng văn bản pháp lý không chính thống.
            </p>
          </div>
        </section>

        {/* Section 5: Công nghệ & Phiên bản */}
        <section className={`ui-card ${styles.card}`}>
          <div className={styles.cardHeader}>
            <Cpu size={22} className={styles.cardIcon} />
            <h2 className={styles.cardTitle}>5. Công nghệ &amp; Phiên bản hệ thống</h2>
          </div>
          <div className={styles.cardBody}>
            <div className={styles.techGrid}>
              <div className={styles.techItem}>
                <span className={styles.techKey}>Frontend:</span>
                <span className={styles.techVal}>React 19 + TypeScript + Vite + Vanilla CSS Tokens</span>
              </div>
              <div className={styles.techItem}>
                <span className={styles.techKey}>Backend:</span>
                <span className={styles.techVal}>Python 3.13 + FastAPI + SQLAlchemy + Pydantic v2</span>
              </div>
              <div className={styles.techItem}>
                <span className={styles.techKey}>Xử lý ảnh &amp; ML:</span>
                <span className={styles.techVal}>OpenCV + Ultralytics YOLO (Nano Detector)</span>
              </div>
              <div className={styles.techItem}>
                <span className={styles.techKey}>Cơ sở dữ liệu:</span>
                <span className={styles.techVal}>SQLite (Idempotent seed)</span>
              </div>
              <div className={styles.techItem}>
                <span className={styles.techKey}>Phiên bản Model:</span>
                <span className={`${styles.techVal} font-mono`}>{health?.model_version || 'yolov8n-signs-v1.0'}</span>
              </div>
              <div className={styles.techItem}>
                <span className={styles.techKey}>Phiên bản Dataset:</span>
                <span className={`${styles.techVal} font-mono`}>{health?.dataset_version || 'vietnam-traffic-signs-v1.0'}</span>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};
