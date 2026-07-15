import { 标本状态 } from '../domain/enums.js';

export class 标本服务 {
  constructor(数据库, 审计) { this.数据库 = 数据库; this.审计 = 审计; }
  接收({ 机构ID, 患者, 项目ID列表, 操作人ID, 标本类型 = '血清' }) {
    const 序号 = String(this.数据库.标本.length + 1).padStart(6, '0');
    const 标本 = { id: `SP-${序号}`, 机构ID, 条码: `LIS${new Date().toISOString().slice(0, 10).replaceAll('-', '')}${序号}`, 患者, 项目ID列表, 标本类型, 状态: 标本状态.已接收, 接收时间: new Date().toISOString(), 结果: [], 报告: null };
    this.数据库.标本.push(标本); this.审计.记录(机构ID, 操作人ID, '标本接收', '标本', 标本.id, { 条码: 标本.条码 }); return 标本;
  }
  查询(机构ID, 标本ID) { const 标本 = this.数据库.标本.find(x => x.id === 标本ID); if (!标本 || 标本.机构ID !== 机构ID) throw new Error('无权访问该标本'); return 标本; }
}
