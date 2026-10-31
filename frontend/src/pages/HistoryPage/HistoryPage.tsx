import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  ClockCounterClockwise,
  Trash,
  MagnifyingGlass,
  FileImage,
  CaretLeft,
  CaretRight,
} from '@phosphor-icons/react';
import { EmptyState } from '../../components/EmptyState/EmptyState';
import { InlineError } from '../../components/InlineError/InlineError';
import { api } from '../../api/client';
import type { HistoryItem } from '../../api/types';
import styles from './HistoryPage.module.css';

export const HistoryPage: React.FC = () => {
  const [items, setItems] = useState<HistoryItem[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<any>(null);

  const fetchHistory = (currentPage: number, query: string) => {
    setLoading(true);
    api
      .getHistory({ page: currentPage, page_size: 15, q: query.trim() || undefined })
      .then((res) => {
        setItems(res.items);
        setTotal(res.total);
        setTotalPages(res.total_pages);
      })
      .catch((err) => setError(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchHistory(page, search);
  }, [page]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(1);
    fetchHistory(1, search);
  };

  const handleDeleteItem = async (id: number) => {
    if (!window.confirm('Bạn có chắc chắn muốn xóa bản ghi lịch sử này?')) return;
    try {
      await api.deleteHistoryById(id);
      fetchHistory(page, search);
    } catch (err: any) {
      alert(`Lỗi khi xóa: ${err.message || 'Không thể xóa bản ghi'}`);
    }
  };

  const handleClearAll = async () => {
    if (!window.confirm('Bạn có chắc chắn muốn xóa toàn bộ lịch sử quét? Thao tác này không thể hoàn tác.')) {
      return;
    }
    try {
      await api.clearHistory();
      fetchHistory(1, '');
    } catch (err: any) {
      alert(`Lỗi khi xóa: ${err.message || 'Không thể xóa lịch sử'}`);
    }
  };

  const formatDate = (isoString: string) => {
    try {
      const d = new Date(isoString);
      return d.toLocaleString('vi-VN', {
        hour: '2-digit',
        minute: '2-digit',
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
      });
    } catch {
      return isoString;
    }
  };

  return (
    <div className={styles.page}>
      <div className="container">
        {/* Header */}
        <div className={styles.header}>
          <div>
            <h1 className={styles.title}>Lịch sử quét ảnh</h1>
            <p className={styles.subtitle}>
              Lưu trữ thời gian, tệp ảnh và kết quả nhận diện biển báo khi người dùng bật tùy chọn "Lưu vào lịch sử".
            </p>
          </div>

          {items.length > 0 && (
            <button
              type="button"
              className="btn btn-secondary btn-sm"
              onClick={handleClearAll}
              title="Xóa toàn bộ bản ghi lịch sử"
            >
              <Trash size={16} />
              <span>Xóa toàn bộ</span>
            </button>
          )}
        </div>

        {error && (
          <div style={{ marginBottom: '20px' }}>
            <InlineError error={error} onRetry={() => fetchHistory(page, search)} />
          </div>
        )}

        {/* Filter bar */}
        <form onSubmit={handleSearchSubmit} className={styles.searchForm}>
          <div className={styles.searchWrapper}>
            <MagnifyingGlass size={18} className={styles.searchIcon} />
            <input
              type="text"
              placeholder="Tìm theo tên file, nhãn biển báo hoặc Request ID..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className={styles.searchInput}
            />
          </div>
          <button type="submit" className="btn btn-secondary btn-sm">
            Tìm kiếm
          </button>
        </form>

        {/* Content */}
        {loading ? (
          <div className={styles.loadingBox}>
            <p>Đang tải lịch sử...</p>
          </div>
        ) : items.length === 0 ? (
          <div className={`ui-card ${styles.emptyCard}`}>
            <EmptyState
              icon={<ClockCounterClockwise size={36} />}
              title="Chưa có lịch sử quét"
              description="Lịch sử chỉ được ghi khi bạn bật tùy chọn 'Lưu vào lịch sử' tại màn hình Quét ảnh. Hãy thử quét một ảnh mới và bật tùy chọn này."
              action={
                <Link to="/" className="btn btn-primary btn-sm">
                  Đến trang Quét ảnh
                </Link>
              }
            />
          </div>
        ) : (
          <>
            {/* Desktop Table View */}
            <div className={`ui-card ${styles.tableCard}`}>
              <table className={styles.table}>
                <thead>
                  <tr>
                    <th>Thời gian</th>
                    <th>Tên tệp</th>
                    <th className={styles.numCol}>Số biển</th>
                    <th className={styles.numCol}>Xử lý (ms)</th>
                    <th>Chi tiết nhãn phát hiện</th>
                    <th className={styles.actionCol}>Thao tác</th>
                  </tr>
                </thead>
                <tbody>
                  {items.map((item) => (
                    <tr key={item.id}>
                      <td className={`${styles.timeCell} font-mono tabular-nums`}>
                        {formatDate(item.created_at)}
                      </td>
                      <td className={styles.fileCell}>
                        <div className={styles.fileRow}>
                          <FileImage size={18} className={styles.fileIcon} />
                          <span className={styles.fileName}>{item.original_filename}</span>
                        </div>
                      </td>
                      <td className={`${styles.numCol} font-mono tabular-nums`}>
                        <span
                          className={`${styles.countBadge} ${
                            item.detection_count > 0 ? styles.countPositive : styles.countZero
                          }`}
                        >
                          {item.detection_count}
                        </span>
                      </td>
                      <td className={`${styles.numCol} font-mono tabular-nums`}>
                        {item.processing_ms.toFixed(1)}
                      </td>
                      <td className={styles.classesCell}>
                        {item.result?.classes && item.result.classes.length > 0 ? (
                          <div className={styles.chipsRow}>
                            {item.result.classes.map((cls, idx) => (
                              <span key={idx} className={styles.classChip}>
                                {cls}
                              </span>
                            ))}
                          </div>
                        ) : (
                          <span className={styles.noClasses}>Không có biển báo</span>
                        )}
                      </td>
                      <td className={styles.actionCol}>
                        <button
                          type="button"
                          className={styles.delBtn}
                          onClick={() => handleDeleteItem(item.id)}
                          aria-label={`Xóa bản ghi ${item.original_filename}`}
                          title="Xóa bản ghi này"
                        >
                          <Trash size={16} />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Mobile Card List View */}
            <div className={styles.mobileList}>
              {items.map((item) => (
                <div key={item.id} className={`ui-card ${styles.mobileCard}`}>
                  <div className={styles.mobileCardHeader}>
                    <div className={styles.fileRow}>
                      <FileImage size={18} className={styles.fileIcon} />
                      <span className={styles.fileName}>{item.original_filename}</span>
                    </div>
                    <button
                      type="button"
                      className={styles.delBtn}
                      onClick={() => handleDeleteItem(item.id)}
                      aria-label="Xóa bản ghi"
                    >
                      <Trash size={16} />
                    </button>
                  </div>

                  <div className={styles.mobileMetaRow}>
                    <span className="font-mono tabular-nums">{formatDate(item.created_at)}</span>
                    <span className="font-mono tabular-nums">{item.processing_ms.toFixed(1)} ms</span>
                    <span className={styles.countBadge}>
                      {item.detection_count} biển phát hiện
                    </span>
                  </div>

                  {item.result?.classes && item.result.classes.length > 0 && (
                    <div className={styles.chipsRow}>
                      {item.result.classes.map((cls, idx) => (
                        <span key={idx} className={styles.classChip}>
                          {cls}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className={styles.pagination}>
                <button
                  type="button"
                  className="btn btn-secondary btn-sm"
                  disabled={page <= 1}
                  onClick={() => setPage(page - 1)}
                >
                  <CaretLeft size={16} />
                  <span>Trước</span>
                </button>
                <span className="font-mono tabular-nums">
                  Trang {page} / {totalPages} ({total} bản ghi)
                </span>
                <button
                  type="button"
                  className="btn btn-secondary btn-sm"
                  disabled={page >= totalPages}
                  onClick={() => setPage(page + 1)}
                >
                  <span>Sau</span>
                  <CaretRight size={16} />
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};
