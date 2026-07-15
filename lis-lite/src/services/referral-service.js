export class 转检服务 {
  constructor(数据库, 审计) { this.数据库 = 数据库; this.审计 = 审计; }
  外送({ 源标本ID, 目标机构ID, 操作人ID, 项目ID列表 }) {
    const 标本 = this.数据库.标本.find(x => x.id === 源标本ID); if (!标本) throw new Error('标本不存在');
    const 关系 = this.数据库.合作关系.find(x => x.源机构ID === 标本.机构ID && x.目标机构ID === 目标机构ID && x.状态 === '启用'); if (!关系) throw new Error('无有效合作关系');
    const 单号 = `REF-${String(this.数据库.转检.length + 1).padStart(6, '0')}`;
    const 脱敏载荷 = { 转检单号: 单号, 脱敏患者令牌: `PTK-${标本.id}`, 性别: 标本.患者.性别, 年龄: 标本.患者.年龄, 标本类型: 标本.标本类型, 项目: 项目ID列表 };
    const 转检单 = { 单号, 源机构ID: 标本.机构ID, 目标机构ID, 源标本ID, 项目ID列表, 状态: '已发送', 脱敏载荷, 回传: null };
    this.数据库.转检.push(转检单); 标本.状态 = '已外送'; this.审计.记录(标本.机构ID, 操作人ID, '外送转检', '转检单', 单号, { 目标机构ID }); return 转检单;
  }
  合作机构视图({ 单号, 当前机构ID }) { const t = this.数据库.转检.find(x => x.单号 === 单号 && x.目标机构ID === 当前机构ID); if (!t) throw new Error('无权访问转检单'); return t.脱敏载荷; }
  回传({ 单号, 当前机构ID, 结果值, 单位, 审核摘要 }) { const t = this.数据库.转检.find(x => x.单号 === 单号 && x.目标机构ID === 当前机构ID); if (!t) throw new Error('无权回传转检结果'); t.回传 = { 结果值, 单位, 审核摘要, 时间: new Date().toISOString() }; t.状态 = '已回传'; return t; }
}
