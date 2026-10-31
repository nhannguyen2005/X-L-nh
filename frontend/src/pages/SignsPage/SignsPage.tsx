import React, { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { MagnifyingGlass, CaretLeft, CaretRight, X } from '@phosphor-icons/react';
import { SignGlyph } from '../../components/SignGlyph/SignGlyph';
import { SignGroupChip } from '../../components/SignGroupChip/SignGroupChip';
import { EmptyState } from '../../components/EmptyState/EmptyState';
import { api } from '../../api/client';
import type { SignItem, SignGroupSummary } from '../../api/types';
import styles from './SignsPage.module.css';

export const SignsPage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const qParam = searchParams.get('q') || '';
  const groupParam = searchParams.get('group') || '';
  const pageParam = parseInt(searchParams.get('page') || '1', 10);

  const [searchInput, setSearchInput] = useState(qParam);
  const [signs, setSigns] = useState<SignItem[]>([]);
  const [groups, setGroups] = useState<SignGroupSummary[]>([]);
  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(true);

  // Fetch groups once
  useEffect(() => {
    api.getSignGroups().then(setGroups).catch(console.error);
  }, []);

  // Debounce search query update to URL
  useEffect(() => {
    const timer = setTimeout(() => {
      setSearchParams((prev) => {
        const next = new URLSearchParams(prev);
        if (searchInput.trim()) {
          next.set('q', searchInput.trim());
        } else {
          next.delete('q');
        }
        next.set('page', '1');
        return next;
      });
    }, 300);
    return () => clearTimeout(timer);
  }, [searchInput, setSearchParams]);

  // Fetch signs on search param changes
  useEffect(() => {
    setLoading(true);
    api
      .listSigns({
        q: qParam || undefined,
        group: groupParam || undefined,
        page: pageParam,
        page_size: 16,
      })
      .then((res) => {
        setSigns(res.items);
        setTotal(res.total);
        setTotalPages(res.total_pages);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [qParam, groupParam, pageParam]);

  const handleGroupSelect = (groupName: string) => {
    setSearchParams((prev) => {
      const next = new URLSearchParams(prev);
      if (groupName) {
        next.set('group', groupName);
      } else {
        next.delete('group');
      }
      next.set('page', '1');
      return next;
    });
  };

  const handlePageChange = (newPage: number) => {
    setSearchParams((prev) => {
      const next = new URLSearchParams(prev);
      next.set('page', newPage.toString());
      return next;
    });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const clearFilters = () => {
    setSearchInput('');
    setSearchParams(new URLSearchParams());
  };

  return (
    <div className={styles.page}>
      <div className="container">
        {/* Header */}
        <div className={styles.header}>
          <h1 className={styles.title}>Danh mục biển báo giao thông</h1>
          <p className={styles.description}>
            Cơ sở dữ liệu {total} biển báo được chuẩn hóa mã số, quy chuẩn ý nghĩa và khuyến nghị
            hành vi tuân thủ theo Quy chuẩn Kỹ thuật Quốc gia QCVN 41:2019/BGTVT.
          </p>
        </div>

        {/* Filter Bar with Search & Segmented Group Chips */}
        <div className={styles.filterSection}>
          {/* Search Box with top label */}
          <div className={styles.searchBox}>
            <label htmlFor="signs-search-input" className={styles.searchLabel}>
              Tìm theo tên hoặc mã biển:
            </label>
            <div className={styles.inputWrapper}>
              <MagnifyingGlass size={18} className={styles.searchIcon} />
              <input
                id="signs-search-input"
                type="text"
                placeholder="Nhập tên (ngược chiều, cấm vượt...) hoặc mã (P.102, W.201a)..."
                value={searchInput}
                onChange={(e) => setSearchInput(e.target.value)}
                className={styles.input}
              />
              {searchInput && (
                <button
                  type="button"
                  onClick={() => setSearchInput('')}
                  className={styles.clearBtn}
                  aria-label="Xóa nội dung tìm kiếm"
                >
                  <X size={16} />
                </button>
              )}
            </div>
          </div>

          {/* Group Filter Chips */}
          <div className={styles.groupChipsRow}>
            <button
              type="button"
              className={`${styles.groupChipBtn} ${!groupParam ? styles.chipActive : ''}`}
              onClick={() => handleGroupSelect('')}
            >
              <span>Tất cả nhóm</span>
              <span className={styles.chipCount}>{groups.reduce((acc, g) => acc + g.count, 0)}</span>
            </button>

            {groups.map((g) => (
              <button
                key={g.group_name}
                type="button"
                className={`${styles.groupChipBtn} ${
                  groupParam === g.group_name ? styles.chipActive : ''
                }`}
                onClick={() => handleGroupSelect(g.group_name)}
              >
                <SignGlyph group={g.group_name} size={16} />
                <span>{g.group_name}</span>
                <span className={styles.chipCount}>{g.count}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Results Grid */}
        {loading ? (
          <div className={styles.grid}>
            {Array.from({ length: 8 }).map((_, i) => (
              <div key={i} className={`ui-card ${styles.skeletonCard}`} />
            ))}
          </div>
        ) : signs.length === 0 ? (
          <div className={`ui-card ${styles.emptyWrapper}`}>
            <EmptyState
              title="Không tìm thấy biển báo phù hợp"
              description="Thử tìm kiếm với từ khóa khác hoặc xóa bộ lọc để hiển thị toàn bộ 23 lớp biển báo."
              action={
                <button type="button" className="btn btn-secondary btn-sm" onClick={clearFilters}>
                  Xóa bộ lọc
                </button>
              }
            />
          </div>
        ) : (
          <div className={styles.grid}>
            {signs.map((sign) => (
              <Link
                key={sign.id}
                to={`/signs/${sign.id}`}
                className={`ui-card ${styles.signCard}`}
              >
                <div className={styles.cardHeader}>
                  <div className={styles.glyphBox}>
                    {sign.image_url ? (
                      <img
                        src={sign.image_url}
                        alt={sign.name}
                        className={styles.signImg}
                        loading="lazy"
                      />
                    ) : (
                      <SignGlyph group={sign.group_name} size={38} />
                    )}
                  </div>
                  <SignGroupChip group={sign.group_name} size="sm" />
                </div>

                <div className={styles.cardBody}>
                  <span className={`${styles.codeBadge} font-mono`}>{sign.sign_code}</span>
                  <h3 className={styles.signTitle}>{sign.name}</h3>
                  <p className={styles.meaningSnippet}>{sign.meaning}</p>
                </div>

                <div className={styles.cardFooter}>
                  <span className={styles.sourceText}>Nguồn: {sign.legal_source}</span>
                  <span className={styles.viewLink}>Chi tiết &rarr;</span>
                </div>
              </Link>
            ))}
          </div>
        )}

        {/* Pagination */}
        {totalPages > 1 && (
          <div className={styles.pagination} aria-label="Phân trang">
            <button
              type="button"
              className="btn btn-secondary btn-sm"
              disabled={pageParam <= 1}
              onClick={() => handlePageChange(pageParam - 1)}
              aria-label="Trang trước"
            >
              <CaretLeft size={16} />
              <span>Trước</span>
            </button>

            <span className={`${styles.pageIndicator} font-mono tabular-nums`}>
              Trang {pageParam} / {totalPages}
            </span>

            <button
              type="button"
              className="btn btn-secondary btn-sm"
              disabled={pageParam >= totalPages}
              onClick={() => handlePageChange(pageParam + 1)}
              aria-label="Trang sau"
            >
              <span>Sau</span>
              <CaretRight size={16} />
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
