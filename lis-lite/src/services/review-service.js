export class 审核服务 {
  constructor(数据库, 审计) { this.数据库 = 数据库; this.审计 = 审计; }
  审核({ 结果ID, 审核人ID, 审核级别 }) {
    const 结果 = this.数据库.结果.find(x => x.id === 结果ID), 用户 = this.数据库.用户.find(x => x.id === 审核人ID);
    if (!结果 || !用户) throw new Error('结果或审核人员不存在'); if (结果.状态 === '已锁定') throw new Error('批次质控失控，结果及报告已锁定');
    if (结果.签署.some(x => x.审核人ID === 审核人ID)) throw new Error('同一审核人不可重复签署');
    if (!结果.危急 && 审核级别 !== '初审') throw new Error('常规结果仅需初审');
    if (结果.危急 && !['初审', '复审'].includes(审核级别)) throw new Error('危急值仅支持初审或复审');
    if (审核级别 === '复审' && !结果.签署.some(x => x.审核级别 === '初审')) throw new Error('危急值须先完成初审');
    const 签署 = { 审核人ID, 审核级别, 时间: new Date().toISOString(), 签名摘要: `${审核人ID}:${结果ID}:${Date.now()}` }; 结果.签署.push(签署);
    if (结果.危急) { const 告警 = this.数据库.危急值.find(x => x.结果ID === 结果ID); 告警.签署.push(签署); if (告警.签署.length === 2) { 告警.状态 = '已双签'; 告警.通知状态 = '已推送'; 结果.状态 = '已审核'; } }
    else 结果.状态 = '已审核';
    this.审计.记录('HOSP-A', 审核人ID, `${审核级别}审核`, '结果', 结果ID, { 危急: 结果.危急 }); return 结果;
  }
}
