import { 渲染报告HTML } from '../pdf/report-renderer.js';
export class 报告服务 {
  constructor(数据库, 审计) { this.数据库 = 数据库; this.审计 = 审计; }
  签发({ 标本ID, 签发人ID }) {
    const 标本 = this.数据库.标本.find(x => x.id === 标本ID), 结果 = this.数据库.结果.filter(x => x.标本ID === 标本ID);
    if (!标本 || !结果.length) throw new Error('标本或结果不存在'); if (结果.some(x => x.状态 === '已锁定')) throw new Error('质控失控，报告锁定');
    if (结果.some(x => x.状态 !== '已审核')) throw new Error('存在未审核结果，不能签发报告');
    if (结果.some(x => x.危急 && this.数据库.危急值.find(a => a.结果ID === x.id)?.签署.length !== 2)) throw new Error('危急值未完成双签，不能签发报告');
    const 报告 = { 编号: `RPT-${String(this.数据库.报告.length + 1).padStart(6, '0')}`, 标本ID, 签发人ID, 签发时间: new Date().toISOString(), 状态: '已签发', HTML: 渲染报告HTML({ 标本, 结果列表: 结果, 项目表: this.数据库.项目 }) };
    this.数据库.报告.push(报告); 标本.报告 = 报告.编号; 标本.状态 = '已签发'; this.审计.记录('HOSP-A', 签发人ID, '签发PDF报告', '报告', 报告.编号); return 报告;
  }
}
