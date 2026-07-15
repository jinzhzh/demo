/** audit-log 数据模型：生产环境映射为 PostgreSQL 表，并强制机构ID隔离。 */
export const audit_log模型 = Object.freeze({ 名称: "audit-log", 主键: "id", 审计: true });
